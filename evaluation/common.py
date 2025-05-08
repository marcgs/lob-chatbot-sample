from datetime import datetime
import json
import os
from pathlib import Path


def convert_json_to_jsonl(filePath: str) -> str:
    """
    Convert the JSON file to JSONL format

    Args:
        filePath (str): path to the JSON file
    Returns:
        str: path to the JSONL file
    """

    print(f"Converting JSON to JSONL: {filePath}")

    outputPath = filePath.replace(".json", ".jsonl")
    with open(filePath, encoding="utf-8") as inputFile:
        with open(outputPath, "w", encoding="utf-8") as outputFile:
            json_data = json.load(inputFile)
            for entry in json_data:
                json.dump(entry, outputFile)
                outputFile.write("\n")

    return outputPath


def save_to_file(data: list[dict], output_dir: str):
    """
    Save content to a file
    Args:
        data (list[dict]): data to save
        experiment_name (str): name of the experiment
    """

    # file_dir = f"{root_path()}/evaluation/output/{experiment_name}"
    file_path = f"{output_dir}/evaluation_results.json"
    os.makedirs(output_dir, exist_ok=True)
    with open(file_path, "w+") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))

    for result in data:
        del result["rows"]

    with open(f"{output_dir}/evaluation_metrics.json", "w+") as f:
        f.write(json.dumps(data, indent=2))


def generate_experiment_name(name: str = "Eval") -> str:
    """
    Generate a unique experiment name

    Args:
        description (str): description of the experiment

    Returns:
        str: unique experiment name
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    return f"{name}_{timestamp}"
