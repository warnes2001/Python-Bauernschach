'''Storage module: manages loading, saving and verifiying of game data'''


# Imports
import json
import hashlib
from player import Player
from const import SAVED_GAME_PATH, HASH_PATH


def save_json(data):
    '''Store game values in JSON file and the md5 hash in a second file

    Arguments:
        data {dict} - game values

    '''
    try:
        with open(SAVED_GAME_PATH, 'w') as file:

            try:
                json.dump(data, file)

            except TypeError:
                print('Spielstand konnte nicht gespeichert werden.')

    except ValueError:
        print('Spielstand konnte nicht gespeichert werden.')

    save_hash(data)


def load_json():
    '''Load data from saved game JSON file

    Return:
        data {dict} -- game values
        False {bool} --

    '''
    try:
        with open(SAVED_GAME_PATH, 'r') as file:
            try:
                data = json.load(file)

            except ValueError:
                print('Datei konnte nicht geladen werden.')
                return None

    except FileNotFoundError:
        print('Datei konnte nicht geladen werden.')
        return None

    if verify_hash(data):
        print('Spielstand erfolgreich geladen.')
        return data

    print('Dateien konnten nicht verifiziert werden.')
    return None


def get_hash(data):
    '''Return the checksum of given object

    Arguments:
        data {dict} -- game values

    Return:
        sha256 {String} -- checksum

    '''

    sha256_hash = hashlib.sha256(str(data).encode()).hexdigest()

    return sha256_hash


def save_hash(data):
    '''Retrieves the checksum of given object and stores it

    Arguments:
        data {dict} -- game values

    '''
    hash_str = get_hash(data)
    try:
        with open(HASH_PATH, 'w') as file:

            file.write(hash_str)

    except ValueError:
        print('Hash error')


def load_hash():
    '''Returns the previously saved checksum from file

    Returns:
        hash_str {String} -- sha256 checksum

    '''
    try:
        with open(HASH_PATH, 'r') as file:
            hash_str = file.read()
        return hash_str

    except FileNotFoundError:
        return None


def verify_hash(data):
    '''Verify game data by comparing the md5 hashes

    Arguments:
        data {dict} -- game values

    Returns:
        {Bool}  --  True if check passed
                    False if check failed

    '''
    return get_hash(data) == load_hash()


def load_player(player_as_dict):
    '''Converts the player dict into python object

    Arguments:
        player_as_dict {dict} -- player dictionary

    Returns:
        Player object

    '''

    return Player.from_dict(player_as_dict)


def delete_json():
    '''Overwrites the JSON with empty string'''

    try:
        with open(SAVED_GAME_PATH, 'w') as file:
            file.write('')
            print('Spielstand wurde gelöscht.')

    except ValueError:
        print('Spielstand konnte nicht gelöscht werden.')
