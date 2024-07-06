from cards import *
import time
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
        self.players = {}
        self.deck = Deck(self)
        self.discardPile = DiscardedPile(self)
        self.current_player_index = 1
    def add_player(self, player):
        '''
        When adding new players, first create a player using the player class

        Then call this function, passing the new player object as a variable
        '''
        
        self.players[len(self.players)+1] = player
        self.room.append(player)
   
    
    def start_game(self):
        '''Call this function when the game is ready to start'''
        for player in self.players.values():
            player.setup()
        while True:
            current_player = self.players[self.current_player_index]
            if len(self.deck.getDeck()) == 0:
                
                self.deck.refillDeck(self.discardPile.getDeck())
                self.deck.shuffleDeck()
                

            print("-----\nPlayer number {}'s turn\n-----".format(str(self.current_player_index)))
            
            current_player.on_turn()
            
            
            self.checkEliminations()
            #win condition - all other players eliminated
            if len(self.players) == 1:
                print('Game over! Player {} has won the game!'.format(self.players.keys()[0]))
            
            self.current_player_index += 1
            if self.current_player_index > len(self.players):
                self.current_player_index = 1
    def checkEliminations(self):
        playersToEliminate = []
        for playerIndex, player in self.players.items():
                if player.health == 0:
                    print("Player {} has been eliminated!".format(playerIndex)) #announce a players death
                    playersToEliminate.append(playerIndex)
        for playerIndex in playersToEliminate:
            del self.players[playerIndex]
    def get_current_player(self):
        '''To get which player is currently performing actions'''
        return self.players[self.current_player_index]

    def get_next_player(self):
        next_index = self.current_player_index + 1
        if next_index > len(self.players):
            next_index = 1
        return self.players[next_index]

class Player():
    def __init__(self, game):
        self.game = game
        self.hand = Hand(self)
        self.effect_zone = EffectZone(self)
        self.equipment_zone = EquipmentZone(self)
        self.health = 0

    def setup(self):
        num_players = len(self.game.players)
        for _ in range(init_cards[num_players]):
            self.draw()
        self.updateHealth() #update health stat
    def updateHealth(self):
        #give health to each player
        self.health = 0
        for card in self.hand:
            
            self.health += card.health
    def on_turn(self):
        self.updateHealth()
        print("Current health: {}".format(self.health))
        print("Current effects:")
        if len(self.effect_zone) == 0:
            print("None")
        else:
            prettyprint(self.effect_zone)
        results = [Effects.on_effect() for Effects in self.effect_zone]
        
            
        if 'skip' in results:
            print('Player {}\'s turn skipped!'.format(self.game.current_player_index))
            pass
        else:
            drawCard = input(f'Press any key to draw a card : ') #just as an input - later used for frontend card drawing
            self.draw()
            prettyprint(self.hand)
            choice = int(input(f'choose from hand above\nCard number : '))
            print("Card choice")
            print(self.hand[choice-1].name)
            successful_play = False
            while not successful_play:
                successful_play = self.hand[choice-1].on_play()
            
    
        
    #actions which a player can do 


    def draw(self):
        card = self.game.deck.draw() #self.deck is a class - draws card from deck
        card.player = self #sets ownership of card to this player
        self.hand.append(card) #initialize each card object (self is the hand of the player who drew it and self.next is the next player)
   


class Hand(list):
    def __init__(self, player):
        self.game = player.game
        self.player = player
        self.name = 'hand'


class EffectZone(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'effect_zone'
    
class EquipmentZone(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'equipment_zone'
        
class Deck(list):
    def __init__(self, game):
        super().__init__()
        self.game = game
        
        # Populate deck with instances of cards
        for _ in range(6):
            self.append(seed_of_life(None))  # Assuming seed_of_life is a class and requires no arguments
        
        for _ in range(13):
            self.append(arrow_ice(None))  # Assuming arrow is a class and requires no arguments
        
        # Example of adding a variant
        card = seed_of_life(None)
        card.health += 1
        card.image += '_health'
        self.append(card)
        
        self.shuffleDeck()  # Optionally shuffle the deck after initialization

    def draw(self):
        if not self:
            raise IndexError("Deck is empty, cannot draw.")
        
        card_index = random.randint(0, len(self) - 1)
        card = self.pop(card_index)
        return card
    def refillDeck(self, cards):
        self += cards
    def shuffleDeck(self):
        random.shuffle(self)
    def getDeck(self):
        return self
class DiscardedPile(list):
    def __init__(self, game):
        self.game = game
        self.discardPile = []
    def getDeck(self):
        return self.discardPile
    


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
    