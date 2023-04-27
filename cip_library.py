import mariadb
import sys
import pandas as pd
import sqlalchemy as sa
import nltk
from nltk.tokenize import word_tokenize
def mariadb_connect(usr="cip_user",pw="cip_pw", db="CIP"):
    """
    Function is used to connect to mariadb. It takes 3 optional arguments 'usr', 'pw', and 'db'.
    :param usr: defines the user used in the connection (default is 'cip_user'
    :param pw: defines the password used in the connection (default is 'cip_pw'
    :param db: defines the database used in the connection (default is 'CIP'
    :return: Returns mariadb connector object.
    """
    try:
        conn = mariadb.connect(
            user=usr,
            password=pw,
            host="127.0.0.1",
            port=3306,
            database=db
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def create_table(table_name, columns, datatypes):
    """
    Function is used to create tables on mariadb. it takes 3 arguments 'table_name', 'columns' and 'datatypes'.
    :param table_name: defines the name of the table to be created
    :param columns: list containing all the columns needed in the table
    :param datatypes: list of datatypes for each column
    """
    cur = mariadb_connect().cursor()
    create_table = "CREATE OR REPLACE TABLE" + " " + table_name + " ("
    # zip columns and datatypes
    zipped = list(zip(columns, datatypes))

    for i in range(len(zipped)):
        create_table += zipped[i][0] + " " + zipped[i][1] + ", "
    #remove last two characters from string (, and space) and add a closing ")".
    create_table = create_table[:-2] + ")"
    cur.execute(create_table)

def write_to_table(df, table_name, usr="cip_user",pw="cip_pw", db="CIP"):
    """
    Function is used to write dataframes into tables in mariadb. To do so it creates a sqlalchemy engine. It takes 5 arguments 'df', 'table_name', 'usr', 'pw', and 'db'.
    :param df: Specifies the dataframe that should be written into a table.
    :param table_name: Specifies the name of the table the data should be written into.
    :param usr: defines the user used in the connection (default is 'cip_user')
    :param pw: defines the password used in the connection (default is 'cip_pw')
    :param db: defines the database used in the connection (default is 'CIP')
    """
    #first we create the sqlalchemy engine.
    engine_str = f'mysql+pymysql://{usr}:{pw}@localhost:3306/{db}'
    engine = sa.create_engine(engine_str)
    df.to_sql(con=engine, name=table_name, if_exists='replace')

def get_data_from_mariadb(table_name, columns = "*"):
    """
    Function is used to read data from a table in mariadb into a dataframe. It takes two arguments 'table_name' and 'columns'.
    :param table_name: Name of the table we want to read data from
    :param columns: Optional. Defines the columns that should be selected. If nothing is defined then all columns are selected.
    :return: returns a dataframe containing the data from the specified table
    """
    #create connection to mariadb
    cur = mariadb_connect().cursor()
    #create string for cols to select
    cols = ""
    #if columns is not equal to "*" then read all entries from the list provided and then add them to the cols string. Otherwise cols string is "*"
    if columns != "*":
        for col in columns:
            cols += col + ", "
        cols = cols[:-2]
    else:
        cols = "*"
    #create string for query
    query = "SELECT " + cols + " FROM " + table_name
    #execute query and fetch results into "results"
    cur.execute(query)
    results = cur.fetchall()
    #get the column headers of the table
    headers = pd.DataFrame(cur.description)
    #create dataframe containing the results
    df = pd.DataFrame(results)
    #use the fetched table headers as column headers in dataframe
    df.columns = headers[0]
    return df

def to_int(df, column):
    """
    Function is used to transform a column in a dataframe to integer type. It takes two arguments 'df' and 'column'
    :param df: dataframe in which a column needs to be changed
    :param column: column which needs to be changed
    :return: Returns a dataframe in which the specified column was transformed to integer type
    """
    #first we need to replace all non-numeric characters in the specified column. To do so we are using regex with the replace() function
    df[column] = df[column].replace('[^0-9]', '', regex = True)
    #then we define the specified column as type integer
    df[column] = df[column].astype(int)
    return df

def clean_film_title(df, column):
    """
    Function is used to clean the "film title" column to make sure that we have the same format from all the sources.
    Specifically we want to remove all special characters such as ":" and "," and then we want to cast the title to lower case.
    It takes two arguments 'df' and 'column'
    :param df: dataframe in which a column needs to be changed
    :param column: film title column.
    :return: Returns a dataframe in which the film title column was cleaned and added as a new column
    """
    # first we need to replace all "special" characters in the specified column. To do so we are using regex with the replace() function
    df["film_title_cleaned"] = df[column].replace('[^a-zA-Z0-9]', '', regex=True)
    #now we cast the title to lower case
    df["film_title_cleaned"] = df["film_title_cleaned"].str.lower()
    return df

def extract_id(list_in, list_out):
    """
    Function is used to extract the movie id from IMDb href link
    :param list_in: list containing all href values
    :param list_out: list to be returned containing only id's
    :return: Returns list of id's
    """
    #go through each element in list_in and split the entries by "/". if a word starts with "tt" it is an id and we want to append it to list_out.
    for i in list_in:
        string = i
        split = string.split("/")
        for word in split:
            if word[0:2] == "tt":
                list_out.append(word)
    return list_out

def tokenize_and_clean(text):
    """
    This function is used to tokenize text and to remove any special characters, symbols, punctuations, numbers and stopwords. This is important when preparing text for sentiment analysis. It takes one argument 'text'.
    :param text: text value that needs to be tokenized
    :return: returns the tokenized text
    """
    #tokenize text
    tokens = word_tokenize(text)
    # Remove punctuation, symbols, special characters, and numbers from the tokens
    tokens = [token.lower() for token in tokens if token.isalpha()]
    #define stopwords and remove them
    stopwords = nltk.corpus.stopwords.words("english")
    tokens = [token.lower() for token in tokens if token.lower() not in stopwords]
    #return tokens
    return tokens

