import cip_library as cip
import pandas as pd

#read data from table "oscars_stage_1.csv" and store the data in a dataframe
df_oscars_transform = pd.read_csv('oscars_stage_1.csv')


df_oscars_transform_sort = df_oscars_transform.sort_values(by= ['status'], ascending=False)


df_oscars_transform_1 = df_oscars_transform_sort.drop_duplicates(subset=['category', 'name', 'movie', 'year'],
                                                                         keep = 'first')


# alle bis auf diese
#'ACTOR', 'ACTOR IN A LEADING ROLE', 'ACTOR IN A SUPPORTING ROLE',
#'ACTRESS', 'ACTRESS IN A LEADING ROLE', 'ACTRESS IN A SUPPORTING ROLE'


categories_to_swap = ['ANIMATED FEATURE FILM', 'ART DIRECTION', 'ART DIRECTION (BLACK-AND-WHITE)',
       'ART DIRECTION (COLOR)', 'ASSISTANT DIRECTOR',
       'BEST MOTION PICTURE', 'BEST PICTURE', 'CINEMATOGRAPHY',
       'CINEMATOGRAPHY (BLACK-AND-WHITE)', 'CINEMATOGRAPHY (COLOR)',
       'COSTUME DESIGN', 'COSTUME DESIGN (BLACK-AND-WHITE)',
       'COSTUME DESIGN (COLOR)', 'DANCE DIRECTION', 'DIRECTING',
       'DIRECTING (COMEDY PICTURE)', 'DIRECTING (DRAMATIC PICTURE)',
       'DOCUMENTARY (FEATURE)', 'DOCUMENTARY (SHORT SUBJECT)',
       'ENGINEERING EFFECTS', 'FILM EDITING', 'FOREIGN LANGUAGE FILM',
       'HONORARY AWARD', 'HONORARY FOREIGN LANGUAGE FILM AWARD',
       'INTERNATIONAL FEATURE FILM', 'IRVING G. THALBERG MEMORIAL AWARD',
       'JEAN HERSHOLT HUMANITARIAN AWARD', 'MAKEUP',
       'MAKEUP AND HAIRSTYLING', 'MUSIC (ADAPTATION SCORE)',
       'MUSIC (MUSIC SCORE OF A DRAMATIC OR COMEDY PICTURE)',
       'MUSIC (MUSIC SCORE OF A DRAMATIC PICTURE)',
       'MUSIC (MUSIC SCORE--SUBSTANTIALLY ORIGINAL)',
       'MUSIC (ORIGINAL DRAMATIC SCORE)', 'MUSIC (ORIGINAL MUSIC SCORE)',
       'MUSIC (ORIGINAL MUSICAL OR COMEDY SCORE)',
       'MUSIC (ORIGINAL SCORE)',
       'MUSIC (ORIGINAL SCORE--FOR A MOTION PICTURE [NOT A MUSICAL])',
       'MUSIC (ORIGINAL SONG SCORE AND ITS ADAPTATION -OR- ADAPTATION SCORE)',
       'MUSIC (ORIGINAL SONG SCORE AND ITS ADAPTATION OR ADAPTATION SCORE)',
       'MUSIC (ORIGINAL SONG SCORE OR ADAPTATION SCORE)',
       'MUSIC (ORIGINAL SONG SCORE)', 'MUSIC (ORIGINAL SONG)',
       'MUSIC (SCORE OF A MUSICAL PICTURE--ORIGINAL OR ADAPTATION)',
       'MUSIC (SCORING OF A MUSICAL PICTURE)',
       'MUSIC (SCORING OF MUSIC--ADAPTATION OR TREATMENT)',
       'MUSIC (SCORING)',
       'MUSIC (SCORING: ADAPTATION AND ORIGINAL SONG SCORE)',
       'MUSIC (SCORING: ORIGINAL SONG SCORE AND ADAPTATION -OR- SCORING: ADAPTATION)',
       'MUSIC (SONG)', 'MUSIC (SONG--ORIGINAL FOR THE PICTURE)',
       'OUTSTANDING MOTION PICTURE', 'OUTSTANDING PICTURE',
       'OUTSTANDING PRODUCTION', 'PRODUCTION DESIGN',
       'SHORT FILM (ANIMATED)', 'SHORT FILM (DRAMATIC LIVE ACTION)',
       'SHORT FILM (LIVE ACTION)', 'SHORT SUBJECT (ANIMATED)',
       'SHORT SUBJECT (CARTOON)', 'SHORT SUBJECT (COLOR)',
       'SHORT SUBJECT (COMEDY)', 'SHORT SUBJECT (LIVE ACTION)',
       'SHORT SUBJECT (NOVELTY)', 'SHORT SUBJECT (ONE-REEL)',
       'SHORT SUBJECT (TWO-REEL)', 'SOUND', 'SOUND EDITING',
       'SOUND EFFECTS', 'SOUND EFFECTS EDITING', 'SOUND MIXING',
       'SOUND RECORDING', 'SPECIAL ACHIEVEMENT AWARD',
       'SPECIAL ACHIEVEMENT AWARD (SOUND EDITING)',
       'SPECIAL ACHIEVEMENT AWARD (SOUND EFFECTS EDITING)',
       'SPECIAL ACHIEVEMENT AWARD (SOUND EFFECTS)',
       'SPECIAL ACHIEVEMENT AWARD (VISUAL EFFECTS)', 'SPECIAL AWARD',
       'SPECIAL EFFECTS', 'SPECIAL FOREIGN LANGUAGE FILM AWARD',
       'SPECIAL VISUAL EFFECTS', 'UNIQUE AND ARTISTIC PICTURE',
       'VISUAL EFFECTS', 'WRITING', 'WRITING (ADAPTATION)',
       'WRITING (ADAPTED SCREENPLAY)', 'WRITING (MOTION PICTURE STORY)',
       'WRITING (ORIGINAL MOTION PICTURE STORY)',
       'WRITING (ORIGINAL SCREENPLAY)', 'WRITING (ORIGINAL STORY)',
       'WRITING (SCREENPLAY ADAPTED FROM OTHER MATERIAL)',
       'WRITING (SCREENPLAY BASED ON MATERIAL FROM ANOTHER MEDIUM)',
       'WRITING (SCREENPLAY BASED ON MATERIAL PREVIOUSLY PRODUCED OR PUBLISHED)',
       'WRITING (SCREENPLAY WRITTEN DIRECTLY FOR THE SCREEN)',
       'WRITING (SCREENPLAY WRITTEN DIRECTLY FOR THE SCREEN--BASED ON FACTUAL MATERIAL OR ON STORY MATERIAL NOT PREVIOUSLY PUBLISHED OR PRODUCED)',
       'WRITING (SCREENPLAY)', 'WRITING (SCREENPLAY--ADAPTED)',
       'WRITING (SCREENPLAY--BASED ON MATERIAL FROM ANOTHER MEDIUM)',
       'WRITING (SCREENPLAY--ORIGINAL)', 'WRITING (STORY AND SCREENPLAY)',
       'WRITING (STORY AND SCREENPLAY--BASED ON FACTUAL MATERIAL OR MATERIAL NOT PREVIOUSLY PUBLISHED OR PRODUCED)',
       'WRITING (STORY AND SCREENPLAY--BASED ON MATERIAL NOT PREVIOUSLY PUBLISHED OR PRODUCED)',
       'WRITING (STORY AND SCREENPLAY--WRITTEN DIRECTLY FOR THE SCREEN)',
       'WRITING (TITLE WRITING)' ]

for cat in categories_to_swap:
    df_temp = df_oscars_transform_1['category'] == cat
    df_oscars_transform_1.loc[df_temp, ['name', 'movie']] = df_oscars_transform_1.loc[df_temp, ['movie', 'name']].values

#clean film titles
df_oscars_transform_2 = cip.clean_film_title(df_oscars_transform_1, "movie")
df_oscars_transform_2.head()

#crate couned data
df_count = pd.DataFrame(df_oscars_transform_1[['year','status','film_title_cleaned']].value_counts()).reset_index()

df_count_1 = df_count.rename(columns={0:'number', 'film_title_cleaned':'movie'})


#create dataframe with number of wins
df_win = df_count_1.loc[df_count['status'] == 'winner'].rename(columns={'number':'number_W'})


#create dataframe with number of nominees
df_nom = df_count_1.loc[df_count['status'] == 'nominee'].rename(columns={'number':'number_N'})

df_win_dropped = df_win.drop('status', axis=1)
df_nom_dropped = df_nom.drop('status', axis=1)

#crate joined data
df_oscars_final = pd.merge(df_win_dropped, df_nom_dropped, how = 'outer', on=['year', 'movie'])


#fill all NaN with zeros in place
df_oscars_final.fillna(0, inplace=True)

print(df_oscars_final)

df_oscars_final = df_oscars_final.rename(columns={'count_x':'number_W'})
df_oscars_final = df_oscars_final.rename(columns={'count_y':'number_N'})



df_oscars_final['number_W'] = df_oscars_final['number_W'].astype(int)
df_oscars_final['number_N'] = df_oscars_final['number_N'].astype(int)


df_oscars_final['number_W+N'] =  df_oscars_final['number_W'] + df_oscars_final['number_N']

df_oscars_final.to_csv("oscars_stage_3.csv", index=False)
df_oscars_final.to_excel("oscars_stage_3.xlsx", engine='xlsxwriter', index=False)