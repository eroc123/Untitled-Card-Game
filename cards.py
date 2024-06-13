
def prettyprint(l):
    for i in l:
        print(i.name, end=', ')
    print()

class Action:
    def remove(card, actor, bypass_effect=False) -> None: #remove card from any players hand
        '''
        Removes a card from any player's hand
        
        Inputs:
        - card : the card to remove
        - actor : who causes the card removal
        - bypass_effect : if true, skip checking for preventive effects
        '''
        if bypass_effect:
            card.on_discard(actor)
            card.hand.remove(card)
        else:
            # check for effects
            card.on_discard(actor)
            card.hand.remove(card)

    def choose(zone, actor) -> int: 
        '''
        Gets actor to choose a card from the zone
        
        returns n where n is the index of the choice
        '''
        prettyprint(zone)
        n = int(input(f'choose from deck above : '))
        return n - 1
    
    def choose_zone(player, actor):
        # idk let player choose a zone from a player
        n = 1
        zones = [player.hand, player.effect_zone, player.equipment_zone]
        return zones[n]
    
    def add_effect(card, player, actor):
        player.effect_zone.append(card)

    def remove_effect(card, player, actor):
        player.effect_zone.remove(card)

    def skip_action(player, actor):
        # skip player's next turn
        pass

    def draw_card(actor):
        actor.hand.draw()

    def move(card, origin, target, actor):
        target.append(card)
        origin.remove(card)

    def throw_error(card, message, action, actor):
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
    def __init__(self, hand):
        self.hand = hand
        
    def on_play(self,):
        Action.remove(self, actor=self.hand.player)

    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class arrow:
    name = 'Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand

    def on_play(self,):
        Action.remove(self, actor=self.hand.player)
        next_player = self.hand.player.game.get_next_player()
        n = Action.choose(next_player.hand, actor=self.hand.player)
        Action.remove(next_player.hand[n], actor=self.hand.player)

    def on_effect(self,): 
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class arrow_poison:
    name = 'Posion Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand

    def on_play(self,):
        Action.remove(self, actor=self.hand.player)
        next_player = self.hand.player.game.get_next_player()
        n = Action.choose(next_player.hand, actor=self.hand.player)
        Action.remove(next_player.hand[n], actor=self.hand.player)
        Action.add_effect(self, next_player, actor=self.hand.player)

    def on_effect(self,):
        n = Action.choose(self)
        Action.remove(n, self)
        Action.remove_effect(self, next_player.effect_zone)

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass
        
class arrow_fire:
    name = 'Fire Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand

    def on_play(self,):
        Action.remove(self, self.hand)
        next_player = self.hand.player.game.get_next_player()
        n = Action.choose(next_player.hand, self.hand.player)
        card = next_player.hand[n]
        if card.health == 1:
            # Choose another card
            n1 = Action.choose(next_player.hand)
            Action.remove(n, next_player.hand)
            Action.remove(n1, next_player.hand)
        else:
            Action.remove(n, next_player.hand)

    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class arrow_ice:
    name = 'Ice Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand

    def on_play(self,):
        Action.remove(self, self.hand)
        next_player = self.hand.player.game.get_next_player()
        n = Action.choose(next_player.hand)
        Action.remove(n, next_player.hand)
        Action.add_effect(self, next_player.effect_zone)
            
    def on_effect(self,):
        next_player = self.hand.player.game.get_next_player()
        Action.skip_action(next_player.hand)
        Action.remove_effect(self)

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass


class arrow_electric:
    name = 'Electric Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.hand = hand

    def on_play(self,):
        Action.remove(self, self.hand)
        next_player = self.hand.player.game.get_next_player()
        n = Action.choose(next_player.hand)
        Action.remove(next_player.hand[n], next_player.hand, actor = self.hand.player)
        # goofy method to get next next opponent
        n = Action.choose(next_player.hand[0].next)
        Action.remove(next_player.hand[n], next_player.hand, actor = self.hand.player)
            
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class arrow_electric_health(arrow_electric):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

class arrow_wind:
    name = 'Wind Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

    def on_play(self,):
        Action.remove(self, self.hand)
        n = Action.choose(next_player.hand)
        Action.remove(next_player.hand[n], next_player.hand, bypass_effect=True, actor = self.hand.player)
        
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class arrow_wind_health(arrow_wind):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

class extra_rations:
    name = 'Extra Rations'
    image = 'url/path'
    type = ['utility']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

    def on_play(self,):
        Action.remove(self, self.hand)
        Action.draw_card(self.hand)
        Action.draw_card(self.hand)
        
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class extra_rations_health(extra_rations):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

class spoiled_rations:
    name = 'Spoiled Rations'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

    def on_play(self,):
        Action.remove(self, self.hand)
        zone = Action.choose_zone(next_player)
        if zone.name == 'hand':
            n = Action.choose(zone)
            Action.remove(self.zone[n], self.zone, actor=self.hand.player)
        elif zone.name == 'equipment zone':
            n = Action.choose(zone)
            Action.remove(self.zone[n], self.zone, actor = self.hand.player)
        else:
            Action.throw_error(self, 'Invalid zone selected', 'on_play')
        
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass

class spoiled_rations_health(spoiled_rations):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

class spied_sucessfully:
    name = 'Spied sucessfully'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next

    def on_play(self,):
        Action.remove(self, self.hand)
        zone = Action.choose_zone(next_player)
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

    def on_discard(self, actor):
        pass

    def on_equip(self,):
        pass

class spied_sucessfully_health(spied_sucessfully):
    image = 'url/path'
    health = 1
    def __init__(self, hand, next):
        self.hand = hand
        next_player = next
