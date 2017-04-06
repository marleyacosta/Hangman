import sqlite3

movie_metadata_connection = sqlite3.connect('movie_metadata.sqlite')
cursor = movie_metadata_connection.cursor()

# This generated a random row from the movie_metadata database
cursor.execute(
    "SELECT * " +
     "FROM movie_metadata " +
     "ORDER BY RANDOM() " +
     "LIMIT 1")

results = cursor.fetchall()

print ("Get the movie metadata:\n")

# get the row the sql query generated.
row = results[0]

# Get the data from the row.
director_name = row[1]
actor_1_name = row[3]
actor_2_name = row[2]
actor_3_name = row[5]
title_year = row[6]
movie_title = row[4]

print (director_name)
print(actor_1_name)
print(actor_2_name)
print(actor_3_name)
print(title_year)
print(movie_title)


movie_metadata_connection.close()
