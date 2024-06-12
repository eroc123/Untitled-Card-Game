import cards
import random
init_cards = {
    2:9,
    3:8,
    4:7,
    5:6,
    6:5,
}
class Hand(list):
    def __init__(self,num_players):
        
        for i in range(init_cards[num_players]):
            self.draw()
    def draw(self,):
        card = cards.Deck.draw()
        self.append(card)



'''
class effectZone:

class equipmentZone:
'''
cards.Deck()
c = Hand(2)
print(c)

