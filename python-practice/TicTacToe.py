import random
import time

class TicTacToe:

    def __init__(self):

        self.game_layout ='''
                               *     *     
                            1  *  2  *  3  
                          * * * * * * * * *
                               *     *      
                            4  *  5  *  6   
                          * * * * * * * * *
                               *     *
                            7  *  8  *  9    
                                            '''
        
        print(self.game_layout)

        self.num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]


    def update_game_layout(self, game_layout_live, num, letter):
        self.num_list.remove(int(num))
        return game_layout_live.replace(num, letter)

    def print_question(self, player, letter):
        play = str(input("{}, Choose a value to replace with '{}': ".format(player, letter)))
        return play


    # function to be utilized when player_1 and player_1 make a move
    def have_turn(self, game_layout_live, player_str, letter):
        player = ""

        while True:
            player = self.print_question(player_str, letter)

            if player not in game_layout_live:
                print("not valid")
            else:
                game_layout_live = self.update_game_layout(game_layout_live, player, letter)
                break

        return game_layout_live

    # have computer play random number from remaining
    # list and update tictactoe table
    def computer_turn(self, game_layout_live, letter, num_list):
        play = ""

        while True:
            play = str(random.choice(num_list))
            print("Computer plays 'O' at {}".format(play))
            time.sleep(1)

            if play not in game_layout_live:
                print("not valid")
            else:
                game_layout_live = self.update_game_layout(game_layout_live, play, letter)
                break

        return game_layout_live

    # this is the main function in which the player_1 and player_2
    # play against each other
    def play_player2(self):
        game_layout_live = self.game_layout
        num_list = self.num_list

        while len(num_list) > 1:

            game_layout_live = self.have_turn(game_layout_live, "Player 1", 'X')
            print(game_layout_live)

            game_layout_live = self.have_turn(game_layout_live, "Player 2", 'O')
            print(game_layout_live)

        game_layout_live = self.have_turn(game_layout_live, "Player 2", 'O')
        print(game_layout_live)
        
            
    # this is the main function in which the player and compuer
    # play against each other
    def play_computer(self):
        game_layout_live = self.game_layout
        num_list = self.num_list

        while len(num_list) > 1:

            game_layout_live = self.have_turn(game_layout_live, "Player 1", 'X')
            print(game_layout_live)

            game_layout_live = self.computer_turn(game_layout_live, 'O', num_list)
            
            print(game_layout_live)
        
        game_layout_live = self.computer_turn(game_layout_live, 'O', num_list)
        print(game_layout_live)

    


while True:

    # initialize TicTacToe class
    tic_tac_toe = TicTacToe()
    
    #   Choose your opponent? Computer(c) or player2(p) or exit(q)?
    play_response = input("Choose your opponent? Computer(c) or player2(p) or exit(q)? \n").lower()

    if play_response == "q":
        print("Exiting Game")
        break
    elif play_response == "c":
        print("opponent chosen: computer")
        tic_tac_toe.play_computer()
        break
    elif play_response == "p":
        print("opponent chosen: player")
        tic_tac_toe.play_player2()
        break
    else:
        print("ERROR: Input Incorrect")
