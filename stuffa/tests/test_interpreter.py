# type: ignore
"""Tests for the Datalog interpreter."""

from project3.interpreter import Interpreter
from project3.datalogprogram import DatalogProgram, Predicate, Rule


class MockDatalogProgram(DatalogProgram):
    def __init__(self, schemes=None, facts=None, queries=None, rules=None):
        self.schemes = schemes or []
        self.facts = facts or []
        self.queries = queries or []
        self.rules = rules or []


class MockPredicate(Predicate):
    def __init__(self, name, values):
        self.name = name
        self.values = values


class MockRule(Rule):
    def __init__(self, head, body):
        self.head = head
        self.body = body


def test_eval_schemes_creates_relations():
    # given
    schemes = [MockPredicate("parent", ["name", "child"])]
    datalog_program = MockDatalogProgram(schemes=schemes)
    interpreter = Interpreter(datalog_program)

    # when
    interpreter.eval_schemes()

    # then
    assert hasattr(interpreter, "relations")
    assert "parent" in interpreter.relations
    assert interpreter.relations["parent"].header == ["name", "child"]


def test_eval_facts_adds_tuples_to_relations():
    # given
    schemes = [MockPredicate("parent", ["name", "child"])]
    facts = [MockPredicate("parent", ["Alice", "Bob"])]
    datalog_program = MockDatalogProgram(schemes=schemes, facts=facts)
    interpreter = Interpreter(datalog_program)
    interpreter.eval_schemes()

    # when
    interpreter.eval_facts()

    # then
    assert ("Alice", "Bob") in interpreter.relations["parent"].set_of_tuples


def test_eval_queries_returns_correct_relations():
    # given
    schemes = [MockPredicate("parent", ["name", "child"])]
    queries = [MockPredicate("parent", ["Alice", "Bob"])]
    datalog_program = MockDatalogProgram(schemes=schemes, queries=queries)
    interpreter = Interpreter(datalog_program)
    interpreter.eval_schemes()
    interpreter.eval_facts()

    # when
    results = list(interpreter.eval_queries())

    # then
    assert len(results) == 1
    query, relation = results[0]
    assert query.name == "parent"
    assert ("Alice", "Bob") in relation.set_of_tuples
