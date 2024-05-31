from question_type_cls.configs.key_type import math_type


def rulebase_cls(text: str) -> str:
    """
    Classifies a mathematical question type based on keywords in the text.

        This function iterates through a predefined dictionary (`math_type`) that maps math types (e.g., "G1") to keyword groups. It checks if any keywords within a group are present in the input text (`text`).

        If a match is found, the function returns a combined label based on the matched labels (e.g., "G1-Q-P" for "G1-Q" or "G1-P"). If no exact match is found, the function returns the original label as a fallback.

        If no keywords from any group are found in the text, the function returns "NaN" to indicate that a classification couldn't be made.

        Args:
            text (str): The mathematical question text to be classified.

        Returns:
            str: The classified math type label (e.g., "G1-Q-P", "A-S-UB") or "NaN" if no match is found.
    """
    for type, keywords_dict in math_type.items():
        for label, keywords in keywords_dict.items():
            for keyword in keywords:
                if keyword in text:
                    if label == "G1-Q" or label == "G1-P":
                        label = "G1-Q-P"
                    elif label == "G1-R" or label == "G1-S":
                        label = "G1-R-S"
                    elif (
                        label == "G2-PL" or label == "G2-R" or label == "G2-CU" or label == "G2-P"
                    ):
                        label = "G2-PL-R-CU-P"
                    elif label == "G2-S" or label == "G2-CY" or label == "G2-CO":
                        label = "G2-S-CY-CO"
                    elif label == "A-EQ" or label == "A-SE":
                        label = "A-EQ-SE"
                    elif label == "A-S" or label == "A-UB":
                        label = "A-S-UB"
                    elif label == "C-AN" or label == "C-I":
                        label = "C-AN-I"
                    elif label == "C-L" or label == "C-AS":
                        label = "C-L-AS"
                    else:
                        pass
                    return {'label': label}
                else:
                    return {'label': "NaN"}

    return {'label': "NaN"}
