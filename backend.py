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


class DiscardedPile():
    pass

class Player():
    def __init__(self, deck, num_players):
        self.hand = Hand(deck) #handd of a player 
        self.effect_zone = EffectZone(deck)
        self.equipment_zone = EquipmentZone(deck)
        #hands out cards to each players (dependent on number of players)
        self.hand.setup(num_players, None, self)

class Hand(list):
    def __init__(self, player):
        self.game = player.game
        self.player = player
        self.name = 'hand'

    def setup(self, num_players, target, player):
        self.num_players = num_players
        self.target = target
        self.player = player
        for i in range(init_cards[num_players]):
            self.draw()

    def draw(self,):
        card = self.deck.draw() #self.deck is a class - draws card from deck
        self.append(card(self)) #initialize each card object (self is the hand of the player who drew it and self.next is the next player)

class EffectZone(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'effect_zone'
    
class EquipmentZone(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'equipment_zone'
        
class Deck(list):
    def __init__(self, cards): #cards is a list of all cards to fill deck with
        # fill up deck using list of cards provided
        super().__init__(cards)

    def shuffle(self,): #shuffles the deck
        random.shuffle(self)
    def draw(self,):
        print(len(self)-1)
        card_index = random.randint(0,len(self)-1)
        card = self[card_index]
        self.pop(card_index)
        return card
    def discard(self, card): #discarded cards immediately placed back in the deck in a random position
        self.insert(random.randint(0,(len(self)-1)), card)
    


#actual meat of the code


#target is a player object 


class GameLoop(): #top level class
    
    def __init__(self, number_of_players) -> None: #sets up game and players and stuff
        self.deck = Deck([seed_of_life for i in range(number_of_players)] + [arrow for i in range(15)] + [arrow_wind for i in range(10)]) #create a random deck
        self.playerList = [Player(self.deck, number_of_players) for _ in range(number_of_players)] 
        self.turn = 0 
        self.currentPlayer = self.playerList[self.turn] #stores the player class of whoevers turn it is.
    def play(self, target):
        
        self.currentPlayer.hand[5].on_play(target) #plays a card
    
    def nextTurn(self,):
        self.turn += 1
        self.currentPlayer = self.playerList[self.turn]

    
if __name__ == '__main__':
    game = GameLoop(2)
    game.play( game.playerList[1])