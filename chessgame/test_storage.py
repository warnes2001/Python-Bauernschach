# pylint: disable=C

import unittest
import storage
from player import Player


class StorageTest(unittest.TestCase):

    def test_get_hash(self):
        data = "test"
        hash_data = storage.get_hash(data)
        self.assertEqual(
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", hash_data)

        data = "hallo"
        hash_data = storage.get_hash(data)
        self.assertEqual(
            "d3751d33f9cd5049c4af2b462735457e4d3baf130bcbb87f389e349fbaeb20b9", hash_data)

        data = "d34141s3f4vg5gv435f134d234cv15"
        hash_data = storage.get_hash(data)
        self.assertEqual(
            "be896bbba4c09c234679dbd02b6f7e657127e1696bca492896fd7a90b457018c", hash_data)

    def test_load_player(self):

        test_data = {'name': '1', 'color': 'b', 'turn': False}
        output_data = storage.load_player(test_data)

        player = Player('1', 'b', False)

        self.assertEqual(player.name, output_data.name)
        self.assertEqual(player.color, output_data.color)
        self.assertEqual(player.turn, output_data.turn)
        
    def test_load_save_hash(self):

        storage.save_hash("d34141s3f4vg5gv435f134d234cv15")
        expected_output = "be896bbba4c09c234679dbd02b6f7e657127e1696bca492896fd7a90b457018c"

        self.assertEqual(expected_output, storage.load_hash())

    def test_verify_hash(self):

        test_data = "d34141s3f4vg5gv435f134d234cv15"

        storage.save_hash(test_data)
        self.assertTrue(storage.verify_hash(test_data))

        storage.save_hash(test_data)
        self.assertFalse(storage.verify_hash("test"))

    def test_save_load(self):

        test_data = '{"chessfield": [[null, null, null, null, null, null, null, null], [null, "b", "b", "b", "b", "b", "b", "b"], [null, null, null, null, null, null, null, null], ["b", null, null, null, null, null, null, null], ["w", null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, "w", "w", "w", "w", "w", "w", "w"], [null, null, null, null, null, null, null, null]], "player1": {"name": "1", "color": "b", "turn": false}, "player2": {"name": "2", "color": "w", "turn": true}}'

        storage.save_json(test_data)
        data_output = storage.load_json()

        self.assertEqual(test_data, data_output)


    def test_save_json_error(self):

        game_data = Player('1', 'b', False)
        storage.save_json(game_data)

        self.assertRaises(ValueError)

     


    def test_delete_json(self):

        test_data = '{"chessfield": [[null, null, null, null, null, null, null, null], [null, "b", "b", "b", "b", "b", "b", "b"], [null, null, null, null, null, null, null, null], ["b", null, null, null, null, null, null, null], ["w", null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, "w", "w", "w", "w", "w", "w", "w"], [null, null, null, null, null, null, null, null]], "player1": {"name": "1", "color": "b", "turn": false}, "player2": {"name": "2", "color": "w", "turn": true}}'

        storage.save_json(test_data)
        storage.delete_json()

        self.assertIsNone(storage.load_json())
