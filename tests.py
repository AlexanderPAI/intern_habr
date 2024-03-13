import random
import unittest

from task1_func import generate_game, generate_stamp, get_score, get_score_recursion


class GetScoreCycleTest(unittest.TestCase):
    """Тестирование get_score"""
    @classmethod
    def setUpClass(cls):
        cls.game_stamps = generate_game()

    def func_by_existing_offset(self, func):
        """Общая функция тестирования при передаче существующего offset'a."""
        offset = random.choice(self.game_stamps)
        get_score_cycle_result = func(self.game_stamps, offset['offset'])
        self.assertEqual(get_score_cycle_result, (offset['score']['home'], offset['score']['away']))

    def func_by_unexisting_offset(self, func):
        """Общая функция тестирования при передаче несуществующего offset'a."""
        fake_offset = self.game_stamps[-1]['offset'] + 1
        get_score_cycle_result = func(self.game_stamps, fake_offset)
        self.assertEqual(get_score_cycle_result, None)

    def test_get_score_cycle_by_existing_offset(self):
        """Передача существующего offset в get_score, использующую рекурсию."""
        self.func_by_existing_offset(get_score)

    def test_get_score_cycle_by_unexisting_offset(self):
        """Передача несуществующего offset в get_score, использующую рекурсию."""
        self.func_by_unexisting_offset(get_score)

    def test_get_score_recursion_by_existing_offset(self):
        self.func_by_existing_offset(get_score_recursion)

    def test_get_score_recursion_by_unexisting_offset(self):
        self.func_by_unexisting_offset(get_score_recursion)
