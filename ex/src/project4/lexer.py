"""Turn a input string into a stream of tokens with lexical analysis.

The `lexer(input_string: str)` function is the entry point. It generates a
stream of tokens from the `input_string`.

Examples:

    >>> from project4.lexer import lexer
    >>> input_string = ":\\n  \\n:"
    >>> for i in lexer(input_string):
    ...     print(i)
    ...
    (COLON,":",1)
    (COLON,":",3)
    (EOF,"",3)
"""

from typing import Iterator

from project4.token import Token, TokenType
from project4.fsm import FiniteStateMachine, Colon, Eof, WhiteSpace


def lexer(input_string: str) -> Iterator[Token]:
    """Produce a stream of tokens from a given input string.

    Pseudo-code:

    ```
    fsms: list[FiniteStateMachine] = [Colon(), Eof(), WhiteSpace()]
    hidden: list[TokenType] = ["WHITESPACE"]
    line_num: int = 1
    token: Token = Token.undefined("")
    while not _is_last_token(token):
        token = _get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + _get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type in hidden:
            continue
        yield token
    ```

    The `_get_token` function should return the token from the FSM that reads
    the most characters. In the case of two FSMs reading the same number of
    characters, the one that comes first in the list of FSMs, `fsms`, wins.
    Some care must be given to determining when the _last_ token has been
    generated and how to update the new `line_num` for the next token.

    Args:
        input_string: Input string for token generation.

    Yields:
        token: The current token resulting from the string.
    """
    fsms: list[FiniteStateMachine] = [Colon(), Eof(), WhiteSpace()]
    hidden: list[TokenType] = ["WHITESPACE"]

    # TODO: remove the `print` statements since they are only here for ruff
    print(fsms)
    print(hidden)

    raise NotImplementedError
