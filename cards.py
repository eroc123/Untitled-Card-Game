import random
import socket
init_cards = {
    2:9,
    3:8,
    4:7,
    5:6,
    6:5,
}
class Hand(list):
    def __init__(self, deck):
        self.deck = deck
    def setup(self, num_players, next):
        self.next = next
        for i in range(init_cards[num_players]):
            self.draw()
    def draw(self,):
        card = self.deck.draw()
        self.append(card(self, self.next))

class EffectZone(list):
    def __init__(self, deck):
        self.deck = deck

class EquipmentZone(list):
    def __init__(self, deck):
        self.deck = deck
        
class Deck(list):
    def __init__(self,):
        # fill up deck
        [self.append(seed_of_life) for i in range(6)]
        [self.append(arrow) for i in range(13)]
        [self.append(arrow_health) for i in range(2)]
    def draw(self,):
        card_index = random.randint(0,len(self)-1)
        card = self[card_index]
        self.pop(card_index)
        return card

class Action:
    def remove(card, hand):
        hand.remove(card)
    def choose(hand):
        # idk let player choose a card from a hand
        n = 1
        return n

    
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
    type = ['basic']
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

class arrow_health:
    name = 'Arrow'
    image = 'url/path'
    type = ['basic']
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next
    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(n, self.next.hand)
    def on_effect(self,):
        pass
    def on_discard(self,):
        pass
    def on_equip(self,):
        pass

class arrow_poison:
    name = 'Posion Arrow'
    image = 'url/path'
    type = ['basic']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next
    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next.hand)
        Action.remove(n, self.next.hand)
        Action.effect(self.next.hand)
    def on_effect(self,):
        n = Action.choose(self)
        Action.remove(n, self)
    def on_discard(self,):
        pass
    def on_equip(self,):
        pass

class arrow_poison_health:
    name = 'Posion Arrow'
    image = 'url/path'
    type = ['basic']
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        self.next = next
    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(self.next)
        Action.remove(n, self.next)
    def on_effect(self,):
        pass
    def on_discard(self,):
        pass
    def on_equip(self,):
        pass

class Player():
    def __init__(self, deck):
        self.hand = Hand(deck)
        self.effect_zone = EffectZone(deck)
    def setup(self, num_players, next):
        self.hand.setup(num_players, next)

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