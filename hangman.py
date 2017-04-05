import time

class Game:
    def __init__(self):
        #name = input("What is your name?")
        #print("Hello, " + name, "Time to play hangman!")
        #print("")

        time.sleep(1)
        print("Start guessing...")      # ...
        time.sleep(0.5)

        word = "secret"     # as an example..
        guesses = ''        # player input
        turns = 10      # ?

        while turns > 0:
            failed = 0

            for char in word:
                if char in guesses:
                    print(char)
                else:
                    print("_")
                    failed += 1

            if failed == 0:
                print("You won!")
                break

            print("")

            guess = input("Guess a character: ")
            guesses += guess

            if guess not in word:
                turns -= 1
                print("Wrong guess.")
                print("You have " + str(turns), "more guesses.")

                if turns == 0:
                    print("You lose!")

        #play = input("Would you like to play again? (y/n): ")
        #while play == 'y':
        #    Game()

#Game()
play = 'y'
while play == 'y':
    Game()
    play = input("Would you like to play again? (y/n): ")
