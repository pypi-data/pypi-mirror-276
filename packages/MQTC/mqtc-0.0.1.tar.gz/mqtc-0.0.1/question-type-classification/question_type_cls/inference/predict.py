from typing import Dict, List, Union

import yaml
from question_type_cls.dataset.preprocess import preprocess_data
from transformers import pipeline


class Classifier:
    """
    Facilitates text classification using a pre-trained sentiment analysis model.

    This class wraps a text classification pipeline from a library like Transformers
    and provides a convenient interface for classifying text inputs.
    """

    def __init__(
        self,
        model_name_or_path: str,
        device_map: str = "auto",
        max_length: int = 256,
        return_all_scores: bool = False,
    ):
        """
        Initializes the Classifier.

        Args:
            model_name_or_path (str): Path to the pre-trained sentiment classification model or its name.
            device_map (str, optional): Device mapping for loading the model (e.g., "cuda", "cpu"). Defaults to "auto".
            max_length (int, optional): Maximum input length to truncate texts for the model. Defaults to 256.
        """

        self.model_name_or_path = model_name_or_path
        self.classifier = pipeline(
            model=self.model_name_or_path,
            device_map=device_map,
            task="sentiment-analysis",
            max_length=max_length,
            truncation=True,
            return_all_scores=return_all_scores,
        )

    def __call__(self, texts: Union[str, List[str]], **kwargs) -> List[dict]:
        """
        Classifies the provided text(s).

        Args:
            texts (Union[str, List[str]]): Single text or a list of texts to classify.
            **kwargs: Additional keyword arguments to pass to the preprocess_data function.

        Returns:
            List[dict]: A list of prediction dictionaries for each input text.
        """

        if isinstance(texts, str):
            texts = preprocess_data(texts, **kwargs)
        else:
            texts = list(map(lambda text: preprocess_data(text, **kwargs), texts))

        return self.classifier(texts)


class MathQuestionClassifier:
    """
    Classifies math questions according to math type and difficulty level.

    This class utilizes two pre-trained models to classify math questions:

    - **Math Type Classifier:** Predicts the type of math question (e.g., addition, subtraction, etc.)
    - **Math Difficulty Classifier:** Predicts the difficulty level of the math question (e.g., easy, medium, hard)

    Args:
        math_type_config (Dict): Configuration for the math type classifier,
            - model_config (Dict): Configuration for the pre-trained model,
                    - model_name_or_path (str): Path to the pre-trained model or a method to retrieve it.
                    - device_map (str, optional): Device to load the model on (e.g., "cuda", "cpu"). Defaults to "auto".
                    - max_length (int, optional): Maximum input length for the model. Defaults to 256.
            - preprocess_data (Dict, optional): Preprocessing steps for the math question,
                    - lower (bool, optional): Whether to convert the text to lowercase. Defaults to True.
        math_diff_config (Dict): Configuration for the math difficulty classifier,
            with the same structure as `math_type_config`.
    """

    def __init__(self, math_type_config: Dict[str, Dict], math_diff_config: Dict[str, Dict]):
        """
        Initializes the MathQuestionClassifier.

        Args:
            math_type_config (Dict[str, Dict]): Configuration for the math type classifier (as described in the class docstring).
            math_diff_config (Dict[str, Dict]): Configuration for the math difficulty classifier (as described in the class docstring).
        """
        self.math_type_config = math_type_config
        self.math_diff_config = math_diff_config

        self.math_type_classifier = Classifier(**self.math_type_config["model_config"])
        self.math_diff_classifier = Classifier(**self.math_diff_config["model_config"])

    @classmethod
    def from_yaml_config(cls, config_path: str):
        """
        Initialize the predictor from a yaml config file.
        Args:
            config_path (str): path to yaml config file.
        """
        config = yaml.safe_load(open(config_path, "r"))
        return cls(**config)

    def __call__(self, math_question: Union[str, list]) -> List[dict]:
        """
        Classifies a given math question according to its math type and difficulty level.

        Args:
            math_question (str): The math question to be classified.

        Returns:
            List[dict]: List of dictionaries containing the result of the classification
                dict: A dictionary containing the following information about the math question:
                    - "math_question": The original math question.
                    - "math_type": The predicted math type of the math question.
                    - "math_difficulty": The predicted difficulty level of the math question.

        Raises:
            TypeError: If the input `math_question` is not a string or list.
        """
        if not isinstance(math_question, (str, list)):
            raise TypeError("Input must be a string or a list of strings.")

        if isinstance(math_question, str):
            math_question = [math_question]

        math_type_result = self.math_type_classifier(
            math_question, **self.math_type_config["preprocess_data"]
        )
        math_diff_result = self.math_diff_classifier(
            math_question, **self.math_diff_config["preprocess_data"]
        )

        results = []

        for i in range(len(math_question)):
            results.append(
                dict(
                    math_question=math_question[i],
                    math_type=math_type_result[i],
                    math_difficulty=math_diff_result[i],
                )
            )

        return results
