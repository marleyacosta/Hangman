import time
import sqlite3


class Game:
    def __init__(self):

        print("\nWelcome to Movies Hangman.\nWhere you guess the title of a movie.\n" +
        "Created by Maurely Acosta & Nicolette Celli.\n")

        cursor = movie_metadata_connection.cursor()

        # This generated a random row from the movie_metadata database
        cursor.execute(
            "SELECT * " +
             "FROM movie_metadata " +
             "ORDER BY RANDOM() " +
             "LIMIT 1")

        results = cursor.fetchall()

        row = results[0]

        # Get the data from the row.
        director_name = row[1]
        actor_1_name = row[3]
        actor_2_name = row[2]
        actor_3_name = row[5]
        title_year = row[6]
        movie_title = row[4]

        # Calculate the number of turns depending on how distinct letters in the movie title
        num_distinct_letters = len(''.join(set(movie_title)))
        turns = num_distinct_letters + round(num_distinct_letters * .25)
        print(movie_title)
        time.sleep(1)

        #Hint
        print("Hints:\n")
        print("The movie was released on " + title_year +" and directed by " + director_name + ".\n" +
                "Starring " + actor_1_name + ", " + actor_2_name + ", and " + actor_3_name + ".")

        print("\n\n You will have " + str(turns) +" turns. Start Guessing. Good Luck!")
        time.sleep(0.5)

        guesses = ''

        while turns > 0:
            failed = 0

            for char in movie_title.lower():
                if char in guesses.lower():
                    print(char)
                else:
                    print("-")
                    failed += 1

            if failed == 0:
                print("You won!")
                break

            print("")

            guess = input("Guess a character possibly found in the movie title: ")
            guesses += guess

            if guess not in movie_title:
                turns -= 1
                print("Wrong guess.")
                print("You have " + str(turns), "more guesses.")

                if turns == 0:
                    print("You lose! " + " the movie was: " + movie_title)

play = 'y'
while play == 'y':

    global movie_metadata_connection
    movie_metadata_connection = sqlite3.connect('movie_metadata.sqlite')

    Game()

    play = input("Would you like to play again? (y/n): ")

    if play == "n":
        movie_metadata_connection.close()
