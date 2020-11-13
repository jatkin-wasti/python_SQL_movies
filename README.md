# SQL Movies CRUD Task
Timings

60 Minutes
Summary

Now that you've learned how to connect to the DB using pyodbc you can start abstracting out interaction the db! This is great if you don't like writing sql.
Tasks

    CRUD the DB

Hint: create abstraction and methods to deal with db so you don't have too
Acceptance Criteria

    You can get all the movies
    you can search based on title

    you can add movies to DB

    second iteration:

IMDB CSV <> Py <> SQL
Summary

You know how to parse txt files into python.
You also know how to connect python into the db.
You also know how to manipulated and change data with python.

Your task is to move data from text files into the db and from the the db into text files
Tasks

    read the text file and create object

    save object in DB

    Load that from DB and create object
    output object to text file

Extra:
* Explore other APIs
Acceptance Criteria

    able to take in 10 film names in text file and save to db
    able to load data from DB and create text file with names
# Solution
## Downloading the CSV file
- To do this task, we need to be able to access the csv file containing the information on the numerous movies
- Feel free to copy and paste the contents of my ```imdbtitle.csv``` into a newly created csv file within your Pycharm
 project
## Iteration 1
### This first attempt I've used pure python methods to try and meet the acceptance criteria
- First we'll create our py file and import pyodbc and pandas, which will let us connect to the database and handle
 the csv file
```
import pyodbc  # Importing pyodbc to connect with and manipulate our database
import pandas as pd  # Importing pandas to handle the csv file
import csv  # Importing csv to handle the csv file in a better way
```
- Creating our class
```
# Creating our class which will store all of the functionality
class Movies:
```
- Creating a method that establishes a connection to the database and returns a cursor that we'll use to execute our
 SQL statements later on
```
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
```
- Creating a method that that takes a csv file and converts it to a dataframe object which it then returns
```
    # Method to read a file using pandas and returning the dataframe created
    def read_file(self, filename):
        csv_file = pd.read_csv(filename)
        return csv_file
```
- Creating a method to read and get all of the movie data from the CSV
```
    # Method to read a file using pandas and returning the dataframe created
    def read_file(self, filename):
        csv_file = pd.read_csv(filename)
        return csv_file
```
- Creating a method to loop through the file we've read, finding the required movie and returning the information on
 that movie
```
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

```
## Iteration 2
### This increment uses actual SQL statements to meet the acceptance criteria
- Creating a method to create a table with the appropriate column names and data types
```
# Method to create the table in the database from the csv file information
    def create_movie_db(self):
        cursor = self.connect()
        cursor.execute("CREATE TABLE Jamie_IMDB_Movies (titleType VARCHAR(255), primaryTitle VARCHAR(255), "
                       "originalTitle "
                       "VARCHAR(255), isAdult INT, startYear INT, endYear INT, runtimeMinutes INT,  genres VARCHAR("
                       "50));")
```
- We'll create a method that will read in data from our csv file and then insert that data into our created database
- We'll use our imported csv module to read from the file and we'll change values that would cause errors (i.e. if a
 value in the file is '\N' to signify that it is empty we need to change this value to a number if that column should
  be an int). We'll change these values to 0.
- We'll also handle multiple genres by concatenating them and then we'll put all of these normalised values into our
 sql statement and run it
- Things might still go wrong though, so we should think ahead and put the insert statement in a try block and use
 except to print a message to our users if something went wrong 
```
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
```

- Getting data on the requested movie with a cursor executing an SQL statement on the database instead of searching
 through the file data itself
```
    # Method that connects to the DB and returns the result of the query statement searching for the given movie
    def sql_show_movie(self, table_name, movie_title):
            cursor = self.connect()
            movie_info = cursor.execute(f"SELECT * FROM {table_name} WHERE primaryTitle = '{movie_title}';")
            return movie_info
```
- Creating our method to add movies into our table based on user input
- This is done through a cursor executing an SQL statement formatted in an fstring with the user inputs
```
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

```
- Creating a method that takes a plain text file with film names on their own lines and inserts those films into the
 database
```
    # Function that takes text data and inputs it into our database
    def text_to_database(self, filename):
        cursor = self.connect()
        text_file = open(filename, 'r')  # Opens the file
        for line in text_file:
            # Inserts what's stored on each line into primaryTitle attribute of the table
            cursor.execute(f"INSERT INTO Jamie_IMDB_Movies (primaryTitle) VALUES ('{line}')")
```
- Creating a method that gets all of the data out of the table and puts each record in a new line in a newly created
 text file
```
    # Function that retrieves everything in our database and converts it into a text file
    def database_to_text(self):
        cursor = self.connect()
        # Retrieving all of the data stored in our table
        all_data = cursor.execute("SELECT * FROM Jamie_IMDB_Movies;")
        # Writing to a file or creating one if it doesn't already exist
        writer = open('downloaded_movies.text', 'w')
        # Inputting the name of the film in each record into the text file
        for rows in all_data:
            writer.write(str(rows.primaryTitle) + '\n')
```

