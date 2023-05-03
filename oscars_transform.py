import cip_library as cip

#read data from table "boxofficemojo_raw" and store the data in a dataframe
df_oscars_transform = cip.get_data_from_mariadb(table_name = "oscars_raw")

print(len(df_oscars_transform))
print(df_oscars_transform)