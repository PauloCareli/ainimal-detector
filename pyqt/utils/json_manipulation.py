import json
import os
from typing import Any, Dict, List, Optional


def load_json(json_file_path: str) -> List[Dict[str, Any]]:
    """
    Load AI model data from a JSON file.

    Parameters:
        json_file_path (str): Path to the JSON file containing AI model data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing AI model data.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        return data
    except:
        return {}


def save_ai_models_to_json(data: List[Dict[str, Any]], json_file_path: Optional[str] = None) -> None:
    """
    Save AI model data to a JSON file.

    Parameters:
        data (List[Dict[str, Any]]): List of dictionaries representing AI model data.
        json_file_path (str, optional): Path to the JSON file to save the data.
            If not specified (None), defaults to 'ai_models.json' in the project root directory.

    Returns:
        None
    """
    if json_file_path is None:
        # Default to the root of the project directory
        json_file_path = os.path.join(os.getcwd(), 'pyqt/ai_models.json')

    # Save AIModel data to the specified JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"AI model data saved to: {json_file_path}")


if __name__ == "__main__":
    from model_jsons import ai_models_data
    save_ai_models_to_json(ai_models_data)
