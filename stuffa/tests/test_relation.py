# type: ignore
import pytest
from project3.relation import IncompatibleOperandError, Relation


def test_given_empty_relation_when_add_tuple_then_tuple_in_relation():
    # given
    header = ("a", "b", "c")
    relation = Relation(header, set())
    input = ("'1'", "'2'", "'3'")

    # when
    relation.add_tuple(input)

    # then
    assert 1 == len(relation.set_of_tuples)
    assert input in relation.set_of_tuples


def test_given_relation_when_str_then_match_expected():
    # given
    header = ("a", "b", "c")
    set_of_tuples = set([("'1'", "'2'", "'3'"), ("'1'", "'3'", "'5'")])
    relation = Relation(header, set_of_tuples)

    expected = """+-----+-----+-----+
|  a  |  b  |  c  |
+-----+-----+-----+
| '1' | '2' | '3' |
| '1' | '3' | '5' |
+-----+-----+-----+"""

    # when
    answer = str(relation)

    # then
    assert expected == answer


def test_given_relation_and_wrong_size_when_add_tuple_then_exception():
    # given
    relation = Relation(("a", "b", "c"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        relation.add_tuple(("1", "2"))

    # then
    assert (
        "Error: ('1', '2') is not compatible with header ['a', 'b', 'c'] in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_relation_when_add_tuple_then_added():
    # given
    relation = Relation(("a", "b", "c"), set())

    # when
    relation.add_tuple(("1", "2", "3"))

    # then
    assert ("1", "2", "3") in relation.set_of_tuples


def test_given_mismatched_header_and_tuple_when_construct_then_exception():
    # given
    header = ("a", "b", "c")
    set_of_tuples = set([("1", "2")])

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        _ = Relation(header, set_of_tuples)

    # then
    assert (
        "Error: ('1', '2') is not compatible with header ['a', 'b', 'c'] in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_set_that_is_not_over_tuples_when_construct_then_exception():
    # given
    header = "a"
    set_of_tuples = set(["1"])

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        _ = Relation(header, set_of_tuples)

    # then
    assert (
        "Error: 1 is not type compatible with Relation.RelationTuple in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_set_that_is_tuples_but_not_str_when_construct_then_exception():
    # given
    header = ("a", "b")
    set_of_tuples = set([("1", 2)])

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        _ = Relation(header, set_of_tuples)

    # then
    assert (
        "Error: ('1', 2) is not type compatible with Relation.RelationTuple in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_mismatched_relations_when_difference_then_exception():
    # given
    left = Relation(("a", "b", "c"), set())
    right = Relation(("a", "b"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        left.difference(right)

    # then
    assert (
        "Error: headers ['a', 'b', 'c'] and ['a', 'b'] are not compatible in Relation.difference"
        == str(exception.value)
    )


def test_given_matched_relations_when_difference_then_difference():
    # given
    left = Relation(("a", "b", "c"), set([("1", "2", "3"), ("2", "4", "6")]))
    right = Relation(("a", "b", "c"), set([("2", "4", "6")]))
    expected = Relation(("a", "b", "c"), set([("1", "2", "3")]))

    # when
    answer = left.difference(right)

    # then
    assert expected == answer


def test_given_mismatched_relations_when_intersection_then_exception():
    # given
    left = Relation(("a", "b", "c"), set())
    right = Relation(("a", "b"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        left.intersection(right)

    # then
    assert (
        "Error: headers ['a', 'b', 'c'] and ['a', 'b'] are not compatible in Relation.intersection"
        == str(exception.value)
    )


def test_given_matched_relations_when_intersection_then_intersection():
    # given
    left = Relation(("a", "b", "c"), set([("1", "2", "3"), ("2", "4", "6")]))
    right = Relation(("a", "b", "c"), set([("2", "4", "6")]))
    expected = Relation(("a", "b", "c"), set([("2", "4", "6")]))

    # when
    answer = left.intersection(right)

    # then
    assert expected == answer


def test_given_invalid_attribute_in_projection_then_exception():
    # given
    relation = Relation(("a", "b", "c"), set([("1", "2", "3")]))

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        relation.project(["a", "d"])

    # then
    assert "Error: '{'d'}' is not in the header ['a', 'b', 'c']" in str(exception.value)


def test_given_mismatched_header_length_in_rename_then_exception():
    # given
    relation = Relation(("a", "b", "c"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        relation.rename(["x", "y"])

    # then
    assert (
        "Error: Length of new header ['x', 'y'] does not match header ['a', 'b', 'c']"
        in str(exception.value)
    )


def test_given_matching_length_in_rename_then_renamed_relation():
    # given
    relation = Relation(("a", "b", "c"), set([("1", "2", "3")]))
    expected = Relation(("x", "y", "z"), set([("1", "2", "3")]))

    # when
    answer = relation.rename(["x", "y", "z"])

    # then
    assert expected == answer


def test_given_invalid_columns_in_select_eq_col_then_exception():
    # given
    relation = Relation(("a", "b", "c"), set([("1", "2", "3")]))

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        relation.select_eq_col("a", "d")

    # then
    assert "Error: Column 'd' not found in header ['a', 'b', 'c']" in str(
        exception.value
    )


def test_given_valid_columns_in_select_eq_col_then_filtered_relation():
    # given
    relation = Relation(("a", "b", "c"), set([("1", "2", "2"), ("3", "4", "5")]))
    expected = Relation(("a", "b", "c"), set([("1", "2", "2")]))

    # when
    answer = relation.select_eq_col("b", "c")

    # then
    assert expected == answer


def test_given_invalid_column_in_select_eq_lit_then_exception():
    # given
    relation = Relation(("a", "b", "c"), set([("1", "2", "3")]))

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        relation.select_eq_lit("d", "3")

    # then
    assert "Error: Column 'd' not found in header ['a', 'b', 'c']" in str(
        exception.value
    )


def test_given_valid_column_in_select_eq_lit_then_filtered_relation():
    # given
    relation = Relation(("a", "b", "c"), set([("1", "2", "3"), ("4", "5", "3")]))
    expected = Relation(("a", "b", "c"), set([("1", "2", "3")]))

    # when
    answer = relation.select_eq_lit("a", "1")

    # then
    assert expected == answer


def test_given_mismatched_headers_in_union_then_exception():
    # given
    left = Relation(("a", "b", "c"), set())
    right = Relation(("a", "b"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        left.union(right)

    # then
    assert (
        "Error: headers ['a', 'b', 'c'] and ['a', 'b'] are not compatible in Relation.union"
        == str(exception.value)
    )


def test_given_matched_relations_when_union_then_union_of_relations():
    # given
    left = Relation(("a", "b", "c"), set([("1", "2", "3")]))
    right = Relation(("a", "b", "c"), set([("4", "5", "6")]))
    expected = Relation(("a", "b", "c"), set([("1", "2", "3"), ("4", "5", "6")]))

    # when
    answer = left.union(right)

    # then
    assert expected == answer
