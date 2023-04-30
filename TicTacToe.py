

# print menu


while True:

    #   Choose your opponent? Computer(c) or player2(p) or exit(q)?
    play_response = input("Choose your opponent? Computer(c) or player2(p) or exit(q)? \n").lower()

    if play_response == "q":
        print("Exiting Game")
        break
    elif play_response == "c":
        print("opponent chosen: computer")
    elif play_response == "p":
        print("opponent chosen: player")
    else:
        print("ERROR: Input Incorrect")



# deny and reask if not match options
# else start game

# print game layout and clarify choosing number to place sign
# and ask player1 to choose

#recieve input, update value with on game board

#check if there are 3 in a row
# if yes, whichever player wins if no next player turn

#logic for computer if chosen as player

# repeat until winner