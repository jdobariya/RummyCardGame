"""
Rummy Game

Game Rules:

The objective is to form one's 10 cards into sequences (runs) and sets (also known as trails or trios).

A run (or sequence) consists of three or more consecutive cards of the same suit, the order being A-2-3-4-5-6-7-8-9-10-J-Q-K.

A set (trail, trio) consists of three cards of the same rank in different suits: spade5-heart5-diamond5 is a valid.

Wild cards can be used to substitute for any desired card in a set or run. 
For example if the turned up card is a club8 then heart3-spade8-heart5 is a valid run, and spadeJ-diamondJ-diamond8 is a valid set since all 8's are wild.

A straight run is a run formed without the use of wild cards as substitutes for other cards. 
At least one straight run is required in one's hand in order for any combinations to become valid.

A player "goes rummy" and winds the round when their entire 10 card hand includes sets and runs.
However, a player can only go rummy if their hand contains at least one natural run (a run containing no wilds) as well as a second run, natural or not.
The remaining cards can be runs or sets, natural or not.

Deck contains

The suits are Spades, Hearts, Diamonds, and Clubs (in descending order in bridge).
The ranks are Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, and King.
Joker

Encoding:
Spades => 3, Hearts => 2, Diamonds => 1, Clubs => 0, None => 4
Ace => 1, Jack => 11, Queen => 12, King => 13, Joker => 14
The default values for suit is 0 and for rank is 2.
"""

import random
import copy

class Card:
    # Class variables for the possible suits and ranks
    suit_list = ["Club", "Diamond", "Hearts", "Spades", ""]
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Joker"]

    def __init__(self, suit=0, rank=2):
        # Constructor to initialize the Card object with default values if not provided
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # String representation of the Card object
        if self.rank == 14:
            # Special case for Joker, as it has rank 14
            return self.rank_list[self.rank]
        else:
            # Regular card representation with rank and suit
            return self.rank_list[self.rank] + " of " + self.suit_list[self.suit]


class Deck:
    def __init__(self):
        # Initialize a standard deck of cards with 4 suits and ranks from 1 to 13
        self.cards = [Card(suit, rank) for suit in range(4) for rank in range(1, 14)]
        self.cards.append(Card(4, 14)) # Add a Joker card to the deck
        self._shuffle_card() # Shuffle the deck of cards

    def _shuffle_card(self):
        random.shuffle(self.cards) # Shuffle the sequence of cards in place

    def pop_card(self):
        return self.cards.pop() # Remove and return the top card from the deck

    def is_empty(self):
        return len(self.cards) == 0 # Check if the deck is empty

    def __str__(self):
        # Create a string representation of the deck for easy printing
        s = ""
        for i in range(0, len(self.cards)):
            s = s + i * " " + str(self.cards[i]) + "\n"
        return s

class Player:
    def __init__(self, name):
        # Initialize a player with an empty hand and a given name
        self.hand = []
        self.name = name

    def add_card(self, new_card):
        self.hand.append(new_card) # Add a new card to the player's hand
    
    def remove_card(self, ind):
        # Remove and return a card from the player's hand based on the given index
        card = self.hand[ind]
        self.hand.pop(ind) 
        return card
    
    def swap_card(self, card1_ind, card2_ind):
        # Swap two cards in the player's hand based on their indices
        self.hand[card1_ind], self.hand[card2_ind] = self.hand[card2_ind], self.hand[card1_ind]
    
    def __str__(self):
        # Create a string representation of the player's hand for easy printing
        if len(self.hand) != 0:
            return "Hand of {0} contains [{1}]\n".format(self.name, str.join(", ", [str(card) for card in self.hand]))
        else:
            return "Hand of {0} is empty\n".format(self.name)

class RummyGame:
    def __init__(self, players):
        # Initialize the Rummy game with players, deck, discard pile, and wild card
        self.players = [Player(name) for name in players]
        self.deck = Deck()
        self.discard_card_pile = []
        self.discard_card_pile.append(self.deck.pop_card())
        self.wild_card = self.deck.pop_card()

    def deal_intial_card(self, n_cards=10):
        # Distribute initial cards to players
        for _ in range(n_cards):
            for player in self.players:
                player.add_card(self.deck.pop_card())

    def is_valid_set(self, hand, cards_ind, wild_card):
        # Check if the given list of cards forms a valid set
        if len(cards_ind) < 3:
            return [False]
        
        cards = [hand[ind-1] for ind in cards_ind]
        joker_counter = 0
        for i, card in enumerate(cards):
            if(card.rank == 14 or card.rank == wild_card.rank):
                joker_counter+=1
                cards.pop(i)
        return [len(set(card.rank for card in cards)) == 1, joker_counter == 0]
    
    def is_valid_run(self, hand, cards_ind, wild_card):
        # Check if the given list of cards forms a valid run
        if len(cards_ind) < 3:
            return [False]
        cards = [hand[ind-1] for ind in cards_ind]
        joker_counter = 0
        for i in range(len(cards)):
            if(cards[i-joker_counter].rank == 14 or cards[i-joker_counter].rank == wild_card.rank):
                cards.pop(i-joker_counter)
                joker_counter+=1
        cards.sort(key = lambda card: (card.suit, card.rank))
        wild_card_counter = joker_counter
        for i in range(1, len(cards)):
            if( (cards[i].suit != cards[i-1].suit) or (cards[i].rank == cards[i-1].rank)):
                return [False]
            elif (cards[i].rank == cards[i-1].rank+1):
                continue
            elif(cards[i].rank <= (wild_card_counter + cards[i-1].rank + 1)):
                wild_card_counter -= (cards[i].rank - cards[i-1].rank -1)
            else:
                return [False] 
        return [True, joker_counter == 0]
    
    def printHand(self, hand):
        # Print the player's hand
        if len(hand) != 0:
            return print("Hand contains [{0}]\n".format(str.join(", ", [str(card) for card in hand])))
        else:
            return ("Hand is empty\n")
    
    def checkForWin(self, hand, atleast_one_natrual):
        # Check if the player has won
        if(len(hand) == 0 and atleast_one_natrual):
            return True
        else:
            return False

    def play(self):
        print("Welcome to Rummy!\n")
        random.shuffle(self.players)
        self.deal_intial_card()

        def discardCardFromHand(self, player):
             # Discard a card from the player's hand
            discard_card_pile = self.discard_card_pile
            dicard_card_from_hand = int(input(f"{player.name}, Which card would you like to discard form your hand (Enter sequnce number): ")) - 1
            discard_card = player.remove_card(dicard_card_from_hand)
            print(f"{player.name} discards: {discard_card}")
            discard_card_pile.append(discard_card)

        print("Initial players card:\n")
        for player in self.players:
                print(player)
        while True:
            for player in self.players:
                print("*"* 20 + f" {player.name} turn "+ "*"* 20 + "\n")
                print(player)
                print(f"Top card of discard pile: {self.discard_card_pile[-1]}")
                print(f"Wild card: {self.wild_card}\n")
                draw_from_discard_pile = input(f"{player.name}, draw a card from the top of the discard pile (y/n): ")
                print("\n")
                if(draw_from_discard_pile == "y"):
                    drawn_card = self.discard_card_pile.pop()
                    print(f"{player.name} draws: {drawn_card} (from the top of the discard pile)\n")
                    discardCardFromHand(self, player)
                    player.add_card(drawn_card)
                else:
                    if self.deck.is_empty():
                        top_card_from_discard_pile = self.discard_card_pile.pop()
                        self.deck.cards = copy.deepcopy(self.discard_card_pile)
                        self.deck._shuffle_card()
                        self.discard_card_pile.clear()
                        self.discard_card_pile.append(top_card_from_discard_pile)

                    drawn_card = self.deck.pop_card()
                    print(f"{player.name} draws: {drawn_card} (from the top of the deck)\n")
                    keepOrDicard = input(f"{player.name}, keep this card (y/n): ")
                    if(keepOrDicard == "y"):
                        discardCardFromHand(self, player)
                        player.add_card(drawn_card)
                    else:
                        self.discard_card_pile.append(drawn_card)

                print(player)

                rearrange_flag = input(f"{player.name}, do you want to rearrange cards (y/n): ")
                while (rearrange_flag == "y"):
                    sort_by = int(input("Sort by:\n 1. rank\n 2. suits and rank\n 3. swap\n 0. exit\n"))
                    match (sort_by):
                        case 1:
                            player.hand.sort(key = lambda card: card.rank, reverse=True)
                            print(player)
                        case 2: 
                            player.hand.sort(key = lambda card: (card.suit, card.rank), reverse=True)
                            print(player)
                        case 3:
                            card1_ind, card2_ind = map(int, input("Enter card 1 & card 2 indexes (starts with 1) seperated by space: ").split(" "))
                            player.swap_card(card1_ind - 1, card2_ind - 1)
                            print(player)
                        case 0:
                            break
                        case _:
                            break
                    if(sort_by not in [1, 2, 3]):
                        break
                
                check_for_win = input(f"{player.name}, want to check for win? (y/n): ")
                if(check_for_win == "y"):
                    player_hand = copy.deepcopy(player.hand)
                    has_atleast_one_natural = False
                    win_flag = False
                    while len(player_hand)>0:
                        check_type = int(input("Check :\n 1. sets\n 2. runs\n 3. reset cards\n 0. exit\n"))
                        match (check_type):
                            case 1:
                                card_ind = list(map(int, input("Enter card sequnce seperated by space: ").split(" ")))
                                set_flag = self.is_valid_set(player_hand, card_ind, self.wild_card)
                                if(set_flag[0] == False):
                                    print("The given sequnce is not a set!")
                                elif (set_flag[0] == True):
                                    print("Hooray...the given sequnce is a set!")
                                    deleted_counter = 0
                                    card_ind.sort()
                                    for i in card_ind:
                                        player_hand.pop(i-1-deleted_counter)    
                                        deleted_counter+=1
                                    self.printHand(player_hand)
                                    if(set_flag[1] == True):
                                        has_atleast_one_natural = True
                                    win_flag = self.checkForWin(player_hand, has_atleast_one_natural)
                                    if(win_flag == True):
                                        print("You won!")
                                        break                           
                            case 2: 
                                card_ind = list(map(int, input("Enter card sequnce seperated by space: ").split(" ")))
                                run_flag = self.is_valid_run(player_hand, card_ind, self.wild_card)
                                if(run_flag[0] == False):
                                    print("The given sequnce is not a run!")
                                elif (run_flag[0] == True):
                                    print("Hooray...the given sequnce is a run!")
                                    deleted_counter = 0
                                    card_ind.sort()
                                    for i in card_ind:
                                        player_hand.pop(i-1-deleted_counter)
                                        deleted_counter+=1
                                    self.printHand(player_hand)
                                    if(set_flag[1] == True):
                                        has_atleast_one_natural = True
                                    win_flag = self.checkForWin(player_hand, has_atleast_one_natural)
                                    if(win_flag == True):
                                        print("You won!")
                                        break
                            case 3: 
                                player_hand = copy.deepcopy(player.hand)
                                self.printHand(player_hand)
                            case 0:
                                break
                            case _:
                                break
                        if(check_type not in [1, 2, 3] or win_flag):
                            break
                    
                    if(win_flag):
                        exit(0)

if __name__ == "__main__":
    n_player = input("Enter total number of players: ")
    if n_player.isdigit():
        n_player = int(n_player)
        if 1 < int(n_player) <= 4:
            pass
        else:
            print("Number of players must be at least 2 and maximum of 4.")
            exit(1)
    else:
        print("Please enter number of players correctly.")
        exit(1)

    player_name_list = []
    player_counter = 0
    while player_counter < n_player:
        name = input(f"Enter player {player_counter + 1} name: ")
        if name not in player_name_list:
            player_name_list.append(name)
            player_counter += 1
        else:
            print("Player name \"{0}\" already exist! please enter different name.".format(name))
    game = RummyGame(player_name_list)
    game.play()