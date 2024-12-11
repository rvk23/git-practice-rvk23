"""Interpreter for Datalog programs.

Provides an interpreter interface for interpreting Datalog
programs using relational algebra.
"""

from typing import Iterator, Dict

from project3.datalogprogram import DatalogProgram, Predicate, Rule, Parameter
from project3.relation import Relation, IncompatibleOperandError


class Interpreter:
    """Interpreter class for Datalog.

    Defines the interface, and a place for the implementation, for interpreting
    Datalog programs. The interpreter must be implemented using relational algebra,
    so new attributes must be added to track the named relations in the Datalog
    program during the lifetime of the interpreter.

    Attributes:
        datalog (DatalogProgram): The Datalog program to interpret.
    """

    __slots__ = ["datalog", "relations"]

    def __init__(self, datalog: DatalogProgram) -> None:
        self.datalog = datalog
        self.relations: Dict[str, Relation] = {}
        print(f"Initialized Interpreter with DatalogProgram: {datalog}")

    def eval_schemes(self) -> None:
        """Evaluate the schemes in the Datalog program.

        Create, and store in the interpreter, a relation for each scheme
        in the Datalog program. The _name_ of the scheme must be stored
        separate from the relation since the `Relation` type has no name
        attribute.
        """
        for scheme in self.datalog.schemes:
            values = [param.value for param in scheme.parameters]
            print(f"Processing scheme: {scheme.name}, values: {values}")
            if not values:
                print(f"Warning: Scheme {scheme.name} has no values!")
            relation = Relation(values, set())
            self.relations[scheme.name] = relation
            print(
                f"Created relation for scheme {scheme.name} with header: {relation.header}"
            )

    def eval_facts(self) -> None:
        """Evaluate the facts in the Datalog program.

        Create, and store in the appropriate relation belonging to the
        interpreter, a tuple for each fact in the Datalog program.
        """

        for fact in self.datalog.facts:
            relation = self.relations.get(fact.name)
            if relation:
                values = [param.value for param in fact.parameters]
                print(f"Fact values to add: {values}")
                print(f"Relation header: {relation.header}")
                if len(values) == len(relation.header):
                    relation.add_tuple(tuple(values))
                    print(
                        f"Added fact to relation {fact.name}: {relation.set_of_tuples}"
                    )
                else:
                    print(
                        f"Fact length mismatch: {len(values)} != {len(relation.header)}"
                    )
                    raise ValueError(
                        f"Fact values length {len(values)} does not match header length {len(relation.header)}"
                    )

    def eval_queries(self) -> Iterator[tuple[Predicate, Relation]]:
        """Yield each query and resulting relation from evaluation."

        For each query in the Datalog program, evaluate the query to get a
        resulting relation that is the answer to the query, and then yield
        the resulting `(query, relation)` tuple.

        Returns:
            out (tuple[Predicate, Relation]): An iterator to a tuple where the
            first element is the predicate for the query and the second element
            is the relation for the answer.
        """

        for query in self.datalog.queries:
            relation = self.relations.get(query.name)
            if not relation:
                print(f"No relation found for query: {query.name}")
                continue

            query_values = [param.value for param in query.parameters]
            result = relation

            print(f"Processing query: {query}")
            print(f"Query values: {query_values}")
            print(f"Initial relation: {relation.set_of_tuples}")

            for i, value in enumerate(query_values):
                if value.startswith("'"):
                    try:
                        print(f"Selecting where {relation.header[i]} equals {value}")
                        result = result.select_eq_lit(relation.header[i], value)
                        print(f"Result after select_eq_lit: {result.set_of_tuples}")
                    except IncompatibleOperandError:
                        print(f"Incompatible operand: {relation.header[i]} and {value}")
                        continue

            unique_vars = list(dict.fromkeys(query_values))
            for var in unique_vars:
                var_positions = [
                    i for i, value in enumerate(query_values) if value == var
                ]
                if len(var_positions) > 1:
                    for i in range(1, len(var_positions)):
                        result = result.select_eq_col(
                            relation.header[var_positions[0]],
                            relation.header[var_positions[i]],
                        )
                        print(
                            f"Result after handling repeated variable {var}: {result.set_of_tuples}"
                        )

            variable_positions = [
                i for i, value in enumerate(query_values) if not value.startswith("'")
            ]

            column_map = {
                relation.header[i]: query.parameters[i].value
                for i in variable_positions
            }

            projected_columns = [relation.header[i] for i in variable_positions]

            print(f"Variable positions: {variable_positions}")
            print(f"Projecting to columns: {projected_columns}")

            if projected_columns:
                result = result.project(projected_columns)
                print(f"Result after project: {result.set_of_tuples}")

                new_header = [column_map[col] for col in projected_columns]
                result.header = new_header
                print(f"Updated relation header: {result.header}")

                unique_header = list(dict.fromkeys(result.header))
                formatted_tuples = {
                    tuple(row[result.header.index(col)] for col in unique_header)
                    for row in result.set_of_tuples
                }
                result.header = unique_header
                result.set_of_tuples = formatted_tuples
                print(
                    f"Updated relation header after removing duplicates: {result.header}"
                )
                print(f"Formatted tuples to match new header: {result.set_of_tuples}")

            yield (query, result)

    def eval_rules(self) -> Iterator[tuple[Relation, Rule, Relation]]:
        """Yield each _before_ relation, rule, and _after_ relation from evaluation.

        For each rule in the Datalog program, yield as a tuple the relation associated
        with the rule before evaluating the rule one time, the rule itself, and then
        the resulting relation after evaluating the rule one time. This process
        should repeat until the associated relations stop changing.
        All the generated facts should be stored in the appropriate relation
        in the interpreter.

        For example, given `rule_a` for relation `A`, `rule_b` for
        relation `B`, and that it takes three evaluations to see no change, then
        `eval_rules` should:

            yield((A_0, rule_a, A_1))
            yield((B_0, rule_b, B_1))
            yield((A_1, rule_a, A_2))
            yield((B_1, rule_b, B_2))
            yield((A_2, rule_a, A_3))
            yield((B_2, rule_b, B_3))

        Here `A_0` is the initial relation for `A`, `A_1` is the relation after evaluating
        `rule_a` on `A_0` etc. The same for `B`. The iteration stops because `A_2 == A_3` and
        `B_2 == B_3`.

        Returns:
            out (Iterator[tuple[Relation, Rule, Relation]]): An iterator to a tuple where the
                first element is the relation before rule evaluation, the second element is
                the rule associated with the relation, and the third element is the relation
                resulting from the rule evaluation.
        """

        for rule in self.datalog.rules:
            head_relation = self.relations.get(rule.head.name)
            if not head_relation:
                continue

            before_relation = Relation(
                head_relation.header, head_relation.set_of_tuples.copy()
            )
            new_tuples = set()

            head_values = getattr(rule.head, "values", [])
            header_map = {
                var: col for var, col in zip(head_values, head_relation.header)
            }

            rule_body = getattr(rule, "body", [])
            for predicate in rule_body:
                body_relation = self.relations.get(predicate.name)
                if not body_relation:
                    continue

                predicate_values = getattr(predicate, "values", [])
                selected_relation = body_relation
                for i, val in enumerate(predicate_values):
                    if val != "_" and val in header_map:
                        selected_relation = selected_relation.select_eq_lit(
                            header_map[val], val
                        )

                projected_relation = selected_relation.project(head_relation.header)
                new_tuples.update(projected_relation.set_of_tuples)

            after_relation = Relation(
                before_relation.header, before_relation.set_of_tuples.union(new_tuples)
            )
            yield (before_relation, rule, after_relation)

            self.relations[rule.head.name] = after_relation

    def eval_rules_optimized(self) -> Iterator[tuple[Relation, Rule, Relation]]:
        """Yield each _before_ relation, rule, and _after_ relation from optimized evaluation.

        This function is the same as the `eval_rules` function only it groups rules by strongly
        connected components (SCC) in the dependency graph from the rules in the Datalog
        program. So given the first SCC is with `rule_a` for relation `A`, `rule_b` for
        relation `B`, that takes three evaluations to see no change, and the second SCC with
        `rule_c for relation C that takes two evaluations to see no change, then
        `eval_rules_opt` should:

            yield((A_0, rule_a, A_1))
            yield((B_0, rule_b, B_1))
            yield((A_1, rule_a, A_2))
            yield((B_1, rule_b, B_2))
            yield((A_2, rule_a, A_3))
            yield((B_2, rule_b, B_3))
            yield((C_0, rule_c, C_1))
            yield((C_1, rule_c, C_2))

        Here `A_0` is the initial relation for `A`, `A_1` is the relation after evaluating
        `rule_a` on `A_0` etc. The same for `B` and `C`. The iteration on the first SCC stops
        because `A_2 == A_3` and `B_2 == B_3`. After the iteration for the second SCC starts
        and stops after two iterations when `C_1 == C_2`.

        Returns:
            out (Iterator[tuple[Relation, Rule, Relation]]): An iterator to a tuple where the
                first element is the relation before rule evaluation, the second element is the
                rule associated with the relation, and the third element is the relation resulting
                from the rule evaluation.
        """

        dependency_graph = self.get_rule_dependency_graph()
        for idx, (rule_name, dependencies) in enumerate(dependency_graph.items()):
            rule = next(
                (
                    r
                    for r in self.datalog.rules
                    if getattr(r, "name", f"R{idx}") == rule_name
                ),
                None,
            )
            if not rule:
                continue

            before_relation = self.relations.get(
                getattr(rule.head, "name", "UnnamedRelation")
            )
            if not before_relation:
                continue

            before_relation_copy = Relation(
                before_relation.header, before_relation.set_of_tuples.copy()
            )
            for _ in range(len(dependencies)):
                new_relation = before_relation_copy
                for predicate in getattr(rule, "body", []):
                    predicate_name = getattr(predicate, "name", None)
                    if predicate_name is None:
                        continue
                    body_relation = self.relations.get(predicate_name)
                    if not body_relation:
                        continue
                    new_relation = new_relation.join(body_relation)
                    new_relation = new_relation.project(
                        getattr(rule.head, "values", [])
                    )
                yield (before_relation_copy, rule, new_relation)
                if before_relation_copy == new_relation:
                    break
                before_relation_copy = new_relation

    def get_rule_dependency_graph(self) -> dict[str, list[str]]:
        """Return the rule dependency graph.

        Computes and returns the graph formed by dependencies between rules.
        The graph is used to compute strongly connected components of rules
        for optimized rule evaluation.

        Rules are zero-indexed so the first rule in the Datalog program is `R0`,
        the second rules is `R1`, etc. A return of `{R0 : [R0, R1], R1 : [R2]}`
        means that `R0` has edges to `R0` and `R1`, and `R1` has an edge to `R2`.

        Returns:
            out: A map with an entry for each rule and the associated rules connected to it.
        """
        dependency_graph = {}
        for idx, rule in enumerate(self.datalog.rules):
            rule_name = f"R{idx}"
            dependencies = [
                f"R{i}"
                for i, other_rule in enumerate(self.datalog.rules)
                if any(
                    getattr(pred, "name", None) == getattr(rule.head, "name", None)
                    for pred in getattr(other_rule, "body", [])
                )
            ]
            dependency_graph[rule_name] = dependencies
        return dependency_graph


def load_datalog_program() -> DatalogProgram:
    schemes = [
        Predicate(
            "snap",
            [
                Parameter.id("S"),
                Parameter.id("N"),
                Parameter.id("A"),
                Parameter.id("P"),
            ],
        ),
        Predicate("csg", [Parameter.id("C"), Parameter.id("S"), Parameter.id("G")]),
        Predicate("cp", [Parameter.id("C"), Parameter.id("Q")]),
        Predicate("cdh", [Parameter.id("C"), Parameter.id("D"), Parameter.id("H")]),
        Predicate("cr", [Parameter.id("C"), Parameter.id("R")]),
    ]
    facts = [
        Predicate(
            "snap",
            [
                Parameter.string("1234"),
                Parameter.string("Charley"),
                Parameter.string("Apple St"),
                Parameter.string("555-1234"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter.string("CS101"),
                Parameter.string("1234"),
                Parameter.string("A"),
            ],
        ),
        Predicate("cp", [Parameter.string("CS101"), Parameter.string("CS100")]),
        Predicate(
            "cdh",
            [
                Parameter.string("EE200"),
                Parameter.string("Tu"),
                Parameter.string("10AM"),
            ],
        ),
        Predicate("cr", [Parameter.string("CS101"), Parameter.string("Turing Aud.")]),
    ]
    queries = [
        Predicate(
            "snap",
            [
                Parameter.id("S"),
                Parameter.id("N"),
                Parameter.id("A"),
                Parameter.id("P"),
            ],
        ),
        Predicate("csg", [Parameter.id("C"), Parameter.id("S"), Parameter.id("G")]),
        Predicate("cp", [Parameter.id("C"), Parameter.id("Q")]),
    ]

    rules: list[Rule] = []

    return DatalogProgram(schemes, facts, rules, queries)


if __name__ == "__main__":

    def main() -> None:
        datalog_program = load_datalog_program()
        interpreter = Interpreter(datalog_program)
        interpreter.eval_schemes()
        interpreter.eval_facts()
        results = list(interpreter.eval_queries())
        for query, result in results:
            print(f"Query: {query.name}, Result: {result}")

    main()
