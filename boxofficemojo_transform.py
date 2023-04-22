import cip_library as cip

#read data from table "boxofficemojo_raw" and store the data in a dataframe
pd_boxofficemojo_transform = cip.get_data_from_mariadb(table_name = "boxofficemojo_raw")

#now we transform the column "rank" and "gross" into "integer"
cip.to_int(pd_boxofficemojo_transform, "rank")
cip.to_int(pd_boxofficemojo_transform, "gross")

#clean film_title column
cip.clean_film_title(pd_boxofficemojo_transform, "film_title")

#define columns and datatypes needed in new table
cols = ["id", "rank", "film_title", "gross", "film_title_cleaned"]
dtypes = ["INT", "INT", "VARCHAR(255)", "INT", "VARCHAR(255)"]
cip.create_table("boxofficemojo_transformed", cols, dtypes)

#write transformed dataframe into table "boxofficemojo_transformed"
cip.write_to_table(df=pd_boxofficemojo_transform, table_name="boxofficemojo_transformed")

