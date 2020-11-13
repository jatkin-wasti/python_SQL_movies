import pyodbc  # Importing pyodbc to connect with and manipulate our database
import pandas as pd  # Importing pandas to handle the csv file
import csv  # Importing csv to handle the csv file in a better way


# Creating our class which will store all of the functionality
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
        cursor = self.connect()
        cursor.execute("CREATE TABLE Jamie_IMDB_Movies (titleType VARCHAR(255), primaryTitle VARCHAR(255), "
                       "originalTitle "
                       "VARCHAR(255), isAdult INT, startYear INT, endYear INT, runtimeMinutes INT,  genres VARCHAR("
                       "255));")

    # This method takes and formats the csv data in a way that allows us to insert each row into our database
    def csv_to_database(self):
        # Calling our connection method to execute SQL statements later on
        cursor = self.connect()
        # Creating a list that we'll dump our csv data into
        self.movies_list = []
        with open("imdbtitles.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.movies_list.append(row)
        # Formatting the header as odd characters appear at the start of them
        self.movies_list[0][0] = self.movies_list[0][0][3:]
        # For every non header row we'll create a string containing the values to be input to the table
        for rows in self.movies_list[1:]:
            values = ", ".join(str(word) for word in rows)
            # Splitting the string up to handle the genre field which may have multiple values separated by commas
            attributes_list = values.split(", ")
            # If there are multiple attributes we'll concatenate them
            if len(attributes_list) > 8:
                for _ in range(8, len(attributes_list) - 1):
                    attributes_list[7] += attributes_list[_]
            # Constructing our SQL statement
            sql_query = f"INSERT INTO Jamie_IMDB_Movies VALUES ("
            for _ in range(3):
                sql_query = sql_query + "'" + attributes_list[_] + "', "
            for _ in range(3, 7):
                if str(attributes_list[_]).isdigit():
                    sql_query = sql_query + attributes_list[_] + ", "
                else: sql_query = sql_query + "0" + ", "
            sql_query = sql_query + "'" + attributes_list[7] + "'"
            sql_query = sql_query + ");"
            # It will try to insert each row into the table using our SQL statement
            try:
                print(sql_query)
                cursor.execute(sql_query)
                print("This insert was successful")
            # If this fails we'll output a message to the user
            except:
                print("This insert was unsuccessful")
        return "Movies have been added to the database!"


    # Method to insert a movie to the database based on input from the user
    def insert_movies(self):
        print("To add your movie to the database we'll just have to collect some information from you.")
        media_type = input("Please input the type of media (i.e. 'movie', 'video', or 'videoGame' etc.):  ")
        current_title = input("Please input the current title of your movie:  ")
        original_title = input("Please input the original or working title of your movie:  ")
        suitable_for_children = int(input("If your movie is intended for all ages please enter 0. If it is not "
                                          "suitable for children please enter 1:  "))
        start_year = int(input("Please input the year that you started filming:  "))
        end_year = int(input("Please input the year that the movie was released:  "))
        run_time = int(input("Please input the run time of your movie in minutes:  "))
        genres = input("Please input all the genres that your movie falls under with each genre separated by a "
                       "comma:  ")
        cursor = self.connect()
        cursor.execute(f"INSERT INTO Jamie_IMDB_Movies "
                       f"VALUES ('{media_type}', '{current_title}', '{current_title}', '{original_title}', "
                       f"{suitable_for_children}, {start_year}, {end_year}, {run_time}, '{genres}');")

    # Function that takes text data and inputs it into our database
    def text_to_database(self, filename):
        cursor = self.connect()
        text_file = open(filename, 'r')  # Opens the file
        for line in text_file:
            # Inserts what's stored on each line into primaryTitle attribute of the table
            cursor.execute(f"INSERT INTO Jamie_IMDB_Movies (primaryTitle) VALUES ('{line}')")

    # Function that retrieves everything in our database and converts it into a text file
    def database_to_text(self):
        cursor = self.connect()
        # Retrieving all of the data stored in our table
        all_data = cursor.execute("SELECT * FROM Jamie_IMDB_Movies;")
        # Writing to a file or creating one if it doesn't already exist
        writer = open('downloaded_movies.text', 'w')
        # Inputting the name of the film in each record into the text file
        for rows in all_data:
            writer.write(str(rows.primaryTitle))

    # Method that connects to the DB and returns the result of the query statement searching for the given movie
    def sql_show_movie(self, table_name, movie_title):
            cursor = self.connect()
            movie_info = cursor.execute(f"SELECT * FROM {table_name} WHERE primaryTitle = '{movie_title}';")
            return movie_info

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
# test.python_show_movie("imdbtitles.csv", "Bigfoot")
# test.sql_show_movie("Jamie_IMDB_Movies", "Bigfoot")
# Testing if the table is created
# test.create_movie_db()
# Inserting movies into the db
# test.insert_movies()
# test.database_to_text()
# test.text_to_database("film_names.text")
# test.database_to_text()
print(test.csv_to_database())
