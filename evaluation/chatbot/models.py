from dataclasses import dataclass
import json
from typing import Any

from semantic_kernel.contents.function_call_content import FunctionCallContent


@dataclass
class FunctionCall:
    functionName: str
    arguments: dict[str, str]

    @staticmethod
    def from_FunctionCallContent(source: FunctionCallContent) -> "FunctionCall":
        """
        Converts a FunctionCallContent object to a FunctionCall object.
        """
        args = json.loads(source.arguments) if isinstance(source.arguments, str) else source.arguments
        
        return FunctionCall(
            functionName=source.name or source.function_name, # name attribute includes plugin name plus function name. If available, use it.
            arguments=args, # pyright: ignore [reportArgumentType]
        )
    
    # Ignore certain type checks as the Azure AI Evaluation SDK does not support Python complex types
    
    @staticmethod
    def from_dict(source: dict) -> "FunctionCall": # pyright: ignore [reportUnknownParameterType, reportMissingTypeArgument] As required by the Azure AI Evaluation SDK
        """
        Converts a dictionary to a FunctionCall object.
        """
        return FunctionCall(
            functionName=source["functionName"], # pyright: ignore [reportUnknownArgumentType] As required by the Azure AI Evaluation SDK
            arguments=source["arguments"], # pyright: ignore [reportUnknownArgumentType] As required by the Azure AI Evaluation SDK
        )
    
    def to_dict(self) -> dict[str, Any]:
        """
        Converts the FunctionCall object to a dictionary.
        """
        return {
            "functionName": self.functionName,
            "arguments": self.arguments,
        }
