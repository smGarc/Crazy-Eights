# Crazy-Eights
Simple Text-Based Crazy 8's (Uno) Game in Python based on Object Oriented Programming

Play Crazy 8's with up to 3 computers

## How to Run Python Script

1. Have Python installed on your computer
2. Open the command prompt and navigate to the folder that contains the python script Crazy8s.py
3. Execute one of the following commands: ``python Crazy8s.py``, ``python3 Crazy8s.py``, or ``py Crazy8s.py`` (Depends on what works for your system)
4. Program will start
5. Have fun :-)

## How to Play Crazy Eights:

Each player is dealt 5 cards. The player that reaches 0 cards first wins.

There are two stacks of cards:
1. The Deck that cards are dealt from and players draw from
2. "Card in Play" Deck; cards placed down from players, including the initial card (Named the "stock" deck in the code)

When it is a player's turn, they can choose to play a card from their deck 
if it matches the following criteria:
1. Matches the rank (number) of the Card in Play
2. Matches the suit of the Card in Play
3. Any card that is rank 8, which allows the player to change the suit

If none of the criteria matches the player's cards to the card in play, 
the player must draw from the deck until a match is found.
