import pyodbc  # Importing pyodbc to connect with and manipulate our database
import pandas as pd  # Importing pandas to handle the csv file


class Movies:
    # Method to connect to our database
    def connect(self):
        # We will connect to our Northwind DB which we've already used in the SQL week
        server = "databases1.spartaglobal.academy"
        database = "Northwind"
        username = "SA"
        password = "Passw0rd2018"
        # Server name, database name, username, and password are required to connect to pyodbc
        northwind_connection = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};SERVER='
                                               + server + ';DATABASE=' + database + ';UID='
                                               + username + ';PWD=' + password))
        # Creating and returning a cursor to be used in the other methods
        cursor = northwind_connection.cursor()
        return cursor

    # Method to read a file using pandas and returning the dataframe created
    def read_file(self, filename):
        csv_file = pd.read_csv(filename)
        return csv_file

    # Method to create the table in the database from the csv file information
    def create_movie_db(self):
        pass

    # Method to show a movies information when provided the movie title
    def python_show_movie(self, filename, movie_title):
        all_movies = self.read_file(filename)
        # Iterates through each each tuple in the dataframe
        for movie in all_movies.itertuples():
            # Checking for the movie requested
            if movie.primaryTitle == movie_title:
                # Converting the 0/1 value to a string so that we can output a meaningful message to the user
                if movie.isAdult == 0:
                    rating = "suitable for children"
                else:
                    rating = "not suitable for children"
                # Printing all of the information stored on that movie in a nice format
                print(f"{movie.titleType}: {movie.primaryTitle} was originally called {movie.originalTitle}.\n"
                      f"It is {rating}.\n"
                      f"It started filming in {movie.startYear} and finished filming in {movie.endYear}.\n"
                      f"It is {movie.runtimeMinutes} minutes long and has the following genres: {movie.genres}")
                break


# Creating an instance of the Movies class
test = Movies()
# Testing that it reads the file without throwing an error
# test.read_file("imdbtitles.csv")
# Testing if the show_movie function will provide us with the relevant details to the movie requested
test.python_show_movie("imdbtitles.csv", "Bigfoot")


# ,
#                                names = ['titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear',
#                                           'endYear', 'runtimeMinutes', 'genres']
