#explore.py
#Author: Keerthana Pallela
#Module 14 Lab: Clean a Messy Sales CSV

# Self-Assessment
# 1.
# 2.
# 3.

import pandas as pd

print("----Exercise 1: Inspect----")
df = pd.read_csv("data/messy_sales.csv")
df.info()
print(df.isnull().sum())
print((df.isnull().mean() * 100).round(2))  # percent missing
print(df.head(20))