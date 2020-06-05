'''Main module: manages Board and Game'''

# Imports
import storage
from const import GAME_SIZE, COLOR_WHITE, COLOR_BLACK
from player import Player


def create_player():
    '''Creates the two player objects needed to start the game

    Arguments:
        --


    Returns:
        player1 -- 1. player object
        player2 -- 2. player object

    '''

    name1 = input("Bitte einen Namen für Spieler 1 vergeben: ")

    name2 = input("Bitte einen Namen für Spieler 2 vergeben: ")

    print("Vielen Dank, " + name1 +
          ", welche Farbe möchtest du sein? Drücke 1 für Schwarz und 2 für Weiß:", end=" ")

    while True:

        try:

            color = int(input())

            if color in [1, 2]:
                break

            print("Geben Sie entweder 1 für Schwarz oder 2 für Weiß ein!:", end=" ")

        except ValueError:
            print("Geben Sie entweder 1 für Schwarz oder 2 für Weiß ein!:", end=" ")

    if int(color) == 2:
        player1 = Player(name1, COLOR_WHITE, True)
        player2 = Player(name2, COLOR_BLACK, False)

        print("Danke. Spieler 2, du bist im schwarzen Team.")
        return player1, player2

    if int(color) == 1:
        player1 = Player(name1, COLOR_BLACK, False)
        player2 = Player(name2, COLOR_WHITE, True)

        print("Danke. Spieler 2, du bist im weißen Team.")
        return player1, player2


def new_game():
    '''Loads a new game by returning a 'fresh' chessfield

    Arguments: None


    Returns:
        chessfield {list} -- list of default values

    '''

    rows = GAME_SIZE
    columns = GAME_SIZE

    chessfield = [[None for row in range(rows)] for columns in range(columns)]

    for pos_x in range(columns):
        chessfield[1][pos_x] = COLOR_BLACK
        chessfield[columns - 2][pos_x] = COLOR_WHITE

    return chessfield


def print_chessfield(chessfield):
    '''Prints the chessfield to console

    Arguments:
        chessfield {list} -- current chessfield as list


    Returns:
        --

    '''

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    sep = "+---"
    end = "+"

    for row in range(chessfield.__len__()):

        print(sep * len(chessfield[row]), end="")
        print(end)

        for column in range(len(chessfield[row])):
            if chessfield[row][column] == COLOR_WHITE:
                print("| W", end=" ")

            elif chessfield[row][column] == COLOR_BLACK:
                print("| B", end=" ")

            else:
                print("| *", end=" ")

        print("| " + str(GAME_SIZE - row))

    print(sep * len(chessfield[row]) + "+")

    for k in range(len(chessfield)):
        print("  " + alphabet[k], end=" ")

    print()
    return True


def check_move_requirements(chessfield, coordinates):
    '''Checks if the input coordinates are valid

    Arguments:
        chessfield {list} -- current chessfield as list
        coordinates {list} -- player input as list (eg. a2)


    Returns:
        pos_x {int} -- row in chessfield
        pos_y {int} -- column in chessfield

    '''

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]

    while True:

        if len(coordinates) == 2:
            if not coordinates[0].isdigit() and coordinates[1].isdigit():

                # checks for valid characters
                for char in range(len(chessfield)):

                    if coordinates[0] == alphabet[char]:
                        coordinates[0] = char
                        break

                valid_numbers = list(range(len(chessfield)))

                if coordinates[0] == char and int(coordinates[1]) - 1 in valid_numbers:

                    # verify that coordinates are inside the field
                    if int(coordinates[1]) <= len(chessfield) and coordinates[0] <= len(chessfield):
                        pos_x = len(chessfield) - int(coordinates[1])
                        pos_y = int(coordinates[0])

                        return pos_x, pos_y

        print("Nicht korrekte Zeichenfolge eingegeben. Bitte Koordinaten neu eingeben (z.B. a2, c4):", end=" ")
        point = input()
        coordinates = list(point)


def check_moveability(chessfield, player, pos_x, pos_y):
    '''Checks if a figure on a specific position is able to move

    Arguments:
        chessfield {list} -- current chessfield as list
        player {obj} -- active player
        pos_x {int} -- row in chessfield
        pos_y {int} -- column in chessfield


    Returns:
        True -- figure is movable
        False -- figure is not moveable

    '''
    pos_white = pos_x - 1
    pos_black = pos_x + 1

    # prove if pawn is moveable
    if player.color == COLOR_WHITE:
        pos_turn = pos_white

    else:
        pos_turn = pos_black

    if chessfield[pos_turn][pos_y] is not player.color and chessfield[pos_turn][pos_y] is not None:

        if (chessfield[pos_turn][pos_y - 1] is None) and (chessfield[pos_turn][pos_y + 1] is None):
            return False

        if pos_y - 1 < 0 or pos_y + 1 > GAME_SIZE:

            if pos_y - 1 < 0:
                if chessfield[pos_turn][pos_y + 1] is None:
                    return False

                return True

            if pos_y + 1 > GAME_SIZE:

                if chessfield[pos_turn][pos_y - 1] is None:
                    return False

                return True

    return True


def check_turn(chessfield, player, pos_x, pos_y, end_pos_x, end_pos_y):
    '''Checks if a turn is valid

    Arguments:
        chessfield {list} -- current chessfield as list
        player {obj} -- active player
        pos_x {int} -- start row in chessfield
        pos_y {int} -- start column in chessfield
        end_pos_x {int} -- end row in chessfield
        end_pos_y {int} -- end column in chessfield


    Returns:
        True -- valid turn
        False -- invalid turn

    '''

    dif_pos_x = end_pos_x - pos_x
    dif_pos_y = end_pos_y - pos_y

    pos_black = 1
    pos_white = GAME_SIZE - 2
    dif_pos_black_start = 2
    dif_pos_white_start = -2
    dif_pos_black = 1
    dif_pos_white = -1

    # valid moves for black color
    if player.color == COLOR_BLACK:
        pos_turn = pos_black
        dif_pos_turn = dif_pos_black
        dif_pos_turn_start = dif_pos_black_start

    # valid moves for white color
    else:
        pos_turn = pos_white
        dif_pos_turn = dif_pos_white
        dif_pos_turn_start = dif_pos_white_start

    if chessfield[end_pos_x][end_pos_y] is None:

        # allow move 2x at start position
        if pos_x == pos_turn and dif_pos_x == dif_pos_turn_start and dif_pos_y == 0:
            chessfield[pos_x][pos_y] = None
            chessfield[end_pos_x][end_pos_y] = player.color
            return True

        # regular move
        if dif_pos_x == dif_pos_turn and dif_pos_y == 0:
            chessfield[pos_x][pos_y] = None
            chessfield[end_pos_x][end_pos_y] = player.color
            return True

        return False

    if chessfield[end_pos_x][end_pos_y] is not player.color and chessfield[end_pos_x][end_pos_y] is not None:
        # schräg schlagen
        if dif_pos_x == dif_pos_turn and abs(dif_pos_y) == 1:
            chessfield[pos_x][pos_y] = None
            chessfield[end_pos_x][end_pos_y] = player.color
            return True

        return False

    return False


def play_move(chessfield, player):
    '''Executes a turn

    Arguments:
        chessfield {list} -- current chessfield as list
        player {obj} -- active player


    Returns:
        --

    '''

    while True:

        print(player.name +
              ", wähle bitte den Bauern für deinen nächsten Zug (z.B. a2):", end=" ")
        startpoint = input()
        start_coordinates = list(startpoint)
        pos_x, pos_y = check_move_requirements(chessfield, start_coordinates)

        # prove if Player chose his own pawn
        if chessfield[pos_x][pos_y] != player.color:
            print("Bitte ein Feld mit dem Bauern deines Teams auswählen! Bitte Koordinaten neu eingeben (z.B. a2, c4):")

        elif not check_moveability(chessfield, player, pos_x, pos_y):
            print("Dieser Bauer ist bewegungsunfähig, bitte einen anderen auswählen!")

        else:
            break

    while True:

        print(player.name + ", wähle nun die Position auf die dein Bauer springen soll! (z.B. a4):", end=" ")

        endpoint = input()
        end_coordinates = list(endpoint)
        end_pos_x, end_pos_y = check_move_requirements(
            chessfield, end_coordinates)

        if not check_turn(chessfield, player, pos_x, pos_y, end_pos_x, end_pos_y):
            print("Ungültiger Zug! Bitte Koordinaten nochmal eingeben!")

        else:
            return True


def check_winner(chessfield):
    '''Checks if a figure is at the end of the field and has won

    Arguments:
        chessfield {list} -- current chessfield as list


    Returns:
        Color of the winning player:
            COLOR_WHITE
            COLOR_BLACK


    '''

    for pos_x in range(len(chessfield)):

        if chessfield[0][pos_x] == COLOR_WHITE:
            return COLOR_WHITE

        if chessfield[GAME_SIZE - 1][pos_x] == COLOR_BLACK:
            return COLOR_BLACK

    return False


def save_game(chessfield, player1, player2):
    '''Puts the game objects into a dict and calls the save_json() method of the storage module

    Arguments:
        chessfield {list} -- current chessfield as list
        player1 {obj} -- 1. player
        player2 {obj} -- 2. player

    Returns:
        ---

    '''

    data = {}
    data['chessfield'] = chessfield
    data['player1'] = player1.to_dict()
    data['player2'] = player2.to_dict()

    storage.save_json(data)


def load_game():
    '''Converts the saved game data dicts into objects and returns them

    Arguments:
        --

    Returns:
        chessfield {list}, player1{obj}, player2{obj} -- game objects on successful load
        None, None, None -- error while loading

    '''
    resume_game_data = storage.load_json()

    if resume_game_data:

        player1_dict = resume_game_data['player1']
        player2_dict = resume_game_data['player2']
        chessfield = resume_game_data['chessfield']

        player1 = storage.load_player(player1_dict)
        player2 = storage.load_player(player2_dict)

        return chessfield, player1, player2

    return None, None, None


def main():
    '''Main method:
    contains the game procedure
    handles the user input
    load game or start new game
    saves the game automatically
    '''

    print("Willkommen beim")

    print(r"""    ____                                        __               __
   / __ )____ ___  _____  _________  __________/ /_  ____ ______/ /_ 
  / __  / __ `/ / / / _ \/ ___/ __ \/ ___/ ___/ __ \/ __ `/ ___/ __ \
 / /_/ / /_/ / /_/ /  __/ /  / / / (__  ) /__/ / / / /_/ / /__/ / / /
/_____/\__,_/\__,_/\___/_/  /_/ /_/____/\___/_/ /_/\__,_/\___/_/ /_/ 
"""


          )

    while True:

        print("Wollen Sie Ihr Spiel fortsetzen (f), oder ein neues Spiel beginnen?(n):", end=" ")

        user_input = input()

        # Resume saved game
        if user_input == "f":

            chessfield, player1, player2 = load_game()

            if chessfield is not None:
                print_chessfield(chessfield)
                break

            continue

        # start new game
        if user_input == "n":

            print("Neues Spiel wird geladen. Der Spielstand wird automatisch gespeichert, kein separates Speichern erforderlich.")
            chessfield = new_game()
            player1, player2 = create_player()
            print_chessfield(chessfield)
            break

        continue

    while True:

        if player1.turn:
            active_player = player1

        else:
            active_player = player2

        play_move(chessfield, active_player)

        player1.switch_turn()
        player2.switch_turn()

        print_chessfield(chessfield)
        save_game(chessfield, player1, player2)

        winner = check_winner(chessfield)

        if winner == active_player.color:
            print(active_player.name + " hat mit " +
                  active_player.color + " gewonnen!")

            storage.delete_json()

            print("Wollen Sie noch einmal spielen?(j/n):", end=" ")

            while True:

                game_new = input()

                if game_new == "j":
                    chessfield = new_game()
                    player1, player2 = create_player()
                    print_chessfield(chessfield)
                    break

                if game_new == "n":
                    return True

                print(
                    "Geben Sie entweder (j) für noch einmal spielen, oder (n) für aufhören!:", end=" ")


if __name__ == "__main__":
    main()
