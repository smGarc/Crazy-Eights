# Crazy Eights Game by Simon Garcia
'''
How to Play Crazy Eights:

Each player is dealt 5 cards. The player that reaches 0 cards first wins.
There are two stacks of cards:
    1. The Deck that cards are dealt from and players draw from
    2. "Card in Play" Deck; cards placed down from players, including the initial card

When it is a player's turn, they can choose to play a card from their deck 
if it matches the following criteria:
    1. Matches the rank (number) of the Card in Play
    2. Matches the suit of the Card in Play
    3. Any card that is rank 8, which allows the player to change the suit

If none of the criteria matches the player's cards to the card in play, 
the player must draw from the deck until a match is found.
'''
# Make the game easier to follow by slowing it down in some spots
import time
def pause():
    time.sleep(1)

class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades", "None"] # Added a "None" suit because I needed a blank card for drawing from a deck
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
    "King"]
    def __init__(self, suit = 0, rank = 2):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        if self.rank_list[self.rank] == "None" or self.suit_list[self.suit] == "None":
            return "Joker"
        return (self.rank_list[self.rank] + " of " + self.suit_list[self.suit])
    def __eq__(self, other):
        return (self.rank == other.rank and self.suit == other.suit)
    def __gt__(self, other):
        if self.suit > other.suit:
            return True
        elif self.suit == other.suit:
            if self.rank > other.rank:
                return True
        return False
    def get_suit(self): # Returns the suit of the card
        return self.suit
    def get_rank(self): # Returns the rank of the card
        return self.rank
    def valid_play(self, hand_card): # Determines whether a card can be played validly
        if hand_card.get_rank() == self.get_rank() or hand_card.get_suit() == self.get_suit():
            return True
        return False

import random
class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
    def __str__(self):
        S = ""
        for i in range(len(self.cards)):
            S += str(i) + ": " + str(self.cards[i]) + "\n"
        return S
    def shuffle(self):
        random.shuffle(self.cards) # Fisher-yates algorithm? Better than our example above
    def pop_card(self):
        return self.cards.pop()
    # Checks if the deck is empty and needs to refill
    def is_empty(self): 
        return len(self.cards) == 0
    def deal(self, hands, stock):
        n_players = len(hands)
        for i in range(5):
            for j in range(n_players):
                card = self.pop_card()
                current_player = j
                hands[current_player].add_card(card)
        card = self.pop_card()
        stock.add_card(card)
    # Refills the deck with the cards in the stock pile and reshuffles it
    def refill(self, stock): 
        print("Deck ran out... Refilling from Card in Play deck and shuffling...")
        self.cards = stock.get_cards()
        self.shuffle()
        stock.empty()
    # Makes the user draw a card from the deck until they get a valid card to play
    def draw_until(self, top_card, hand):
        card = Card(4,0) # Empty card 
        # Checks if the deck has enough cards to draw from
        if len(self.cards) == 1: 
            return False 
        # If the deck has too little cards, it returns false to tell the game that 
        # it doesn't have enough cards, then it refills the deck with cards from 
        # the stock pile
        cards_drawn = 0
        while True: 
            card = self.pop_card()
            cards_drawn += 1
            if hand.get_name() == "You":
                pause()
                print("You drew the " + str(card))
            else:
                pause()
                print(hand.get_name() + " drew a card")
                if cards_drawn > 3: # Gives the computers a bit of personality
                    if random.randrange(0,2) == 1: 
                        phrase = random.randrange(0, 4)
                        # There's a chance they say one of these phrases if they 
                        # draw more than 3 cards at a time
                        if phrase == 0: 
                            print(hand.get_name() + " says: \"Ugh, seriously?\"")
                        elif phrase == 1:
                            print(hand.get_name() + " says: \"Come on!\"")
                        elif phrase == 2:
                            print(hand.get_name() + " says: \"Aww man...\"")
                        else:
                            print(hand.get_name() + " says: \"Sigh...\"")
            hand.add_card(card)
            if card.valid_play(top_card) or card.get_rank() == 8:
                return True
            if len(self.cards) == 1:
                return False
        return True

class Hand(Deck):
    def __init__(self, name = ""):
        self.cards = []
        self.name = name
    def add_card(self, card):
        self.cards.append(card)
    def __str__(self):
        if self.name == "You":
            S = "Your hand "
        else: 
            S = self.name + "'s hand "
        if self.is_empty():
            S += "is empty\n"
        else: 
            S += "contains:\n" + Deck.__str__(self)
        S += str(len(self.cards)) + ": Draw from Stock Pile"
        return S
    # Get hand's name
    def get_name(self):
        return self.name
    # Get card in specific index in hand
    def get_card(self, card_index):
        return self.cards[card_index]
    # Get the amount of cards in hand
    def get_len(self):
        return len(self.cards)
    def pop_card(self, index):
        return self.cards.pop(index)
    # Determine whether the hand is out of cards and satisfies win condition
    def win(self):
        if len(self.cards) == 0:
            return True
        return False

# Class for the deck of cards people put down I called "Stock"
class Stock(Deck): # It inherits some Deck functions
    # Initializes itself with an empty array of cards 
    def __init__(self):
        self.cards = []
    # Add card function for when a player puts down a card
    def add_card(self, card):
        self.cards.append(card)
    # Function to check what card is on top of the stack, so that the game can check
    # if the player is choosing a valid card
    def top_card(self):
        return self.cards[-1]
    # Prints only the top card
    def __str__(self):
        S = ""
        S += str(self.cards[-1]) + "\n"
        return S
    # Get all the cards except the last one, so that the cards can be reshuffled into
    # the deck if the deck ran out of cards
    def get_cards(self):
        return self.cards[:-1]
    # Empties the stock after the cards are copied back into the Deck after reshuffling
    def empty(self):
        self.cards = self.cards[-1:]

# Class for the Game
class CrazyEights:
    # Initializes itself with a deck, shuffles that deck, 
    # and initializes a "stock" pile, which is the pile of cards people put down
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.stock = Stock()
    # Deals cards to the players
    def deal(self, hands):
        self.deck.deal(hands, self.stock)
    # Starts the game and plays it out until someone wins
    def start(self, hands):
        player_turn = 0
        rounds = 1
        win = False
        while (not win): # Keeps going until someone places down all their cards
            if player_turn == 0:
                print("\nRound " + str(rounds))
                print("Card in Play:\n", self.stock)
            else:
                print("\nCard in Play:\n", self.stock)
            pause()
            if player_turn == 0:
                self.player_turn(hands[0])
            else:
                self.com_turn(hands[player_turn])
            if hands[player_turn].win(): # Checks if the player won during their turn
                win = True
                if hands[player_turn].get_name() == "You":
                    print(hands[player_turn].get_name() + " win!")
                else:
                    print(hands[player_turn].get_name() + " wins!")
                quit() # Exits the program   
            player_turn += 1 # Moves onto next player
            if player_turn == len(hands): # Resets to player 0 if the player_turn is bigger
                player_turn = 0
                rounds += 1
    
    # Player's turn
    def player_turn(self, hand):
        print("Your Turn...\nPick one of your cards")
        print(hand)
        index = input("Chosen card: ")
        while(True):
            # If unvalid card picked 
            if int(index) > hand.get_len() or int(index) < 0:
                print("That's not a valid option!\nType the number corresponding to a card or draw from the deck.")
                index = input("Chosen card: ")
            # If draw from deck is chosen
            elif hand.get_len() == int(index):
                print("Drawing from deck until a playable card is found...")
                while not self.deck.draw_until(self.stock.top_card(), hand):
                    self.deck.refill(self.stock)
                card = hand.pop_card(-1)
                if card.get_rank() == 8:
                    new_suit = input("0: Clubs, 1: Diamonds, 2: Hearts, 3: Spades\nPick a suit: ")
                    card = Card(int(new_suit), 8)
                self.stock.add_card(card)
                break
            # If a card with rank 8 is chosen
            elif hand.get_card(int(index)).get_rank() == 8:
                new_suit = input("0: Clubs, 1: Diamonds, 2: Hearts, 3: Spades\nPick a suit: ")
                hand.pop_card(int(index)) # Remove card from hand
                card = Card(int(new_suit), 8) # Change suit of card
                self.stock.add_card(card) # Add card to pile
                break
            # If a valid card is chosen
            elif self.stock.top_card().valid_play(hand.get_card(int(index))):
                card = hand.pop_card(int(index)) # Remove card from hand
                self.stock.add_card(card) # Add card to pile
                break
            else: # A non-valid card is chosen
                print("The " + str(hand.get_card(int(index))) + " is not a playable card!\nPick another one, or draw from the deck.")
                index = input("Chosen card: ")
        print("You put down the " + str(card))
    
    # Computer's turn
    def com_turn(self, hand):
        print(hand.get_name() + "'s Turn...")
        # Print number of cards in Computer's hand so Player knows how many
        if hand.get_len() == 1:
            print(hand.get_name() + "'s hand contains: " + str(hand.get_len()) + " card.")
        else:
            print(hand.get_name() + "'s hand contains: " + str(hand.get_len()) + " cards.")
        if hand.get_len() < 4:
            # Give computer chance to say something if they're close to winning
            if random.randrange(0,2) == 1:
                phrase = random.randrange(0, 4)
                if phrase == 0:
                    print(hand.get_name() + " says: \"I'm so close to winning!\"")
                elif phrase == 1:
                    print(hand.get_name() + " says: \"Almost there...\"")
                else:
                    print(hand.get_name() + " is visibly excited.")
        pause()
        match_found = False
        # Find the first card in the Comp's hand that's valid to play
        for i in range(hand.get_len()):
            # 8 Card
            if hand.get_card(i).get_rank() == 8:
                match_found = True
                new_suit = random.randrange(0, 4)
                hand.pop_card(i) # Remove card from hand
                card = Card(int(new_suit), 8) # Change suit of card
                self.stock.add_card(card) # Add card to pile
                break
            # Valid card
            elif self.stock.top_card().valid_play(hand.get_card(i)):
                match_found = True
                card = hand.pop_card(i) # Remove card from hand
                self.stock.add_card(card) # Add card to pile
                break
        # If no valid one is found, draw from deck
        if match_found == False:
            if hand.get_len() < 4:
                # With an extra chance to say something about it
                if random.randrange(0,3) == 1:
                    phrase = random.randrange(0, 2)
                    if phrase == 0:
                        print(hand.get_name() + " says: \"Aww man...\"")
                    if phrase == 1:
                        print(hand.get_name() + " says: \"Shoot!\"")
            print("Drawing from deck until a playable card is found...")
            # If the self.deck.draw_until() function returns False, refill the deck
            while not self.deck.draw_until(self.stock.top_card(), hand):
                self.deck.refill(self.stock)
            card = hand.pop_card(-1) # Remove card from hand
            self.stock.add_card(card) # Add card to pile
        print(hand.get_name() + " put down the " + str(card))
        pause()

# Function that prints out the instructions
def instructions():
    print("\nHow to Play Crazy Eights:\nEach player is dealt 5 cards. The player that reaches 0 cards first wins.\nThere are two stacks of cards: \n\t1. The Deck that cards are dealt from and players draw from\n\t2. \"Card in Play\" Deck; cards placed down from players, including the initial card ")
    print("When it is a player's turn, they can choose to play a card from their deck if it matches the following criteria:\n\t1. Matches the rank (number) of the Card in Play\n\t2. Matches the suit of the Card in Play\n\t3. Any card that is rank 8, which allows the player to change the suit\nIf none of the criteria matches the player's cards to the card in play, the player must draw from the deck until a match is found.")
    input("\nHit enter to play!")

# Welcome message and instructions for player
print("Welcome to Crazy Eights!")
print("0: Instructions\n1: Start Game")
x = int(input("Please make a selection: "))
while x > 1 or x < 0:
    x = int(input("Incorrect input, please make a correct selection: "))
if x == 0:
    instructions()

# Player picks amount of computers to play with
while True:
    x = int(input("Please input the number of computers to play against (1-3): "))
    if x > 0 and x <= 3:
        break
    else:
        print("Invalid input")
num_players = x

# Game initializes
game = CrazyEights()
playerHand = Hand("You")
comHands = []
for i in range(num_players):
    comHands.append(Hand("Computer " + str(i+1)))

# Game deals cards to players
game.deal(comHands + [playerHand])

# Game starts
game.start([playerHand] + comHands)



