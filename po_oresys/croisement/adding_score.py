import sys,os,path,glob
import pandas as pd

files = 'results_rd150_nb100.csv'

df = pd.read_csv(files)
#df = df.convert_objects(convert_numeric=True)
count = 3
while count<=len(df.columns) :
    df.insert(count,'score'+str((int(count/3)-1)),5,allow_duplicates = True)
    print(count)
    count=count+3

df.to_csv(files,index=False)

 