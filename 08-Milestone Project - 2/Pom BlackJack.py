import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suits,ranks):
        self.suits = suits
        self.ranks = ranks
    
    def __str__(self):
        return f'{self.ranks} of {self.suits}'

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        cardlist=''
        for n in self.deck:
            cardlist+=str(n)+'\n'
        return cardlist
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        if card.ranks == 'Ace':
            self.aces +=1
        self.value+=values[card.ranks]
        return card
    
    def adjust_for_ace(self):
        while self.value>21 and self.aces>0:
            self.value-=10
            self.aces-=1
    def __str__(self):
        cardlist = ''
        for n in self.cards:
            cardlist+=str(n)+'\n'
        return cardlist

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total-=self.bet

def take_bet(player):
    while True:
        try:
            player.bet = int(input('Please enter your bet: '))
        except TypeError:
            print ('Please enter as a whole number!')
        else:
            if player.bet > player.total:
                print (f'Bet must not exceed {player.total}!')
            else:
                print (f'You have successfully bet {player.bet}!')
                break

def hit(deck,hand):
    dealtcard=str(hand.add_card(deck.deal()))
    hand.adjust_for_ace()
    print (str(dealtcard)+' was dealt from the deck')
    print ('Now these are cards in the hand: \n' +str(hand)+ 'with value of: ' + str(hand.value))

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True:
        choice=input ('Do you want to hit? (y/n): ')
        if choice == 'y':
            hit(deck,hand)
        elif choice == 'n':
            print ('You chose to stand.')
            playing=False
            break
        else:
            print ('Choose only "y" or "n"!')

def show_some(player,dealer):
    #The passed in argument is Hand class
    print ('The player has: \n' +str(player) +'with value of: '+str(player.value))
    print ('The dealer has: \n' +str(dealer.cards[0])+' and '+'????')
    
def show_all(player,dealer):
    print ('The player has: \n' +str(player) +'with value of: '+str(player.value))
    print ('The dealer has: \n' +str(dealer) +'with value of: '+str(dealer.value))

def player_busts(chip):
    print (f'The player is busted! You lose {chip.bet} chips!')
    chip.lose_bet()

def player_wins(chip):
    print (f'Congratulations! You win {chip.bet} chips!')
    chip.win_bet()

def dealer_busts(chip):
    print(f'Congtatulations! The dealer is busted, you win {chip.bet} chips!')
    chip.win_bet()
    
def dealer_wins(chip):
    print (f'The dealer wins! You lose {chip.bet} chips!')
    chip.lose_bet()
    
# What the f is this????
#def push():
#    pass

playerchip=Chips()
while True:
    # Print an opening statement
    print ('Welcome to Pom\'s version of BlackJack!')
    
    # Create & shuffle the deck, deal two cards to each player
    deck=Deck()
    print ('A deck has been created.')
    
    deck.shuffle()
    print ('The deck has been shuffled.')
    
    playerhand=Hand()
    dealerhand=Hand()
    print ('Now dealing two cards to player and dealer.')
    playerhand.add_card(deck.deal())
    playerhand.add_card(deck.deal())
    dealerhand.add_card(deck.deal())
    dealerhand.add_card(deck.deal())
        
    # Set up the Player's chips
    print (f'You have {playerchip.total} chips left.')
    # Prompt the Player for their bet

    take_bet(playerchip)
    print (f'You bet {playerchip.bet}')
    # Show cards (but keep one dealer card hidden)
    show_some(playerhand,dealerhand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,playerhand)

        # Show cards (but keep one dealer card hidden)
        show_all(playerhand,dealerhand)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if playerhand.value>21:
            player_busts(playerchip)
            break

    	# If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        print ('Dealer\'s turn:')
        while dealerhand.value < 17:
        	hit(deck,dealerhand)
    
        # Show all cards
        show_all(playerhand,dealerhand)
    
        # Run different winning scenarios
        if dealerhand.value > 21:
        	dealer_busts(playerchip)
        elif dealerhand.value == playerhand.value:
        	print ('It\'s a draw!')
        elif dealerhand.value > playerhand.value:
        	dealer_wins(playerchip)
        elif dealerhand.value < playerhand.value:
        	player_wins(playerchip)


        # Inform Player of their chips total 
    print (f'You have {playerchip.total} chips left.')
        # Ask to play again
    if playerchip.total==0:
        print('Game over! You are out of chips!')
        break
    play_again = input('Do you want to play again? (y/n)')
    while play_again != 'y' and play_again != 'n':
        play_again = input('Please enter y or n')
    if play_again == 'y':
    	print('\n'*100)
    	playing=True
    else:
        break
