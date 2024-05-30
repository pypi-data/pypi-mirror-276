import json
import os
from typing import List


def read_json_data_file(file_path: str) -> List[dict]:
    """
    Reads JSON data from a file and validates the format.

    Args:
      file_path: The path to the JSON file.

    Returns:
      A list of dictionaries containing the data.

    Raises:
      ValueError: If the JSON format is invalid.
    """
    try:
        data = json.load(open(file_path, "r"))

        if not isinstance(data, list):
            raise ValueError(f"File {file_path} is invalid JSON format. Expected a list.")

        if not isinstance(data[0], dict):
            raise ValueError(
                f"File {file_path} is invalid JSON format. Expected dictionaries in the list."
            )

        if "data" in data[0].keys():
            data = data[0]["data"]
        else:
            raise ValueError(
                f"File {file_path} is invalid JSON format. Expected 'data' column in the dictionary."
            )

    except (FileNotFoundError, json.JSONDecodeError) as exception:
        raise ValueError(f"Error reading JSON file: {exception}") from exception

    return data


def read_train_valid_data(
    data_dir: str,
    text_column: str = "question",
    label_column: str = "math_type",
    valid_set: bool = True,
) -> tuple[List[dict], List[dict]]:
    """
    Reads training and validation data from JSON files in a directory.

    Args:
        data_dir (str): Path to the directory containing JSON data files.
        text_column (str, optional): Name of the column containing text data. Defaults to "question".
        label_column (str, optional): Name of the column containing label data. Defaults to "math_type".
        valid_set (bool, optional): Whether to read validation data. Defaults to True.

    Returns:
        tuple[List[dict], List[dict]]: A tuple containing lists of dictionaries representing training and validation data, respectively.
            Each dictionary has "text" and "label" keys.

    Raises:
        AssertionError: If the data directory is not found.
        ValueError: If no training data is found in the directory.
    """
    assert os.path.isdir(data_dir), f"Data directory '{data_dir}' not found."

    train_data, eval_data = [], []
    for file_name in os.listdir(data_dir):
        if file_name.startswith("train") and file_name.endswith("json"):
            train_data.extend(read_json_data_file(os.path.join(data_dir, file_name)))

        if valid_set and file_name.startswith("eval") and file_name.endswith("json"):
            eval_data.extend(read_json_data_file(os.path.join(data_dir, file_name)))

    if not train_data:
        raise ValueError("No train data found in the directory.")

    train_data = [{"text": item[text_column], "label": item[label_column]} for item in train_data]
    if eval_data:
        eval_data = [
            {"text": item[text_column], "label": item[label_column]} for item in eval_data
        ]

    return train_data, eval_data
