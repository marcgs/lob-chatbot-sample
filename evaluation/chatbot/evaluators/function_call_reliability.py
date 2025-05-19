from evaluation.chatbot.evaluators.function_call_recall import (
    FunctionCallRecallEvaluator, FunctionCallArgsRecallEvaluator
)
from .evaluator import Evaluator, EvaluatorResult


class FunctionCallReliabilityEvaluator(Evaluator):
    """
    Calculate Reliability of function calls.

    Reliability = Precision / Recall

    """

    def __init__(
        self,
    ):
        """Initialize the object of the class."""
        super().__init__()

    def __call__(
        self, *, actual_function_calls: list[dict[str, object]], expected_function_calls: list[dict[str, object]], **kwargs: dict[str, object]
    ) -> EvaluatorResult:
        """
        Private method, that should be used exclusively for evaluation framework purposes.

        Args:
            actual_function_calls (list[dict]): an array of actual function calls done by the LLM model
            expected_function_calls (list[dict]): an array of expected function calls (ground truth)

        Returns:
            Dict: Result of evaluation in the following format: `{reliability: <value>}`
        """

        return EvaluatorResult(
            score=self.evaluate(actual_function_calls, expected_function_calls)
        )

    def evaluate(
        self, actual_function_calls: list[dict[str, object]], expected_function_calls: list[dict[str, object]]
    ) -> float:
        """
        Reliability = if precision == 1 and recall == 1 then return 1 else return 0

        Args:
            actual_function_calls (list[dict]): an array of actual function calls done by the LLM model
            expected_function_calls (list[dict]): an array of expected function calls (ground truth)

        Returns:
            float: task completion reliability score
        """

        scores: list[float] = []
        evaluators = [
            FunctionCallRecallEvaluator(),
            FunctionCallArgsRecallEvaluator(),
        ]
        for evaluator in evaluators:
            scores.append(evaluator.evaluate(actual_function_calls, expected_function_calls))
        
        return sum(scores) / len(scores)
