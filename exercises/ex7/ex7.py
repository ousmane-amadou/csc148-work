"""CSC148 Exercise 7: Recursion Wrap-Up

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 7.
"""
from typing import Dict, List


##############################################################################
# Task 1: Something a little different
##############################################################################
# The file of English words to use. The one we've provided doesn't contain
# plural forms. Assume this list is in alphabetical order.
FILE = 'dict.txt'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def anagrams(phrase: str, limit: int) -> List[str]:
    """Return a list of up to <limit> anagrams of <phrase>.

    The anagrams are returned in alphabetical order.

    >>> anagrams('dormitory', 3)
    ['dirty room', 'dormitory', 'room dirty']
    """
    # TODO: use the debugger to inspect the contents of the following two
    # variables. This is particularly useful to see how the letter frequencies
    # are being represented.
    words = _generate_word_list(FILE)
    letter_count = _generate_letter_count(phrase)
    return _anagrams_helper(words, letter_count, limit)


def _generate_word_list(dict_file: str) -> List[str]:
    """Read in English words from <dict_file> and return them.

    The returned list is in alphabetical order.

    Precondition:
    """
    words = []
    with open(dict_file) as f:
        for line in f.readlines():
            words.append(line.strip().lower())
    return words


def _generate_letter_count(phrase: str) -> Dict[str, int]:
    """Return a dictionary counting the letter occurrences in <string>.

    All letters in <phrase> are converted to lower-case.
    The keys in the returned dictionary are the 26 lower-case letters,
    'a', 'b', 'c', etc.

    Precondition: <phrase> contains only letters.
    """
    lower = phrase.lower()
    letter_count = {}
    for char in LETTERS:
        letter_count[char] = lower.count(char)
    return letter_count


def _within_letter_count(word: str, letter_count: Dict[str, int]) -> bool:
    """Return whether <word> can be made using letters in <letter_count>."""
    for char in LETTERS:
        if word.count(char) > letter_count[char]:
            return False
    return True


# TODO: Implement this function according to the comments below!
def _anagrams_helper(words: List[str], letter_count: Dict[str, int],
                     limit: int) -> List[str]:
    """Return the first <limit> anagrams using the given letter counts
    and allowed words.

    Each anagram must use all the letters, with correct occurrences, given by
    <letter_count>, and must use only the words appearing in <words>.

    Note: we're using a helper function here so that you don't need to
    recompute <words> for each recursive call.

    If there are more than <limit> possible anagrams, return the <limit>
    anagrams that are first alphabetically.
    If there are fewer than <limit> possible anagrams, return all of them.

    The anagrams are returned in alphabetical order.

    Preconditions:
    - letter_count has 26 keys (one per lowercase letter),
      and each value is a non-negative integer.
    - limit >= 0
    """
    anagrams_list = []
    # 1. Base case: limit == 0.
    if limit == 0:
        return []

    no_character_flag = True
    for letter in letter_count.values():
        if letter != 0:
            no_character_flag = False

    if no_character_flag:
        return ['']

    # 2. Base case: no more letters in <letter_count>.
    # In this case, there is only one valid anagram: the empty string.
    for word in words:
        # 3. For each word, check whether it can be used with the given
        # letter count. (If not, go onto the next word.)
        usabliity_flag = True
        for character in word:
            if letter_count[character] < word.count(character):
                usabliity_flag = False

        if not usabliity_flag:
            continue

        # 4. If the word can be used, recurse and create anagrams.
        #    For this part, you'll need to do three things:
        #  (i) Create a new dictionary that has the same values as letter_count,
        #      except with counts decreased based on the letters in <word>.
        #      Look at how we implemented _generate_letter_count for guidance.
        #
        #      Or, you could mutate letter_count directly, as long as you
        #      change it back at the end of the iteration.
        #  (ii) Call _anagrams_helper recursively with the new, reduced
        #       letter count.
        #  (iii) Combine <word> with the result of the recursive call to update
        #        <anagrams_list> with the anagrams that start with <word>.
        #        Don't forget to separate the words with a space.
        new_letter_count = {}

        for character in LETTERS:
            new_letter_count[character] = \
                letter_count[character] - word.count(character)

        angrm = _anagrams_helper(words, new_letter_count, limit)
        for a in angrm:
            anagrams_list += [(word + " " + a).strip()]

        # 5. If the limit has been reached, stop the loop early!
        #    No need to do more work than asked for.
        if len(anagrams_list) == limit:
            break

    # 6. Return the anagrams that can be made by the letters in letter_count.
    #    (We've done this for you.)
    return anagrams_list


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['_generate_word_list']
    })
