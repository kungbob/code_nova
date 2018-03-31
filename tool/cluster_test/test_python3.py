import numpy as np # linear algebra
import pandas as pd
import matplotlib.pyplot as plt
import glob, os

df2 = pd.read_csv('solutions.csv')

# print(df2.head())

df3 = df2.set_index("Language")

# print(df3.groupby('Language').count())

# Combining both Python 3.1 & Python 3.4
df4 = df3.loc[["PYTH 3.1.2","PYTH 3.4"], :]

# print(df4.groupby('QCode').count().sort_values(by='SolutionUrl', ascending = False))

# Top 10 Question (containing correct & wrong & problematic submission):
# TSORT: 1169; TLG: 907; CHRL4: 391; CHEFSQ: 239; CONFLIP: 149;
# AMIFIB: 147; COMM3: 142; CHOPRT: 130; CARVANS: 129; COOKMACH: 127;

df5 = df4[(df4.Status == 'accepted')]

# Merging two solution.csv and program_codes
path = r'D:\code_nova\tool\cluster_test\program_codes'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
print(all_files)
df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file)
print(concatenated_df.columns)

merged = df5.merge(concatenated_df, on = 'SolutionID')
print(merged.head())
test_solution = merged
test_solution.to_csv("program_code_python_only.csv", encoding='utf-8')
