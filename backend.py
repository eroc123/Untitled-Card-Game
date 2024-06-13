from cards import *

#Basic game rules explanation
'''
Card types:
 * Basic - common card type i am guessing 
 * Utility - does stuff with deck and messes with ppl. may also remove or add effects to people
 * Targeting - attacks other players
'''


import random


init_cards = {
    2:9,
    3:8,
    4:7,
    5:6,
    6:5,
}

class Game():
    def __init__(self):
        '''Sets up a new game environment'''
        self.room = []
        self.players = []
        self.deck = Deck()
        self.current_player_index = 0

    def add_player(self, player):
        '''
        When adding new players, first create a player using the player class

        Then call this function, passing the new player object as a variable
        '''
        
        self.players.append(player)
        self.room.append(player)
        print(len(self.players))
    
    def start_game(self):
        '''Call this function when the game is ready to start'''
        for player in self.players:
            player.setup()
        while True:
            current_player = self.players[self.current_player_index]
            current_player.on_turn()
            self.current_player_index += 1
            if self.current_player_index == len(self.players):
                self.current_player_index = 0
            
    def get_current_player(self):
        '''To get which player is currently performing actions'''
        return self.players[self.current_player_index]

    def get_next_player(self):
        next_index = self.current_player_index + 1
        if next_index == len(self.players):
            next_index = 0
        return self.players[next_index]

class Player():
    def __init__(self, game):
        self.game = game
        self.hand = Hand(self)
        self.effect_zone = EffectZone(self)
        self.equipment_zone = EquipmentZone(self)

    def on_turn(self):
        prettyprint(self.hand)
        choice = int(input(f'choose from deck above\nCard number : '))
        self.hand[choice].on_play()


    def setup(self):
        self.hand.setup()

class Hand(list):
    def __init__(self, player):
        self.game = player.game
        self.player = player
        self.name = 'hand'

    def setup(self):
        num_players = len(self.game.players)
        for _ in range(init_cards[num_players]):
            self.draw()

    def draw(self,):
        card = self.game.deck.draw() #self.deck is a class - draws card from deck
        self.append(card(self)) #initialize each card object (self is the hand of the player who drew it and self.next is the next player)

class EffectZone(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'effect zone'
    
class EquipmentZone(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'equipment zone'
        
class Deck(list):
    def __init__(self,):
        # fill up deck, this is just random numbers not the final
        [self.append(seed_of_life) for _ in range(4)]
        [self.append(arrow) for _ in range(13)]
        # for health varients, e.g.
        card = seed_of_life
        card.health += 1
        card.image += '_health' # etc 
        self.append(card)
        
        
    def draw(self,):
        card_index = random.randint(0,len(self)-1)
        card = self[card_index]
        self.pop(card_index)
        return card
    



# testing code below

def prettyprint(l):
    for i in l:
        print(i.name, end=', ')
    print()


if __name__ == '__main__':
    new_game = Game()
    player1 = Player(new_game)
    player2 = Player(new_game)
    new_game.add_player(player1)
    new_game.add_player(player2)
    new_game.start_game()
    