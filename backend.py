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
        self.deck = Deck([seed_of_life for i in range(number_of_players)] + [arrow for i in range(15)] + [arrow_wind_health for i in range(10)]) #create a random deck
        self.playerList = [Player(self.deck, number_of_players) for _ in range(number_of_players)] 
        self.turn = 0 
        self.currentPlayer = self.playerList[self.turn] #stores the player class of whoevers turn it is.
    def play(self, target):
        
        self.currentPlayer.hand[5].on_play(target) #plays a card
    
    def nextTurn(self,):
        self.turn += 1
        self.currentPlayer = self.playerList[self.turn]





class Action(): #second in the hiearchy, child class of gameloop
    def discard(self,card, hand, actor=None, bypass_effect=False) -> None: #remove card from any players hand
        if bypass_effect:
            card.on_discard(actor) #run the card discard code block
            
             #remove card from hand and place in discard pile
            hand.remove(card)
        else:
            # check for effects
            print(card)
            card.on_discard(actor) #remove card from hand and place in discard pile
            
            hand.remove(card)

    def choose(self, target) -> int: 
        # choose card to remove from player
        n = input("Pick one of the opponents' {} cards.".format(len(target.hand)))
        return int(n)
    
    def choose_zone(player):
        # idk let player choose a zone from a player
        n = 1
        zones = [player.hand, player.effect_zone, player.equipment_zone]
        return zones[n]
    
    def add_effect(card, effect_zone):
        effect_zone.append(card)

    def remove_effect(card, effect_zone):
        effect_zone.remove(card)

    def skip_self(player):
        # skip player's next turn
        pass

    def draw_card(hand):
        hand.draw()

    def move(card, origin, target):
        target.append(card)
        origin.remove(card)

    def throw_error(card, message, self):
        print(message)
        if self == 'on_play':
            card.on_play()
        elif self == 'on_effect':
            card.on_effect()
        elif self == 'on_discard':
            card.on_discard()
        elif self == 'on_equip':
            card.on_equip()
        else:
            print('you did WHAT?')
            print(f'self : {self}')

#########
# cards #
######### 

class seed_of_life(Action):
    name = 'Seed of Life'
    image = 'url/path'
    type = ['basic']
    health = 1
    def __init__(self, hand):
        self.hand = hand

        
    def on_play(self, target):
        print(self.hand)
        self.discard(self, self.hand)

    def on_effect(self, target):
        pass

    def on_discard(self, target):
        pass

    def on_equip(self, target):
        pass

class arrow(Action):
    name = 'Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        print(self.hand)
        
        self.discard(self, self.hand)

        n = self.choose(target)
        self.discard(self.next.hand[n], self.next.hand, actor = self.hand.player)

    def on_effect(self, target): 
        pass

    def on_discard(self, target):
        pass

    def on_equip(self, target):
        pass

class arrow_health(arrow):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand


class arrow_poison(Action):
    name = 'Posion Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        self.discard(self, self.hand)
        n = self.choose(self.next.hand)
        self.discard(self.next.hand[n], self.next.hand, actor = self.hand.player)
        self.add_effect(self, self.next.effect_zone)

    def on_effect(self, target):
        n = self.choose(self)
        self.discard(n, self)
        self.remove_effect(self, self.next.effect_zone)

    def on_discard(self, card, target):
        pass

    def on_equip(self, target):
        pass

class arrow_poison_health(arrow_poison):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand

        
class arrow_fire(Action):
    name = 'Fire Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        self.discard(self, self.hand)
        n = self.choose(self.next.hand)
        card = self.next.hand[n]
        if card.health == 1:
            # Choose another card
            n1 = self.choose(self.next.hand)
            self.discard(n, self.next.hand)
            self.discard(n1, self.next.hand)
        else:
            self.discard(n, self.next.hand)

    def on_effect(self, target):
        pass

    def on_discard(self, card, target):
        pass

    def on_equip(self, target):
        pass

class arrow_fire_health(arrow_fire):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand
  

class arrow_ice(Action):
    name = 'Ice Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand
       

    def on_play(self, target):
        self.discard(self, self.hand)
        n = self.choose(self.next.hand)
        self.discard(n, self.next.hand)
        self.add_effect(self, self.next.effect_zone)
            
    def on_effect(self, target):
        self.skip_self(self.next.hand)
        self.remove_effect(self)

    def on_discard(self, card, target):
        pass

    def on_equip(self, target):
        pass

class arrow_ice_health(arrow_ice):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand
       

class arrow_electric(Action):
    name = 'Electric Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand
        

    def on_play(self, target):
        self.discard(self, self.hand)
        n = self.choose(self.next.hand)
        self.discard(self.next.hand[n], self.next.hand, actor = self.hand.player)
        # goofy method to get next next opponent
        n = self.choose(self.next.hand[0].next)
        self.discard(self.next.hand[n], self.next.hand, actor = self.hand.player)
            
    def on_effect(self, target):
        pass

    def on_discard(self, target):
        pass

    def on_equip(self, target):
        pass

class arrow_electric_health(arrow_electric):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand


class arrow_wind(Action):
    name = 'Wind Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        print(self.hand)
        self.discard(self, self.hand)
        
        n = self.choose(target)
        self.discard(self.target[n], self.target, bypass_effect=True, actor = self.hand.player)
        
    def on_effect(self, target):
        pass

    def on_discard(self, target):
        pass

    def on_equip(self, target):
        pass

class arrow_wind_health(arrow_wind):
    image = 'url/path'
    health = 1
    
    def __init__(self, hand):
        
        self.hand = hand


class extra_rations(Action):
    name = 'Extra Rations'
    image = 'url/path'
    type = ['utility']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        self.discard(self, self.hand)
        self.draw_card(self.hand)
        self.draw_card(self.hand)
        
    def on_effect(self, target):
        pass

    def on_discard(self, card, target):
        pass

    def on_equip(self, target):
        pass

class extra_rations_health(extra_rations):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand


class spoiled_rations(Action):
    name = 'Spoiled Rations'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        self.discard(self, self.hand)
        zone = self.choose_zone(self.next)
        if zone.name == 'hand':
            n = self.choose(zone)
            self.discard(self.zone[n], self.zone, actor=self.hand.player)
        elif zone.name == 'equipment zone':
            n = self.choose(zone)
            self.discard(self.zone[n], self.zone, actor = self.hand.player)
        else:
            self.throw_error(self, 'Invalid zone selected', 'on_play')
        
    def on_effect(self, target):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self, target):
        pass

class spoiled_rations_health(spoiled_rations):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand


class spied_sucessfully(Action):
    name = 'Spied sucessfully'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand):
        self.hand = hand


    def on_play(self, target):
        self.discard(self, self.hand)
        zone = self.choose_zone(target)
        if zone.name == 'hand':
            n = self.choose(zone)
            self.move(self.zone[n], self.zone, self.hand)
        elif zone.name == 'equipment zone':
            n = self.choose(zone)
            self.move(self.zone[n], self.zone, self.hand)
        else:
            self.throw_error(self, 'Invalid zone selected', 'on_play')
        
    def on_effect(self, target):
        pass

    def on_discard(self, target):
        pass

    def on_equip(self, target):
        pass

class spied_sucessfully_health(spied_sucessfully):
    image = 'url/path'
    health = 1
    def __init__(self, hand):
        self.hand = hand

if __name__ == '__main__':
    game = GameLoop(2)
    game.play( game.playerList[1])
