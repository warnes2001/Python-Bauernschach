# pylint: disable=C

# Imports
import unittest
import storage
import main
import const
from player import Player
from unittest.mock import patch


class MainTest(unittest.TestCase):

    def test_check_movability_diagonal(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', None, None, 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, 'b', 'b', None, None, None, None], [
            None, None, 'w', None, None, None, None, None], [None, None, None, 'w', None, None, None, None], ['w', 'w', None, None, 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        player = Player('test', 'w', True)
        self.assertTrue(main.check_moveability(chessfield, player, 4, 2))

    def test_check_movability_normal(self):
        chessfield = [[None, None, None, None, None, None, None, None], [None, 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], ['b', None, None, None, None, None, None, None], [
            'w', None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        player = Player('test', 'b', True)
        self.assertFalse(main.check_moveability(chessfield, player, 3, 0))
        self.assertTrue(main.check_moveability(chessfield, player, 1, 3))

    def test_check_turn_start_position_black(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', None, 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, 'b', None, None, None, None], [
            None, None, 'w', None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', None, 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        player = Player('test', 'b', True)
        self.assertTrue(main.check_turn(chessfield, player, 1, 0, 3, 0))
        self.assertFalse(main.check_turn(chessfield, player, 1, 0, 4, 0))

    def test_check_turn_normal_move_black(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', None, 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, 'b', None, None, None, None], [
            None, None, 'w', None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', None, 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        player = Player('test', 'b', True)
        self.assertTrue(main.check_turn(chessfield, player, 3, 3, 4, 3))
        self.assertFalse(main.check_turn(chessfield, player, 3, 3, 5, 3))

    def test_check_turn_hit_black(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', None, 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, 'b', None, None, None, None], [
            None, None, 'w', None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', None, 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        player = Player('test', 'b', True)
        self.assertTrue(main.check_turn(chessfield, player, 3, 3, 4, 2))
        self.assertFalse(main.check_turn(chessfield, player, 3, 3, 5, 2))

    def test_new_game(self):
        data = main.new_game()

        expected_data = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]

        self.assertEqual(expected_data, data)

    def test_print_chessfield(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', None, 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, 'b', None, None, None, None], [
            None, None, 'w', None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', None, 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        self.assertTrue(main.print_chessfield(chessfield))

    def test_check_move_requirements_true(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]

        x, y = main.check_move_requirements(chessfield, ["a", "7"])

        self.assertEqual(1, x)
        self.assertEqual(0, y)

        x, y = main.check_move_requirements(chessfield, ["b", "2"])

        self.assertEqual(6, x)
        self.assertEqual(1, y)

    @patch('builtins.input', side_effect=['8i', 'i7', 'a5'])
    def test_check_move_requirements_false(self, mock_input):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]

        x, y = main.check_move_requirements(chessfield, ["8", "i", "8"])

        self.assertEqual(3, x)
        self.assertEqual(0, y)

    @patch('builtins.input', side_effect=['a2', 'a4'])
    def test_play_move(self, mock_input):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]
        player = Player('test', 'w', True)

        self.assertTrue(main.play_move(chessfield, player))

    def test_load_game(self):
        chessfield = [[None, None, None, None, None, None, None, None], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]

        player1 = Player('1', 'b', False)
        player2 = Player('2', 'w', True)

        main.save_game(chessfield, player1, player2)

        load_chessfield, load_player1, load_player2 = main.load_game()

        self.assertEqual(chessfield, load_chessfield)

        self.assertEqual(player1.name, load_player1.name)
        self.assertEqual(player1.color, load_player1.color)
        self.assertEqual(player1.turn, load_player1.turn)

        self.assertEqual(player2.name, load_player2.name)
        self.assertEqual(player2.color, load_player2.color)
        self.assertEqual(player2.turn, load_player2.turn)

    def test_load_game_error(self):
        storage.delete_json()
        chessfield, player1, player2 = main.load_game()

        self.assertIsNone(chessfield)
        self.assertIsNone(player1)
        self.assertIsNone(player2)

    def test_check_winner(self):
        chessfield = [[None, 'w', None, None, None, None, None, None], [None, None, 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], ['b', None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, 'w', 'w', 'w', 'w', 'w', 'w', 'w'], [None, None, None, None, None, None, None, None]]

        expected_result = const.COLOR_WHITE

        self.assertEqual(expected_result, main.check_winner(chessfield))

        chessfield = [[None, None, None, None, None, None, None, None], [None, 'b', 'b', 'b', 'b', 'b', 'b', 'b'], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [
            None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], ['w', None, 'w', 'w', 'w', 'w', 'w', 'w'], [None, 'b', None, None, None, None, None, None]]

        expected_result = const.COLOR_BLACK

        self.assertEqual(expected_result, main.check_winner(chessfield))

    @patch('builtins.input', side_effect=['Spieler 1', 'Spieler 2', '2'])
    def test_create_player_true_player2(self, mock_input):
        player1, player2 = main.create_player()

        exp_player1 = Player('Spieler 1', 'w', True)
        exp_player2 = Player('Spieler 2', 'b', False)

        self.assertEqual(exp_player1.name, player1.name)
        self.assertEqual(exp_player1.color, player1.color)
        self.assertEqual(exp_player1.turn, player1.turn)

        self.assertEqual(exp_player2.name, player2.name)
        self.assertEqual(exp_player2.color, player2.color)
        self.assertEqual(exp_player2.turn, player2.turn)

    @patch('builtins.input', side_effect=['Spieler 1', 'Spieler 2', '3', '1'])
    def test_create_player_true_player1(self, mock_input):
        player1, player2 = main.create_player()

        exp_player1 = Player('Spieler 1', 'b', False)
        exp_player2 = Player('Spieler 2', 'w', True)

        self.assertEqual(exp_player1.name, player1.name)
        self.assertEqual(exp_player1.color, player1.color)
        self.assertEqual(exp_player1.turn, player1.turn)

        self.assertEqual(exp_player2.name, player2.name)
        self.assertEqual(exp_player2.color, player2.color)
        self.assertEqual(exp_player2.turn, player2.turn)

    @patch('builtins.input', side_effect=['Spieler 1', 'Spieler 2', 'g', '1'])
    def test_create_player_false(self, mock_input):
        main.create_player()
        self.assertRaises(ValueError)

    @patch('builtins.input', side_effect=['n', 'spieler1', 'spieler2', '1', 'a2', 'a4', 'b7', 'b5', 'a4', 'b5', 'a7', 'a5', 'b5', 'b6', 'c7', 'c5', 'b6', 'b7', 'c5', 'c4', 'b7', 'b8', 'n'])
    def test_main(self, mock_input):
        self.assertTrue(main.main())

    @patch('builtins.input', side_effect=['f', 'b7', 'b8', 'n'])
    def test_main_load(self, mock_input):
        chessfield = [[None, None, None, None, None, None, None, None], [None, "w", None, "b", "b", "b", "b", "b"], [None, None, None, None, None, None, None, None], ["b", None, None, None, None, None, None, None], [
            None, None, "b", None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, "w", "w", "w", "w", "w", "w", "w"], [None, None, None, None, None, None, None, None]]
        player1 = Player('1', 'w', True)
        player2 = Player('2', 'b', False)

        main.save_game(chessfield, player1, player2)
        self.assertTrue(main.main())
