import pandas as pd
import pickle
from column_headings import *

df = pd.read_excel("Extract_003.xlsx")
df = df.iloc[5:]
#print(df.iat[10000,SCORE])

with open('election_data.pkl', 'wb') as f:
    pickle.dump(df, f)
