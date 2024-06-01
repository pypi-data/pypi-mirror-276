from typing import List, Tuple

class SpecialWordReplacer:
    """
    This class replace or mask special words between in particular words in a text.

    :param special_words: List of special words to replace or mask
    :param target_word: Word to replace or mask in special words
    :param replacement_char: Character to replace the target word with

    >>> replacer = SpecialWordReplacer(['New York', 'El Nino'], ' ', '•')
    >>> print(replacer.mask_words('New York is affected by El Nino.'))
    New•York is affected by El•Nino.
    >>> replacer = SpecialWordReplacer(['"apple"'], 'apple', 'green apple')
    >>> print(replacer.mask_words('He said the word "apple" while pointing at an apple.'))
    He said the word "green apple" while pointing at an apple.
    """
    def __init__(self, special_words: List[str], target_word: str, replacement_char: str):
        import re

        self.special_words = special_words
        self.target_word = target_word
        self.replacement_char = replacement_char
        self.compiled_patterns = {
            re.compile(re.escape(word)): word.replace(target_word, replacement_char)
            for word in special_words
        }

    def mask_words(self, text: str) -> str:
        """
        This function masks special words in a text.

        :param text: Text to mask special words in

        :return: Text with special words masked
        """
        for pattern, masked_word in self.compiled_patterns.items():
            text = pattern.sub(masked_word, text)
        return text
    
    def __repr__(self):
        return f'<SpecialWordReplacer(special_words={self.special_words}, target_word=\'{self.target_word}\', replacement_char=\'{self.replacement_char}\')>'
