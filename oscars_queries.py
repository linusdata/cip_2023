import cip_library as cip

#read data from table "oscars_raw" and store the data in a dataframe
df_oscars_transform = cip.get_data_from_mariadb(table_name = "oscars_stage_3")

# Get Cursor
cur = cip.mariadb_connect().cursor()

cur.execute("SELECT * FROM oscars_stage_3 WHERE movie=?", ("kingrichard",))

# Print Result-set
for (name) in cur:
    print(f"Name: {name}")
print(30 * "*")


cur.execute("SELECT * FROM oscars_stage_3 WHERE movie=?", ("titanic",))

# Print Result-set
for (name) in cur:
    print(f"Name: {name}")
print(30 * "*")