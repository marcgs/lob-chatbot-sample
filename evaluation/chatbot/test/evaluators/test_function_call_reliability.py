import pytest
from evaluation.chatbot.evaluators.function_call_reliability import (
    FunctionCallReliabilityEvaluator,
)
from evaluation.chatbot.test.evaluators.test_data import (
    FC_TICKET_CREATE,
    FC_TICKET_CREATE_2,
    FC_TICKET_CREATE_2_DIFF_ARGS,
    FC_TICKET_CREATE_DIFF_ARGS,
    FC_TICKET_CREATE_DIFF_NAME,
    convert_to_dict,
)


@pytest.mark.parametrize(
    "actual, expected, expected_score",
    [
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE],
            1.0,  # perfect function name and arguments recall
        ),
        (
            [FC_TICKET_CREATE],
            [FC_TICKET_CREATE_DIFF_ARGS],
            0.5,  # argument recall not 1
        ),
        (
            [FC_TICKET_CREATE, FC_TICKET_CREATE_2],
            [FC_TICKET_CREATE_DIFF_NAME, FC_TICKET_CREATE_2_DIFF_ARGS],
            0.25,  # argument recall of second function call is not 1
        ),
    ],
)
def test_function_call_reliability(actual, expected, expected_score):
    evaluator = FunctionCallReliabilityEvaluator()
    result = evaluator(actual_function_calls=convert_to_dict(actual), expected_function_calls=convert_to_dict(expected))
    assert result.score == expected_score
