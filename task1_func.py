import math
import random
from pprint import pprint

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {"offset": 0, "score": {"home": 0, "away": 0}}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = (
        1 if score_changed and random.random() > 1 - PROBABILITY_HOME_SCORE else 0
    )
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change,
        },
    }


def generate_game():
    stamps = [
        INITIAL_STAMP,
    ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()

pprint(game_stamps)


# Так как gamestamps генерируются последовательно, по сути у нас
# задача максимально эффективно найти нужное значение ключа offset в списке словарей gamestamps,
# отсортированном по значению offset.
# Лучше всего, на мой взгляд сделать с использованием бинарного поиска.
# Асимптотическая сложность: логарифмическая  - O(log(n)).
# Бинарный поиск можно реализовать, через цикл или рекурсию.


def get_score(game_stamps, offset):
    """
    Бинарный поиск через цикл.
    """
    first_index = 0
    last_index = len(game_stamps) - 1
    stamp = None
    iter_count = 0
    while (first_index <= last_index) and stamp == None:
        iter_count += 1
        mid = (first_index + last_index) // 2
        if game_stamps[mid]["offset"] == offset:
            stamp = game_stamps[mid]
        else:
            if offset < game_stamps[mid]["offset"]:
                last_index = mid - 1
            else:
                first_index = mid + 1
    if stamp:
        home, away = dict(**stamp["score"]).values()
        return home, away
    return stamp


def get_score_recursion(game_stamps, offset):
    """
    Бинарный поиск через рекурсию.
    """

    def binary_search(lst, offset, first_index=0, last_index=None):
        if last_index is None:
            last_index = len(lst) - 1
        if first_index > last_index:
            return None
        mid = (first_index + last_index) // 2
        if lst[mid]["offset"] == offset:
            return lst[mid]
        if offset < lst[mid]["offset"]:
            return binary_search(lst, offset, first_index, mid - 1)
        if offset > lst[mid]["offset"]:
            return binary_search(lst, offset, mid + 1, last_index)

    stamp = binary_search(game_stamps, offset)
    if stamp:
        home, away = dict(**stamp["score"]).values()
        return home, away
    return stamp
