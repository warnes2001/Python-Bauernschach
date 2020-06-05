'''Player module: manages Player
'''


class Player():

    '''
    player class
    attributes: name, color, turn
    '''

    def __init__(self, name, color, turn):
        self.name = name
        self.color = color
        self.turn = turn

    def switch_turn(self):
        '''switches turn of player'''

        self.turn = not self.turn

    def to_dict(self):
        '''converting player objects to a dictionary'''

        return {
            'name': self.name,
            'color': self.color,
            'turn': self.turn,
        }

    @staticmethod
    def from_dict(player_dict):
        '''converting given dictionary into a player object and returns it'''

        return Player(
            player_dict.get('name'),
            player_dict.get('color'),
            player_dict.get('turn')
        )
