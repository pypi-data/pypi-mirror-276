from typing import List


def find_with_word(word: str, sentences: List[str]) -> List[str]:
    """
    This function checks if a word is in a list of sentences.

    :param word: Word to check
    :param sentences: List of sentences
    
    :return: List of sentences that contain the word

    >>> print(find_with_word('experience', [
    ...     'Proverbs are short sentences drawn from long experience.', 
    ...     'Naked I came into the world, and naked I must go out.']))
    ['Proverbs are short sentences drawn from long experience.']
    """
    return [sentence for sentence in sentences if word in sentence]


def replace_word(word: str, new_word: str, sentences: List[str]) -> List[str]:
    """
    This function replaces a word with a new word in a list of sentences.

    :param word: Word to replace
    :param new_word: New word to replace with
    :param sentences: List of sentences
    
    :return: List of sentences with the replaced word

    >>> print(replace_word('experience', 'wisdom', [
    ...     'Proverbs are short sentences drawn from long experience.', 
    ...     'Naked I came into the world, and naked I must go out.']))
    ['Proverbs are short sentences drawn from long wisdom.']
    """
    return [sentence.replace(word, new_word) for sentence in sentences]
