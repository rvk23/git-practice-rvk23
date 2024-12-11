"""Representation for a Datalog program.

The module includes abstractions for the Parameter, Predicate, Rule,
and a DatalogProgram.
"""

from typing import Any, Literal, Set


ParameterType = Literal["ID", "STRING"]
"""
Parameters can be either an ID naming a part of a relation or a string naming
a literal value.
"""


class Parameter:
    """Parameter class for all predicates.

    There are two types of parameters: ID and STRING. These correspond to their
    token counterparts.

    Attributes:
        value (str): The actual text for the parameter taken from the associated token.
        parameter_type (ParameterType): The type of the parameter: ID or STRING.
    """

    __slots__ = ["value", "parameter_type"]

    def __init__(self, value: str, parameter_type: ParameterType) -> None:
        self.value = value
        self.parameter_type = parameter_type

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Parameter):
            return False
        return (self.parameter_type == other.parameter_type) and (
            self.value == other.value
        )

    def __repr__(self) -> str:
        return (
            f"Parameter(value={self.value!r}, parameter_type={self.parameter_type!r})"
        )

    def is_id(self) -> bool:
        """True iff it is an ID parameter."""
        return "ID" == self.parameter_type

    def is_string(self) -> bool:
        """True iff it is a STRING parameter."""
        return "STRING" == self.parameter_type

    @staticmethod
    def id(value: str) -> "Parameter":
        """Create an ID parameter with value."""
        return Parameter(value, "ID")

    @staticmethod
    def string(value: str) -> "Parameter":
        """Create a STRING parameter with value."""
        return Parameter(value, "STRING")


class Predicate:
    """Predicate class for all datalog entities.

    The predicate is a general structure that is used for schemes, facts,
    rules, and queries. The only difference is in the type of parameters
    allowed in the predicates where rules and queries allow for
    both the ID and STRING parameters -- the former for parts of a relation
    and the later for literals while schemes only allow for IDs and facts
    only allow for STRINGs.

    Attributes:
        name (str): The name of the predicate.
        parameters (list[Parameter]): The parameter list.
    """

    __slots__ = ["name", "parameters"]

    def __init__(self, name: str, parameters: list[Parameter] = []) -> None:
        self.name = name
        self.parameters = parameters

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Predicate):
            return False
        return (self.name == other.name) and (self.parameters == other.parameters)

    def __repr__(self) -> str:
        return f"Predicate(name={self.name!r}, parameters={self.parameters!r})"

    def __str__(self) -> str:
        parameters: str = ",".join([i.value for i in self.parameters])
        return f"{self.name}({parameters})"

    def add_parameter(self, parameter: Parameter) -> None:
        """Add a parameter to the predicate.

        Helper function if the __init__ doesn't provide parameters or a
        complete parameter list.

        Args:
            parameter: The parameter to add.
        """
        self.parameters.append(parameter)


class Rule:
    """Rule class consisting of a head and list of predicates.

    There are two components to a rule: the head predicate and then a list
    of predicates. The head predicate defines the resulting relation. The list
    of predicates define how tuples are generated for the relation.

    Attributes:
        head (Predicate): The head predicate.
        predicates (list[Predicate]): The list of predicates comprising this rule.
    """

    __slots__ = ["head", "predicates"]

    def __init__(self, head: Predicate, predicates: list[Predicate]) -> None:
        self.head = head
        self.predicates = predicates

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Rule):
            return False
        return (self.head == other.head) and (self.predicates == other.predicates)

    def __repr__(self) -> str:
        return f"Rule(head={self.head!r}, predicates={self.predicates!r})"

    def __str__(self) -> str:
        predicates = ",".join([str(i) for i in self.predicates])
        return f"{str(self.head)} :- {predicates}"


class DatalogProgram:
    """Class for a Datalog program.

    Holds all the schemes, rules, facts, and queries for the program.

    Attributes:
        schemes (list[Predicate]): The list of schemes as predicates.
        facts (list[Predicate]): The list of facts as predicates.
        rules (list[Rule]): The list of rules.
        queries (list[Predicate]): The list of queries.
        domain (set[str]): A set of unique string values from the facts.
    """

    __slots__ = [
        "schemes",
        "facts",
        "rules",
        "queries",
        "domain",
        "include_queries_in_domain",
    ]

    def clear_state(self: "DatalogProgram") -> None:
        self.schemes.clear()
        self.facts.clear()
        self.rules.clear()
        self.queries.clear()
        self.domain.clear()

    def __init__(
        self,
        schemes: list[Predicate] = [],
        facts: list[Predicate] = [],
        rules: list[Rule] = [],
        queries: list[Predicate] = [],
        domain: Set[str] = set(),
        include_queries_in_domain: bool = False,
    ):
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries
        self.domain = domain
        self.include_queries_in_domain = include_queries_in_domain
        self._initialize_domain()

    def _initialize_domain(self) -> None:
        self.domain = set()
        for fact in self.facts:
            self._update_domain(fact)
        if self.include_queries_in_domain:
            for query in self.queries:
                self._update_domain(query)

    def add_fact(self, fact: Predicate) -> None:
        self.facts.append(fact)
        self._update_domain(fact)

    def _update_domain(self, fact: Predicate) -> None:
        for param in fact.parameters:
            if param.is_string():
                cleaned_value = param.value.strip("'").strip()
                if cleaned_value or param.value == "''":
                    self.domain.add(cleaned_value)

    def __str__(self) -> str:
        result = [
            self._section_str("Schemes", self.schemes),
            self._section_str("Facts", self.facts, period=True),
            self._section_str("Rules", self.rules),
            self._section_str("Queries", self.queries, question=True),
        ]

        result.append(self._domain_str())

        return "\n".join(result)

    def _section_str(
        self, title: str, items: list[Any], period: bool = False, question: bool = False
    ) -> str:
        section = [f"{title}({len(items)}):"]
        for item in items:
            line = f"  {item}"
            if period or title == "Rules":
                line += "."
            if question:
                line += "?"
            section.append(line)
        return "\n".join(section)

    def _domain_str(self) -> str:
        sorted_domain = sorted(self.domain)
        domain_section = [f"Domain({len(sorted_domain)}):"]
        domain_section.extend([f"  '{value}'" for value in sorted_domain])
        return "\n".join(domain_section)

    def add_scheme(self, scheme: Predicate) -> None:
        """Add a scheme to the list of schemes."""
        self.schemes.append(scheme)

    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the list of rules."""
        self.rules.append(rule)

    def add_query(self, query: Predicate) -> None:
        """Add a query to the list of queries."""
        self.queries.append(query)
        if self.include_queries_in_domain:
            self._update_domain(query)
