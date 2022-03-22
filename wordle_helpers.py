import string
import random
import numpy as np
from collections import Counter
import itertools
import pandas as pd
from functools import wraps
import datetime as dt
import re
from spellchecker import SpellChecker
from tqdm import tqdm


def words_with_commonly_used_letters(word_list):
    most_commonly_used_letters = "etaionshrdluymwfgcbp"
    alphabet = string.ascii_lowercase
    least_commonly_used_letters = "".join(set(alphabet) - set(most_commonly_used_letters))
    return [word for word in word_list if not any(char in word for char in least_commonly_used_letters)]


def words_starting_with_commonly_used_letters(word_list):
    most_common_starting_letters = "taisocmfpw"
    return [word for word in word_list for letter in most_common_starting_letters if word.startswith(letter)]
    

def sorted_words_by_frequency(word_list, sorting=True):
    spell = SpellChecker()
    spell_checker_words_and_frquency = [(word, spell.word_usage_frequency(word)) for word in word_list]
    if sorting:
        return sorted(spell_checker_words_and_frquency, key=lambda word_freq: word_freq[1], reverse=True)
    return spell_checker_words_and_frquency


def anagram_pairs(words_list):
    return np.array([combo for combo in itertools.combinations(words_list, 2)
                     if len(set("".join(combo))) == 5])


def anagram_word_frequency(arr):
    word_freq = []
    spell = SpellChecker()
    for anagrams in arr:
        words = anagrams.split(", ")
        frequency = []
        for word in words:
            frequency.append((word, spell.word_usage_frequency(word)))
        word_freq.append(frequency)
    return np.array(word_freq, dtype=object)


def anagram_to_keep(arr):
    keep_words = []
    for tup in arr:
        most_frequent = sorted(tup, key=lambda x: x[1], reverse=True)
        word_to_keep = most_frequent[0][0]
        if word_to_keep not in keep_words:
            keep_words.append(word_to_keep)
    return np.unique(np.array(keep_words, dtype=object))


def wordle_scoring(guess_word_pairs, challenge_words):
    np.random.shuffle(guess_word_pairs)
    np.random.shuffle(challenge_words)

    data = []

    for word in tqdm(challenge_words):
        for pair in guess_word_pairs:
            scores = np.zeros(10, dtype=np.int8).reshape(2, 5)
            for idx, selection in enumerate(pair):
                for idx2, (x, y) in enumerate(zip(word, selection)):
                    if x == y:
                        scores[idx][idx2] = 1
                    elif x != y and y in word:
                        scores[idx][idx2] = 0
                    else:
                        scores[idx][idx2] = -1

            positional_scores = re.sub(r"[\[\]]", "", str(scores)).replace("\n", ",")
 
            temp = {
                "challenge_word": word,
                "guess_pair": ", ".join(pair),
                "first_guess": pair[0],
                "second_guess": pair[1],
                "first_pos_score": positional_scores.split(", ")[0].strip(),
                "second_pos_score": positional_scores.split(", ")[1].strip(),
                "sum_first_pos_score": scores[0].sum(),
                "sum_second_pos_score": scores[1].sum(),
                "correct_letter_pos_score": re.sub(r"[\[\]]", "", str(np.max(scores, axis=0))).strip(),
                "sum_correct_letter_pos_score": np.sum(np.max(scores, axis=0)),
            }
            data.append(temp)

    wordle_score = pd.DataFrame(data)

    cat_cols = wordle_score.select_dtypes(include=object).columns.tolist()
    wordle_score[cat_cols] = wordle_score[cat_cols].astype(dtype="string[pyarrow]")

    num_cols = wordle_score.select_dtypes(include=np.number).columns.tolist()
    wordle_score[num_cols] = wordle_score[num_cols].astype(np.int8)
    return wordle_score