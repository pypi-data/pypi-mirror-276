import pandas as pd
from question_type_cls.dataset.normalize_character import NormalizeCharacter


normalizer = NormalizeCharacter()


def drop_duplicate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate question.

    Args:
        df (DataFrame): A dataset.

    Returns:
        A dataframe with unique question.
    """

    return df.drop_duplicates(subset=["question"])


def preprocess_data(text: str, lower: bool = True, remove_img_tags: bool = True) -> str:
    """Preprocess data for training"""
    return normalizer.normalize_text(text, lower=lower, remove_img=remove_img_tags)
