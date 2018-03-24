import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import glob, os

df2 = pd.read_csv('solutions.csv')

# print(df2.head())

df3 = df2.set_index("Language")

# print(df3.groupby('Language').count())

df4 = df3.loc["PYTH 3.1.2", :]

# print(df4.groupby('QCode').count().sort_values(by='SolutionUrl', ascending = False))

# Top 10 Question (containing correct & wrong & problematic submission):
# TSORT: 1169; TLG: 907; CHRL4: 391; CHEFSQ: 239; CONFLIP: 149;
# AMIFIB: 147; COMM3: 142; CHOPRT: 130; CARVANS: 129; COOKMACH: 127;

df5 = df4[df4.QCode == "TSORT"]

df6 = df5[(df5.Status == 'accepted') | (df5.Status == 'wrong answer')]

# Merging two solution.csv and program_codes
path = r'D:\Siemens\Testing\program_codes'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
print(all_files)
df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file)
print(concatenated_df.columns)

merged = df6.merge(concatenated_df, on = 'SolutionID')
print(merged.head())
test_solution = merged.Solutions
test_solution.to_csv("program_code.csv", encoding='utf-8')
