from typing import Dict, List, Union


def normalize_model_output(output: Union[List[List[Dict]], List[Dict]]) -> List[List[Dict]]:
    if not output:
        return []

    if isinstance(output[0], list):
        return output
    else:
        return [output]
