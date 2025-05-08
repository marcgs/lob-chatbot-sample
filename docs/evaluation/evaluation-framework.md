# Line-of-Business Chatbot Evaluation Framework

## Introduction

This document provides a comprehensive guide to the evaluation framework used in this Line-of-Business (LOB) chatbot sample. The framework is designed specifically to address the unique challenges of evaluating LLM-powered, function-calling chatbots in business contexts where traditional chatbot evaluation approaches fall short.

## Evaluation Challenges for LOB Chatbots

Traditional evaluation methods are inadequate for LLM-powered business chatbots because they:

1. **Don't capture function call quality** - Standard metrics like BLEU or ROUGE don't measure how accurately a chatbot calls business functions
2. **Miss conversation complexity** - Multi-turn conversations with specific business workflows are difficult to evaluate with generic metrics
3. **Lack business process adherence measures** - Most evaluation frameworks don't assess if chatbots follow prescribed business processes
4. **Can't assess reliability across similar inputs** - Consistency of function calling behavior isn't captured by content-focused metrics

## Framework Architecture

### Core Components

1. **EvaluationService** (`evaluation/evaluation_service.py`)
   - Central coordinator for the evaluation process
   - Loads ground truth data
   - Executes evaluations against target chatbots
   - Aggregates and stores results

2. **Evaluation Target** (`evaluation/chatbot/eval_target.py`)
   - Implements the chatbot behavior to be evaluated
   - Simulates conversations based on ground truth data
   - Returns function calls made during conversations

3. **Specialized Evaluators** (`evaluation/chatbot/evaluators/`)
   - Implements various metrics for chatbot evaluation
   - Each evaluator focuses on a specific aspect of chatbot performance

4. **Ground Truth Datasets** (`evaluation/chatbot/ground-truth/`)
   - Contains expected conversations and function calls
   - Structured in JSON/JSONL format
   - Annotated with expected behaviors and outcomes

### Key Metrics

The framework focuses on five core metrics that are particularly relevant for function-calling business chatbots:

1. **Function Call Precision (`FunctionCallPrecisionEvaluator`)**
   - Measures whether the chatbot calls the right functions at the right time
   - Formula: `Correct function calls / Total function calls made`
   - High precision indicates the chatbot doesn't make unnecessary function calls

2. **Function Call Recall (`FunctionCallRecallEvaluator`)**
   - Measures whether the chatbot makes all necessary function calls
   - Formula: `Correct function calls / Expected function calls`
   - High recall indicates the chatbot doesn't miss required function calls

3. **Function Call Arguments Precision (`FunctionCallArgsPrecisionEvaluator`)**
   - Measures if the arguments in function calls are correct
   - Formula: `Correctly provided arguments / Total arguments provided`
   - High precision indicates the chatbot includes the right parameters in function calls

4. **Function Call Arguments Recall (`FunctionCallArgsRecallEvaluator`)**
   - Measures if all necessary arguments are included in function calls
   - Formula: `Correct arguments provided / Expected arguments`
   - High recall indicates the chatbot doesn't miss required parameters

5. **Function Call Reliability (`FunctionCallReliabilityEvaluator`)**
   - Measures overall success in completing business processes
   - Requires both perfect precision and recall to achieve a score of 1.0
   - Indicates how often a complete business process is successfully executed

## Ground Truth Dataset Structure

The ground truth datasets are stored in JSON/JSONL format and contain:

```json
{
  "id": "conversation_id",
  "description": "Description of the conversation scenario",
  "scenarioType": "create_ticket_and_action_item",
  "task_completion_condition": "The user has confirmed the end of the session",
  "instructions": "Instructions for the simulated user",
  "expected_function_calls": [
    {
      "functionName": "TicketManagementPlugin-create_support_ticket",
      "arguments": {
        "title": "Server performance degradation",
        "department_code": "IT",
        "priority": "Critical",
        "workflow_type": "Expedited",
        "description": "Main application server is experiencing significant performance degradation",
        "expected_outcome": "Server performance restored to normal levels"
      }
    },
    {
      "functionName": "ActionItemPlugin-create_action_item",
      "arguments": {
        "ticket_id": "TKT-*",
        "title": "Increase server memory allocation",
        "assigned_to": "John Smith",
        "description": "Allocate additional memory resources to the main application server",
        "due_date": "2025-05-10"
      }
    }
  ]
}
```

Each conversation in the ground truth dataset includes:

- **Conversation ID and description**: Metadata about the conversation
- **Scenario type**: The business scenario being tested
- **Task completion condition**: When the conversation is considered complete
- **Instructions**: Guidance for the simulated user
- **Expected function calls**: The functions the chatbot should call with expected arguments

## Evaluation Process

The evaluation process follows these key steps:

1. **Setup**: The evaluation framework loads ground truth data and initializes evaluators.

2. **Execution**: For each conversation in the ground truth dataset:
   - A simulated conversation takes place through the `SupportTicketChatSimulator`
   - The chatbot responds to user inputs and makes function calls
   - Function calls are recorded along with their arguments

3. **Comparison and Measurement**: For each conversation:
   - Actual function calls are compared with expected function calls
   - The matching algorithm compares function names (case-insensitive) and arguments
   - Special functions like `CommonPlugin-ask_clarification` are ignored in the evaluation
   - Metrics are calculated for precision, recall, and reliability

4. **Result Aggregation**: Results are aggregated across all conversations and stored in:
   - JSON format for detailed analysis
   - Summarized metrics for overall performance assessment

5. **Analysis and Visualization**: Results can be analyzed using:
   - Evaluation notebook (`evaluation/chatbot/evaluation.ipynb`)
   - Error analysis notebook (`evaluation/chatbot/error_analysis_chatbot.ipynb`)

## Running Evaluations

To run evaluations on the chatbot:

1. **Using Command Line**:

   ```bash
   make chatbot-eval
   ```

2. **View Results**: Evaluation results are stored in:

   ```bash
   evaluation/chatbot/output/{experiment_name}/evaluation_results.json
   ```

## Interpreting Results

Evaluation results provide insights into:

1. **Function Call Quality**
   - **High precision, low recall**: Chatbot makes correct function calls but misses some required calls
   - **Low precision, high recall**: Chatbot makes unnecessary function calls while covering expected ones
   - **Low precision, low recall**: Chatbot has fundamental issues with function call understanding

2. **Parameter Accuracy**
   - **High argument precision, low recall**: Parameters provided are correct but incomplete
   - **Low argument precision, high recall**: All expected parameters are provided, but with incorrect values
   - **Low argument precision, low recall**: Significant parameter issues in function calls

3. **Business Process Adherence**
   - **High reliability across scenarios**: Chatbot correctly follows business processes
   - **Variable reliability across scenarios**: Chatbot may be better at certain workflows than others
   - **Consistently low reliability**: Fundamental issues with business process execution

4. **Specific Function Analysis**
   - Analyzing which functions have lowest precision/recall helps prioritize improvements
   - Patterns in parameter errors can guide targeted improvements

## Extending the Framework

The evaluation framework is designed to be extensible in multiple ways:

1. **Creating Custom Evaluators**:

   ```python
   from evaluation.chatbot.evaluators.evaluator import Evaluator
   
   class CustomEvaluator(Evaluator):
       """A custom evaluator that measures a specific aspect of chatbot performance."""
       
       def __call__(self, *, actual_function_calls, expected_function_calls, **kwargs):
           score = self.evaluate(actual_function_calls, expected_function_calls)
           return EvaluatorResult(score=score)
           
       def evaluate(self, actual_function_calls, expected_function_calls):
           # Custom evaluation logic
           return score
   ```

2. **Adding New Ground Truth Datasets**:
   - Create a new JSON file in `evaluation/chatbot/ground-truth/`
   - Follow the existing format structure
   - Include diverse scenarios for comprehensive evaluation

3. **Adding New Metrics**:
   - Implement new evaluators for domain-specific requirements
   - Register them in the evaluation service

## Best Practices

1. **Regular Evaluation**: Run evaluations after significant changes to the chatbot to track improvements or regressions.

2. **Comprehensive Scenario Coverage**: Ensure ground truth data covers a diverse range of business scenarios and edge cases.

3. **Balanced Metric Analysis**: Consider all evaluation metrics together rather than optimizing for just one.

4. **Targeted Improvements**: Focus improvements on specific function calls or parameters with lowest scores.

5. **Iterative Refinement**: Use evaluation results to guide iterative improvements to chatbot implementation.

## Conclusion

This evaluation framework provides a structured approach to measuring and improving function-calling chatbot performance in business contexts. By focusing on function call accuracy and business process adherence, it enables the development of reliable and effective line-of-business chatbots.
