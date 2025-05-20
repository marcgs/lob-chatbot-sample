from typing import Any
from evaluation.chatbot.evaluators.evaluator import Evaluator, EvaluatorResult
from evaluation.chatbot.models import FunctionCall


# Ignore certain type checks as the Azure AI Evaluation SDK does not support Python complex types
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownParameterType=false, reportMissingTypeArgument=false
class FunctionCallEvaluator(Evaluator):
    """
    An evaluator to calculate function call precision.

    Precision = Number of correct function_calls / Actual number of function_calls

    """

    def __init__(self):
        super().__init__()

    def __call__(self, *, actual_function_calls: dict, expected_function_calls: dict, **kwargs: Any) -> EvaluatorResult:
        # Convert the function calls to FunctionCall objects
        actual = [FunctionCall.from_dict(f) for f in actual_function_calls]
        expected = [FunctionCall.from_dict(f) for f in expected_function_calls]
        return EvaluatorResult(
            score=self.evaluate(actual, expected)
        )
    
    def evaluate(
        self, actual_function_calls: list[FunctionCall], expected_function_calls: list[FunctionCall]
    ) -> float:
        raise NotImplementedError("Subclasses should implement this method.")