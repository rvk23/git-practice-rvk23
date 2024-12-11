"""Parser for Datalog programs.

Provides the parser and error interface for when parsing fails for Datalog
programs.
"""

from typing import Iterator
from project3.token import Token, TokenType
from project3.datalogprogram import DatalogProgram, Predicate, Parameter, Rule


class UnexpectedTokenException(Exception):
    """Class for parsing errors.

    A parse error is when the actual token does not have the correct type
    according to the state of the parser. In other words, the parser is
    expecting a specific token type but the actual token at that point does
    not match the expected type.

    Attributes:
        expected_type (TokenType): The type that was expected in the parse.
        token (Token): The actual token that was encountered.
    """

    __slots__ = ["expected_type", "token"]

    def __init__(
        self,
        expected_type: TokenType,
        token: Token,
        message: str = "A parse error occurred due to an unexpected token",
    ) -> None:
        super().__init__(message)
        self.expected_type = expected_type
        self.token = token


class TokenStream:
    """Class for managing the token iterator from the lexer.

    A `TokenStream` is a wrapper for the `Iterator[Token]` from the lexer that
    provides core functions for parsing -- `match` and `advance` -- along with an
    additional function for checking if the current token has a type that
    belongs to a set of types -- useful for checking FIRST and FOLLOW sets -- and
    a way to get the value from the current token.

    Attributes:
        token_iterator (Iterator[Token]): A token iterator.
        token (Token): The current token.
    """

    __slots__ = ["token", "_token_iterator"]

    def __init__(self, token_iterator: Iterator[Token]) -> None:
        self._token_iterator = token_iterator
        self.advance()

    def __repr__(self) -> str:
        return f"TokenStream(token={self.token!r}, _token_iterator={self._token_iterator!r})"

    def advance(self) -> None:
        """Advances the iterator and updates the token.

        The last token in the iterator is stuttered meaning that it is repeated
        on every subsequent call.

        **WARNING**: `advance` side-effects the `token` and `token_iterator`.
        This side-effect means that the previous token is gone and cannot be
        recovered. There is no deep-copy for a `TokenStream`, so it's a _use
        once_ object. That is fine for parsing.
        """
        try:
            while True:
                self.token = next(self._token_iterator)
                if self.token.token_type != "COMMENT":
                    break
        except StopIteration:
            pass

    def match(self, expected_type: TokenType) -> None:
        """Return if token matches expected type.

        `match` returns iff the expected type matches the current token. If
        ever the token type does not match the expected type, it raises an exception
        indicating a match failure. The exception includes the expected token
        type and the token that did not match.

        Args:
            expected_type (TokenType): The expected token type in the stream for a successful match.

        Raises:
            error (UnexpectedTokenException): Error if the type of the current token does not match.
        """
        if self.token.token_type != expected_type:
            raise UnexpectedTokenException(expected_type, self.token)

    def member_of(self, token_types: set[TokenType]) -> bool:
        """Returns true iff the current token type is in the specified type.

        `member_of` is a way to determine if the type of the current token is
        in a set of token types. It is especially useful for checking membership
        in FIRST and FOLLOW sets when implementing a table-driven parser.
        The FIRST and FOLLOW sets are used to determine which alternative to use
        in a grammar rule with alternatives.

        Args:
            token_types: A set of token types.

        Returns:
            out: True iff the current token type is in the set of token types.
        """
        return self.token.token_type in token_types

    def value(self) -> str:
        """Return the value attribute of the current token."""
        return self.token.value


def match_and_advance(token: TokenStream, expected_type: TokenType) -> None:
    while token.token.token_type == "COMMENT":
        token.advance()

    token.match(expected_type)
    token.advance()


def datalog_program(token: TokenStream) -> DatalogProgram:
    """Top-level grammar rule for a Datalog program.

    The function directly matches its associated grammar rule by matching
    on keywords and collecting returns from other non-terminal rules to
    build an instance of a `DatalogProgram`.

    Args:
        token (TokenStream]): A token stream.

    Returns:
        program (DatalogProgram): The Datalog program from the parse.
    """

    program = DatalogProgram()

    program.clear_state()

    # Schemes
    match_and_advance(token, "SCHEMES")
    match_and_advance(token, "COLON")
    program.add_scheme(scheme(token))
    program.schemes.extend(scheme_list(token))

    # Facts
    match_and_advance(token, "FACTS")
    match_and_advance(token, "COLON")
    program.facts.extend(fact_list(token))

    # Rules
    match_and_advance(token, "RULES")
    match_and_advance(token, "COLON")
    program.rules.extend(rule_list(token))

    # Queries
    match_and_advance(token, "QUERIES")
    match_and_advance(token, "COLON")
    program.add_query(query(token))
    program.queries.extend(query_list(token))

    program._initialize_domain()

    # Check for EOF
    token.match("EOF")
    return program


def scheme(token: TokenStream) -> Predicate:
    name = token.value()
    match_and_advance(token, "ID")
    match_and_advance(token, "LEFT_PAREN")

    parameters = [Parameter.id(token.value())]
    match_and_advance(token, "ID")

    parameters.extend(id_list(token))

    match_and_advance(token, "RIGHT_PAREN")
    return Predicate(name, parameters)


def head_predicate(token: TokenStream) -> Predicate:
    name = token.value()
    token.match("ID")
    token.advance()

    token.match("LEFT_PAREN")
    token.advance()

    parameters = [Parameter.id(token.value())]
    token.match("ID")
    token.advance()

    parameters.extend(id_list(token))

    token.match("RIGHT_PAREN")
    token.advance()

    return Predicate(name, parameters)


def scheme_list(token: TokenStream) -> list[Predicate]:
    schemes = []
    while token.token.token_type == "ID":
        schemes.append(scheme(token))
    return schemes


def fact_list(token: TokenStream) -> list[Predicate]:
    facts = []
    while token.token.token_type == "ID":
        facts.append(fact(token))
    return facts


def id_list(token: TokenStream) -> list[Parameter]:
    ids = []
    while token.token.token_type == "COMMA":
        token.advance()
        value = token.value()
        token.match("ID")
        token.advance()
        ids.append(Parameter.id(value))
    return ids


def string_list(token: TokenStream) -> list[Parameter]:
    strings = []
    while token.token.token_type == "COMMA":
        token.advance()
        value = token.value()
        token.match("STRING")
        token.advance()
        strings.append(Parameter.string(value))
    return strings


def fact(token: TokenStream) -> Predicate:
    name = token.value()
    match_and_advance(token, "ID")
    match_and_advance(token, "LEFT_PAREN")
    parameters = [Parameter.string(token.value())]
    match_and_advance(token, "STRING")
    parameters.extend(string_list(token))
    match_and_advance(token, "RIGHT_PAREN")
    match_and_advance(token, "PERIOD")
    return Predicate(name, parameters)


def rule_list(token: TokenStream) -> list[Rule]:
    rules = []
    while token.token.token_type == "ID":
        rules.append(rule(token))
    return rules


def parameter(token: TokenStream) -> Parameter:
    """Parse a parameter from the token stream.

    A parameter can either be an ID or a STRING.
    """
    if token.token.token_type == "STRING":
        value = token.value()
        token.match("STRING")
        token.advance()
        return Parameter.string(value)
    elif token.token.token_type == "ID":
        value = token.value()
        token.match("ID")
        token.advance()
        return Parameter.id(value)
    else:
        raise UnexpectedTokenException("ID", token.token)


def parameter_list(token: TokenStream) -> list[Parameter]:
    """Parse a list of parameters separated by commas.

    The function handles parameters of type ID or STRING.
    """
    parameters = []
    while token.token.token_type == "COMMA":
        token.advance()
        parameters.append(parameter(token))
    return parameters


def predicate(token: TokenStream) -> Predicate:
    """Parse a predicate."""
    name = token.value()
    token.match("ID")
    token.advance()

    token.match("LEFT_PAREN")
    token.advance()

    parameters = [parameter(token)]
    parameters.extend(parameter_list(token))

    token.match("RIGHT_PAREN")
    token.advance()

    return Predicate(name, parameters)


def predicate_list(token: TokenStream) -> list[Predicate]:
    """Parse a list of predicates separated by commas.

    This function collects predicates for rules or other structures
    where multiple predicates may appear.
    """
    predicates = []
    while token.token.token_type == "COMMA":
        token.advance()
        predicates.append(predicate(token))
    return predicates


def rule(token: TokenStream) -> Rule:
    """Parse a rule."""
    head = head_predicate(token)

    token.match("COLON_DASH")
    token.advance()

    predicates = [predicate(token)]
    predicates.extend(predicate_list(token))

    token.match("PERIOD")
    token.advance()

    return Rule(head, predicates)


def query_list(token: TokenStream) -> list[Predicate]:
    """Parse a list of queries."""
    queries = []
    while token.token.token_type == "ID":
        queries.append(query(token))
    return queries


def query(token: TokenStream) -> Predicate:
    """Parse a query."""
    pred = predicate(token)
    match_and_advance(token, "Q_MARK")
    return pred


def parse(token_iterator: Iterator[Token]) -> DatalogProgram:
    """Parse a datalog program."""
    token = TokenStream(token_iterator)
    return datalog_program(token)
