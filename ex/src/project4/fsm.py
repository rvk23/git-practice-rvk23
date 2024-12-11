"""Finite State Machine (FSM) abstraction.

The finite state machine (FSM) is abstracted by the `FiniteStateMachine` class.
The function `run_fsm(fsm, input_string)` runs the indicated `fsm` until it
accepts or rejects to return the resulting characters read and token.
"""

from typing import Callable
from project4.token import Token


State = Callable[[int, str], "StateAndOutput"]
"""
`State` is a function that takes two inputs and returns a new state with the
new output. The `int` input is the number of characters read. The `str`
input is the character to read. The output is the new state and the new
number of characters read.
"""
StateAndOutput = tuple[State, int]
"""
The `State` is the new state resulting from the input while the `int` is the
new output resulting from the input.
"""


def run_fsm(fsm: "FiniteStateMachine", input_string: str) -> tuple[int, Token]:
    """Run an FSM and return the number of characters read with the token.

    Run the passed in FSM until it accepts or rejects. The output is captured
    on each state transition and passed as input with the next character. It returns
    the number or character read and the resulting token.

    Args:

        fsm: the FSM to run
        input_string: the string to use as input

    Returns:

        (output_num_chars_read, token): the number of characters read from the input and the associated token produced by the FSM as a tuple

    Examples:

        >>> from project4.fsm import run_fsm, Colon
        >>> colon = Colon()
        >>> input_string = ": a"
        >>> number_chars_read, token = run_fsm(colon, input_string)
        >>> "number_chars_read = {} token = {}".format(number_chars_read, str(token))
        'number_chars_read = 1 token = (COLON,":",0)'
    """
    current_state: State = fsm.initial_state
    next_state: State

    output_num_chars_read: int = 0

    input_num_chars_read: int = 0
    input_char: str = ""

    number_of_chars = len(input_string)
    for i in range(0, number_of_chars + 1):
        input_num_chars_read = output_num_chars_read
        input_char = input_string[i] if i < number_of_chars else ""

        next_state, output_num_chars_read = current_state(
            input_num_chars_read, input_char
        )
        if next_state in {
            FiniteStateMachine.s_accept,
            FiniteStateMachine.s_reject,
        }:
            break

        current_state = next_state

    value = input_string[:output_num_chars_read]
    return (output_num_chars_read, fsm.token(value))


class FiniteStateMachine:
    """Base class for the finite state machine (FSM) abstraction.

    The base class defines the accept and reject states. The reject state
    will always return zero characters read. Once accept/reject, then always
    accept/reject. The output does not change once in these states. The
    `token` function should be overridden in each subclass.

    Attributes:
        initial_state (State): The initial state for this FSM.
    """

    __slots__ = ["initial_state"]

    def __init__(self, initial_state: State) -> None:
        """Initialize the FSM with its initial state

        Args:
            initial_state: The initial state for this FSM.
        """
        self.initial_state = initial_state

    def token(self, value: str) -> Token:
        """Return the token produced by this FSM

        NOTE: this method must be overridden in any subclass as it defaults to UNDEFINED

        Args:
            value: The value associated with this `Token`.

        Returns:
            Token.undefined: The method must be overridden in subclasses.
        """
        return Token.undefined(value)

    @staticmethod
    def s_accept(input_chars_read: int, input_char: str) -> StateAndOutput:
        """Accept sync state -- once accept always accept."""
        return FiniteStateMachine.s_accept, input_chars_read

    @staticmethod
    def s_reject(input_chars_read: int, input_char: str) -> StateAndOutput:
        """Reject sync state -- once reject always reject."""
        return FiniteStateMachine.s_reject, input_chars_read


class Colon(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Colon.s_0)

    def token(self, value: str) -> Token:
        """Create a token of type COLON.

        NOTE: the match statement is for mypy as it ensures that mypy is able to statically
        prove that `value` is ":" when calling `Token.colon(value)`. Follow the pattern for
        other keyword FSMs.

        Args:
            value: The characters read by the FSM.

        Returns:
            Token.colon: iff what is read is a ":" otherwise Token.undefined -- both use `value` for the token.
        """
        match value:
            case ":":
                return Token.colon(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == ":":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Eof(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Eof.s_0)

    def token(self, value: str) -> Token:
        match value:
            case "":
                return Token.eof(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class WhiteSpace(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(WhiteSpace.s_0)

    def token(self, value: str) -> Token:
        return Token.whitespace(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char in [" ", "\t", "\r", "\n"]:
            return WhiteSpace.s_0, input_chars_read + 1
        elif input_chars_read > 0:
            return FiniteStateMachine.s_accept, input_chars_read
        else:
            return FiniteStateMachine.s_reject, 0
