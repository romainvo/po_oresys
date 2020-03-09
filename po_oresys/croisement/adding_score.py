import sys,os,path,glob
import pandas as pd

#-----------------------------------------------------------------------------#
#------------------- Creating "scorex" columns in the file ------------------ #
#-----------------------------------------------------------------------------#


files = 'results_rd155_nb250.csv'

df = pd.read_csv(files)
df_scores = pd.read_csv("all_scores_090320.csv",sep=',', header='infer',error_bad_lines=False, index_col="id_bnb")
count = 3
countBis=0
print(df_scores.iloc[:,0])

while count <= len(df.columns):
    #df.insert(count,'score'+str((int(count/3)-1)),df_scores.iloc[:,countBis],allow_duplicates = True)
    df.loc[:,'score'+str((int(count/3)-1))]=df_scores.iloc[:, countBis]
    print(count)
    count=count+3
    countBis=countBis+1

df.to_csv(files,index=False)



 