import cip_library as cip

#read data from table "oscars_raw" and store the data in a dataframe
df_oscars_transform = cip.get_data_from_mariadb(table_name = "oscars_raw")

# Get Cursor
cur = cip.mariadb_connect().cursor()

cur.execute("SELECT * FROM oscars_raw WHERE name=?", ("KING RICHARD",))

# Print Result-set
for (name) in cur:
    print(f"Name: {name}")
print(30 * "*")


cur.execute("SELECT * FROM oscars_raw WHERE movie=?", ("KING RICHARD",))

# Print Result-set
for (name) in cur:
    print(f"Movie: {name}")
print(30 * "*")


cur.execute("SELECT * FROM oscars_raw WHERE name=?", ("CRUELLA",))

# Print Result-set
for (name) in cur:
    print(f"Name: {name}")
print(30 * "*")


cur.execute("SELECT * FROM oscars_raw WHERE movie=?", ("CRUELLA",))

# Print Result-set
for (name) in cur:
    print(f"Movie: {name}")
print(30 * "*")