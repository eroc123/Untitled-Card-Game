## CARDS ##

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

class Player():
    def __init__(self, deck):
        self.hand = Hand(deck)
        self.effect_zone = EffectZone(deck)
        self.equipment_zone = EquipmentZone(deck)

    def setup(self, num_players, next):
        self.next = next
        self.hand.setup(num_players, next)

class Hand(list):
    def __init__(self, deck):
        self.deck = deck
        self.name = 'hand'

    def setup(self, num_players, next):
        self.num_players = num_players
        self.next = next
        for i in range(init_cards[num_players]):
            self.draw()

    def draw(self,):
        card = self.deck.draw() #self.deck is a class - draws card from deck
        self.append(card(self, self.next)) #initialize each card object (self is the hand of the player who drew it and self.next is the next player)

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
        [self.append(seed_of_life) for _ in range(6)]
        [self.append(arrow) for _ in range(13)]
        [self.append(arrow_health) for _ in range(2)]
        
    def draw(self,):
        card_index = random.randint(0,len(self)-1)
        card = self[card_index]
        self.pop(card_index)
        return card
    

class Action:
    def remove(card, hand, bypass_effect = False) -> None:
        if bypass_effect:
            hand.remove(card)
        else:
            # check for effects
            hand.remove(card)

    def choose(zone) -> int: 
        # idk let player choose a card from a zone
        n = 1
        return n
    
    def choose_zone(player):
        # idk let player choose a zone from a player
        n = 1
        zones = [player.hand, player.effect_zone, player.equipment_zone]
        return zones[n]
    
    def add_effect(card, effect_zone):
        effect_zone.append(card)

    def remove_effect(card, effect_zone):
        effect_zone.remove(card)

    def skip_action(player):
        # skip player's next turn
        pass

    def draw_card(hand):
        hand.draw()

    def move(card, origin, target):
        target.append(card)
        origin.remove(card)

    def throw_error(card, message, action):
        print(message)
        if action == 'on_play':
            card.on_play()
        elif action == 'on_effect':
            card.on_effect()
        elif action == 'on_discard':
            card.on_discard()
        elif action == 'on_equip':
            card.on_equip()
        else:
            print('you did WHAT?')
            print(f'action : {action}')
        


#########
# cards #
######### 



class seed_of_life:
    name = 'Seed of Life'
    image = 'url/path'
    type = ['basic']
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next.hand
        
    def on_play(self,):
        Action.remove(self, self.hand)

    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass


class arrow:
    name = 'Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(self.next.hand[n], self.next.hand)

    def on_effect(self,): 
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass


class arrow_health(arrow):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next


class arrow_poison:
    name = 'Posion Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(self.next.hand[n], self.next.hand)
        Action.add_effect(self, self.next.effect_zone)

    def on_effect(self,):
        n = Action.choose(self)
        Action.remove(n, self)
        Action.remove_effect(self, self.next.effect_zone)

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class arrow_poison_health(arrow_poison):
    image = 'url/path'
    health = 1
    def __init__(self, hand: Hand, next: Hand):
        self.hand = hand
        self.next = next
        

class arrow_fire:
    name = 'Fire Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        card = self.next.hand[n]
        if card.health == 1:
            # Choose another card
            n1 = Action.choose(self.next.hand)
            Action.remove(n, self.next.hand)
            Action.remove(n1, self.next.hand)
        else:
            Action.remove(n, self.next.hand)

    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class arrow_fire_health(arrow_fire):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

class arrow_ice:
    name = 'Ice Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(n, self.next.hand)
        Action.add_effect(self, self.next.effect_zone)
            
    def on_effect(self,):
        Action.skip_action(self.next.hand)
        Action.remove_effect(self)

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class arrow_ice_health(arrow_ice):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next


class arrow_electric:
    name = 'Electric Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(self.next.hand[n], self.next.hand)
        # goofy method to get next next opponent
        n = Action.choose(self.next.hand[0].next)
        Action.remove(self.next.hand[n], self.next.hand)
            
    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class arrow_electric_health(arrow_electric):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next


class arrow_wind:
    name = 'Wind Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(self.next.hand[n], self.next.hand, bypass_effect=True)
        
    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class arrow_wind_health(arrow_wind):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

class extra_rations:
    name = 'Extra Rations'
    image = 'url/path'
    type = ['utility']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        Action.draw_card(self.hand)
        Action.draw_card(self.hand)
        
    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class extra_rations_health(extra_rations):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

class spoiled_rations:
    name = 'Spoiled Rations'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

    def on_play(self,):
        Action.remove(self, self.hand)
        zone = Action.choose_zone(self.next)
        if zone.name == 'hand':
            n = Action.choose(zone)
            Action.remove(self.zone[n], self.zone)
        elif zone.name == 'equipment zone':
            n = Action.choose(zone)
            Action.remove(self.zone[n], self.zone)
        else:
            Action.throw_error(self, 'Invalid zone selected', 'on_play')
        
    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

class spoiled_rations_health:
    image = 'url/path'
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next

class spied_sucessfully:
    name = 'Spied sucessfully'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def on_play(self,):
        Action.remove(self, self.hand)
        zone = Action.choose_zone(self.next)
        if zone.name == 'hand':
            n = Action.choose(zone)
            Action.move(self.zone[n], self.zone, self.hand)
        elif zone.name == 'equipment zone':
            n = Action.choose(zone)
            Action.move(self.zone[n], self.zone, self.hand)
        else:
            Action.throw_error(self, 'Invalid zone selected', 'on_play')
        
    def on_effect(self,):
        pass

    def on_discard(self,):
        pass

    def on_equip(self,):
        pass

# testing code below

def prettyprint(l):
    for i in l.hand:
        print(i.name, end=', ')
    print()


if __name__ == '__main__':
    c = Deck()
    d1 = Player(c)
    d2 = Player(c)
    d1.setup(2, d2)
    d2.setup(2, d1)
    prettyprint(d1)
    prettyprint(d2)
    d1.hand[5].on_play()
    prettyprint(d1)
    prettyprint(d2)
    