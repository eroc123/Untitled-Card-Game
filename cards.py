
def prettyprint(l):
    for i in l:
        print(i.name, end=', ')
    print()

class Action:
    def remove(target, actor, card, bypass_effect=False) -> None: #remove card from any players hand
        '''
        Removes a card from any player's hand
        
        Inputs:
        - card : the card to remove
        - actor : who causes the card removal
        - bypass_effect : if true, skip checking for preventive effects
        '''
        if bypass_effect:
            card.on_discard(target)
            actor.game.discardPile.discardPile.append(card) #add card to discard pile
            target.hand.remove(card)
        else:
            # check for effects
            card.on_discard(target)
            actor.game.discardPile.discardPile.append(card) #add card to discard pile
            target.hand.remove(card)
    def drawCard(actor):
        actor.draw()
    def chooseCard(target, zone) -> int: 
        '''
        Gets actor to choose a card from the zone
        
        returns n where n is the index of the choice
        '''
        if zone == 'hand':
            print(["*" for _ in target.hand]) #hide target players deck, framework for later use by frontend
            n = int(input(f'choose from deck above : '))
        elif zone == 'equipment_zone':
            print(["*" for _ in target.equipment_zone]) #hide target players deck, framework for later use by frontend
            n = int(input(f'choose from equipment deck above : '))
        return n - 1
    def chooseTarget(actor):
        choice = input('Choose a target from these players: {}'.format(prettyprint(actor.game.players))) #choice is integer determining index of chosen target
        return int(choice)-1

    def choose_zone(target):
        # idk let player choose a zone from a player
        zone = input("Choose a zone (hand/equipment)") #return as string
        if zone == 'hand':
            return target.hand
        elif zone == 'equipment':
            return target.equipment_zone
         
    def add_effect(target, card):
        target.effect_zone.append(card)

    def remove_effect(target, card):
        target.effect_zone.remove(card)

    def skip_action(target, actor):
        # skip player's next turn
        pass
    def checkRetaliation(target,actor):
        pass #check whether target has a retaliation card and ask them whether they want to use it. If used, effect negated on utility targetting cardss
        
    def move(target, actor, card):
        target.append(card)
        actor.remove(card)

    def throw_error(target, action, card, message):
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
    def __init__(self, player):
        self.player = player
    def on_play(self,):
        Action.remove(target=self.player, actor=self.player, card=self)
        return True
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
    def __init__(self, player):
        self.player = player #actor is player, target is player where the action is being performed

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
        next_player = self.player.game.get_next_player()
        n = Action.chooseCard(target=self.player, zone='hand')
        Action.remove(target=next_player,actor=self.player,card=next_player.hand[n])
        return True
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
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
        next_player = self.player.game.get_next_player()
        n = Action.chooseCard(target=next_player, zone='hand')
        Action.remove(target=next_player,actor=self.player,card=next_player.hand[n])
        Action.add_effect(target=next_player, action=self.player, card=self)
        self.player = self.next_player #change ownership of card to whoever recieved the effect
        return True
    def on_effect(self, ):
        n = Action.chooseCard(target=self.player, zone=self.player.hand)
        Action.remove(target=self.player, actor=self.player, card=self.player.hand[n])
        Action.remove_effect(target=self.player, card=self)
        
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
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
        next_player = self.player.game.get_next_player()
        n = Action.chooseCard(target=next_player, zone='hand')
        if next_player.hand[n].health == 1:
            # Choose another card
            n1 = Action.chooseCard(target=next_player, zone='hand')
            Action.remove(target=next_player,actor=self.player,card=next_player.hand[n])
            Action.remove(target=next_player,actor=self.player,card=next_player.hand[n1])
        else:
            Action.remove(target=next_player,actor=self.player,card=next_player.hand[n])
        return True
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
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
        next_player = self.player.game.get_next_player()
        n = Action.chooseCard(target=next_player, zone='hand')
        Action.remove(target=next_player,actor=self.player,card=next_player.hand[n])
        
        Action.add_effect(target=next_player,  card=self)
        self.player = next_player #change ownership of card to whoever recieved the effect
        return True
    def on_effect(self,):
        Action.remove_effect(target=self.player, card=self)
        return 'skip' #skip turn
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
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
        next_player = self.player.game.get_next_player() #get next two opponents 
        n = Action.chooseCard(target=next_player, zone='hand')
        Action.remove(target=next_player,actor=self.player,card=next_player.hand[n])

        if len(self.player.game.players) > 2: #if there are more than 2 opponents
            next_next_player = next_player.game.get_next_player() 
            n1 = Action.chooseCard(target=next_next_player, zone='hand')
            Action.remove(next_next_player.hand[n1], next_next_player.hand, actor = self.player)
        else:
            n = Action.chooseCard(target=next_player, zone='hand') #else remove a second card from opponent
            Action.remove(next_player.hand[n], next_player.hand, actor = self.player)
        return True
            
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass


class arrow_wind:
    name = 'Wind Arrow'
    image = 'url/path'
    type = ['basic', 'targeting']
    health = 0
    def __init__(self, hand):
        self.player = hand
      

    def on_play(self,): #basically same as basic except bypass all effects
        Action.remove(target=self.player,actor=self.player, card=self)
        next_player = self.player.game.get_next_player()
        n = Action.chooseCard(target=self.player, zone='hand')
        Action.remove(target=next_player,actor=self.player,card=next_player.hand[n], bypass_effect=True)
        return True
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass



class extra_rations:
    name = 'Extra Rations'
    image = 'url/path'
    type = ['utility']
    health = 0
    def __init__(self, hand):
        self.player = hand
        next_player = next

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
        Action.drawCard(actor=self.player)
        return True
        
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass


class spoiled_rations:
    name = 'Spoiled Rations'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand):
        self.player = hand

    def on_play(self,):
        spyingFailedInHand = False
        for card in self.player.hand: #condition states that this card cannot be played if a spying failed card is in the players hand
            if card.name == "Spying Failed":
                spyingFailedInHand = True
                break

        if spyingFailedInHand:
            return False
        else:
            Action.remove(target=self.player,actor=self.player, card=self)
            next_player = self.player.game.get_next_player()
            zone = Action.choose_zone(target=next_player)

            n = Action.chooseCard(target=next_player, zone=zone.name)
            RetaliationPlayed = Action.checkRetaliation(target=next_player,actor=self.player)
            
            Action.remove(target=next_player,actor=self.player,card=zone[n])
            return True


        
    def on_effect(self,):
        pass

    def on_discard(self, card):
        pass

    def on_equip(self,):
        pass


class spied_sucessfully:
    name = 'Spied sucessfully'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand):
        self.player = hand

    def on_play(self,):
        spyingFailedInHand = False
        for card in self.player.hand: #condition states that this card cannot be played if a spying failed card is in the players hand
            if card.name == "Spying Failed":
                spyingFailedInHand = True
                break

        if spyingFailedInHand:
            return False
        else:
            Action.remove(target=self.player,actor=self.player, card=self)
            next_player = self.player.game.get_next_player()
            zone = Action.choose_zone(target=next_player)
            n = Action.chooseCard(target=next_player, zone=zone.name)

            
            Action.move(target=next_player,actor=self.player,card=zone[n])
            return True
    def on_effect(self,):
        pass

    def on_discard(self, actor):
        pass

    def on_equip(self,):
        pass

class spying_failed:
    name = 'Spying Failed'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand):
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
    
    def on_effect(self,):
        pass

    def on_discard(self, actor):
        Action.drawCard(actor=self.player)
        Action.drawCard(actor=self.player)

    def on_equip(self,):
        pass


class spying_failed:
    name = 'Spying Failed'
    image = 'url/path'
    type = ['utility']
    health = 0
    def __init__(self, hand):
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)
    
    def on_effect(self,):
        pass

    def on_discard(self, actor):
        Action.drawCard(actor=self.player)
        Action.drawCard(actor=self.player)

    def on_equip(self,):
        pass

class retaliation:
    name = 'Spying Failed'
    image = 'url/path'
    type = ['utility', 'targetting']
    health = 0
    def __init__(self, hand):
        self.player = hand

    def on_play(self,):
        Action.remove(target=self.player,actor=self.player, card=self)

    def on_effect(self,):
        pass

    def on_discard(self, actor):
        pass

    def on_equip(self,):
        pass



