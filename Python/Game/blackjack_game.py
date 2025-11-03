import random

CARD_NUMBER = 0
SUIT = 1

def main():
    # Your main logic here
    print("Welcome to the Blackjack Game!")
    # Initialize game variables, deck, players, etc.
    card_numbers = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    deck = []
    player_hand_value = 0

    for card_number in card_numbers:
        for suit in suits:
            deck.append(
                #     0             1
                (str(card_number), suit)
            )

    player_hand = []
    dealer_hand = []


    for i in range(2):
        random_card = deck[random.randint(0, len(deck)-1)]
        deck.remove(random_card)
        player_hand.append(random_card)

        random_card = deck[random.randint(0, len(deck)-1)]
        deck.remove(random_card)
        dealer_hand.append(random_card)

    
    player_hand_value = int(calculate_card_value(player_hand[0][CARD_NUMBER])) + int(calculate_card_value(player_hand[1][CARD_NUMBER]))
    dealer_hand_value = int(calculate_card_value(dealer_hand[0][CARD_NUMBER]))

    print("This is your hand :")
    print("\t" + str(player_hand[0]))
    print("\t" + str(player_hand[1]))
    print("Your hand value: " + str(player_hand_value))
    
    print("\n\nDealer's hand:")
    print("\t" + str(dealer_hand[0]))
    print("Dealer hand value: " + str(dealer_hand_value))

    choice = ""
    while True:
        print("\n\nHit or Stand?")
        choice = input().strip().lower()
        if choice == "hit":
            # Logic for drawing another card
            print("You chose to hit!")
            random_card = deck[random.randint(0, len(deck)-1)]
            deck.remove(random_card)
            player_hand.append(random_card)
            player_hand_value += calculate_card_value(random_card[CARD_NUMBER])
            print("Your hand is now : " + str(player_hand))
            print("Your hand in now worth : " + str(player_hand_value))
            if player_hand_value == 21:
                print("BLACKJACK!")
                print("You Won!")
                exit()
            elif player_hand_value < 21:
                dealer_hand_value += int(calculate_card_value(dealer_hand[1][CARD_NUMBER]))
                
                print("Dealer reveals the second card : " + str(dealer_hand))
                print("Dealer hand value: " + str(dealer_hand_value))

                if(dealer_hand_value < player_hand_value):
                    print("you won!")
                else:
                    print("you lost")
                exit()
                break
            elif player_hand_value > 21:
                print("you bust! you lose! you suck!")
                exit()

        elif choice == "stand":
            # Logic for ending the player's turn
            print("You chose to stand!")
            dealer_hand_value += int(calculate_card_value(dealer_hand[1][CARD_NUMBER]))
            print("Dealer reveals the second card : " + str(dealer_hand[1]))
            if(dealer_hand_value < player_hand_value):
                print("you won!")
            else:
                print("you lost")
            exit()
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")
    



   



def calculate_card_value (card):
    if card == "Ace":
        return 1
    if card == "Jack" or card == "Queen" or card == "King":
        return 10
    else:
        return int(card)
    
    



if __name__ == "__main__":
    main()