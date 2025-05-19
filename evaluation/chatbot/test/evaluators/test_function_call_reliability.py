import pytest
from evaluation.chatbot.evaluators.function_call_reliability import (
    FunctionCallReliabilityEvaluator,
)
from evaluation.chatbot.test.evaluators.test_data import (
    FC_TICKET_CREATE,
    FC_TICKET_CREATE_2,
    # FC_TICKET_CREATE_2_DIFF_ARGS is not used
)


def __call_evaluator(actual: list[dict], expected: list[dict], expected_score: float):
    evaluator = FunctionCallReliabilityEvaluator()
    result = evaluator(actual_function_calls=actual, expected_function_calls=expected)
    assert result.score == expected_score


@pytest.mark.parametrize(
    "actual, expected, expected_score",
    [
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE],
            1.0,  # perfect precision and recall
        ),
        (
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            [FC_TICKET_CREATE],
            0.0,  # precision not 1
        ),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            0.0,  # recall not 1
        ),
    ],
)
def test_function_call_reliability(actual, expected, expected_score):
    __call_evaluator(actual=actual, expected=expected, expected_score=expected_score)
