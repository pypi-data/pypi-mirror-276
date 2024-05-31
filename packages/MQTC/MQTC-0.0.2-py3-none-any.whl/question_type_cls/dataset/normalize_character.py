import re

from question_type_cls.dataset.accent_processor import AccentProcessor
from question_type_cls.utils.special_characters import ACCENT_CHARACTERS, SPECIAL_CHARACTERS


class NormalizeCharacter:
    def __init__(self):
        self.special_characters = SPECIAL_CHARACTERS
        self.accent_characters = ACCENT_CHARACTERS
        self.accent_processor = AccentProcessor()

    def normalize_special_characters(self, text: str) -> str:
        """
        Normalize special characters in text.
        """
        for character in self.special_characters:
            text = text.replace(list(character.keys())[0], list(character.values())[0])

        return text

    def normalize_accent_characters(self, text: str) -> str:
        """
        Normalize accent characters in text.
        """
        sentences = text.split("\n")
        output = []
        for sentence in sentences:
            sentence = sentence.strip().split(" ")
            for i, word in enumerate(sentence):
                for accent in self.accent_characters:
                    accent_error = list(accent.keys())[0]
                    accent_replace = list(accent.values())[0]
                    if accent_error in word:
                        sentence[i] = self.accent_processor.custom_change_accent(
                            word.replace(accent_error, ""), accent_replace
                        )
            normalize_text = " ".join(sentence)
            output.append(normalize_text)
        return "\n".join(output)

    def normalize_punctuations(self, text: str) -> str:
        """
        Replace, remove punctuation in text.
        """
        text = self.normalize_accent_characters(text)
        text = self.normalize_special_characters(text)

        text = text.replace("( ", "(").replace(" )", ")")
        text = text.replace("[ ", "[").replace(" ]", "]")

        text = re.sub(r" ?\^ ?", "^", text)
        text = re.sub(r"\s?_\s?", "_", text)
        text = re.sub(r"\$", "", text)
        text = re.sub(r"[`?]", "", text)
        text = re.sub(r"\.{3,}", " ", text)
        text = re.sub(r"-{2,}", " ", text)
        text = re.sub(r"(\n)+", "\n", text)

        return re.sub(r" +", " ", text).strip()

    def remove_image_tags(self, text: str) -> str:
        """
        Remove image tags in text.
        """
        text = re.sub(r"\[{2}.*?]{2}", "", text)
        text = re.sub(r"<img.*?/>", "", text)
        return text.strip()

    def normalize_text(self, text: str, lower: bool = False, remove_img: bool = True) -> str:
        if remove_img:
            text = self.remove_image_tags(text)

        text = self.normalize_punctuations(text)

        if lower:
            text = text.lower()
        return text
