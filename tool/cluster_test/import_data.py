# from exercise.models import Exercise
import numpy as np # linear algebra
import pandas as pd

df2 = pd.read_csv('program_code_python_only.csv')

# print(df2.head())

# Iterate rows
for index, row in df2.iterrows():
    # print(row)
    Problem_name = row.QCode
    UserID = row.UserID
    Solution_text = row.Solutions
    print(Problem_name, UserID, Solution_text)
