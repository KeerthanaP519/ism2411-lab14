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


# Data quality issues (add the counts from the output above):
# 1. Some columns have fewer non-null values than there are rows (missing data).
# 2. Unit price is read as text, not float, if it contains "$" and "," symbols.
# 3. Order date is read as text, not datetime, and may mix formats and junk
#    such as "TBD".
# 4. Column names need one consistent style (lowercase with underscores).
 
print("---- Exercise 2: Standardize column names----")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())
 
print("----Exercise 3: Handle missing values----")
print("Shape before:", df.shape)
 
# order_id and order_date identify the order and place it in time. A made-up
# value would create a false record, so rows missing either one are dropped.
df = df.dropna(subset=["order_id", "order_date"]).copy()
 
# A mean needs numbers, so remove currency symbols and thousands commas first.
df["unit_price"] = pd.to_numeric(
    df["unit_price"].astype(str).str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False).str.strip(),
    errors="coerce",
)
df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
 
# Few values are missing, so the mean keeps those orders without moving the
# column average. The 9999 placeholder is left out of the quantity mean because
# it would inflate the filled value.
df["unit_price"] = df["unit_price"].fillna(round(df["unit_price"].mean(), 2))
quantity_mean = df.loc[df["quantity_sold"] != 9999, "quantity_sold"].mean()
df["quantity_sold"] = df["quantity_sold"].fillna(round(quantity_mean))
 
print("Shape after:", df.shape)
print(df.isnull().sum())
 
print("----Exercise 4: Fix types----")
raw_dates = df["order_date"]
df["order_date"] = pd.to_datetime(raw_dates, errors="coerce")
print("Dates that became NaT:", df["order_date"].isna().sum())
 
# Real dates typed in another format also fail the first pass. Parse only those
# again, one at a time, so valid orders keep their date. Junk stays NaT.
failed = df["order_date"].isna()
df.loc[failed, "order_date"] = pd.to_datetime(
    raw_dates[failed], format="mixed", errors="coerce"
)
print("NaT after second pass:", df["order_date"].isna().sum())
 
df["unit_price"] = df["unit_price"].astype(float)
df["quantity_sold"] = df["quantity_sold"].astype(int)
df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)
print(df.dtypes)
 
print("----Exercise 5: Duplicates----")
# Fully identical rows would count the same sale twice.
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Shape after removing duplicates:", df.shape)
 
print("----Exercise 6: Describe----")
print(df.describe())
 
# Suspicious statistics (confirm against the table above):
# 1. A negative minimum price/revenue: likely returns or refunds.
# 2. A maximum quantity of 9999: a typed placeholder, not a real order.
# 3. Mean far from the median (50%) for quantity or revenue: extreme values
#    such as the placeholder or a few very large orders pull the mean.
 
# 9999 is clearly an entry error and would badly overstate revenue, so drop it.
# Negative revenues stay: they are returns, real money paid back to customers.
df = df[df["quantity_sold"] != 9999]
print(df.describe())
 
print("----Exercise 7: Save----")
df.to_csv("data/clean_sales.csv", index=False)
 
pd.read_csv("data/clean_sales.csv").info()  # order_date comes back as text
 
# CSV has no date type, so ask pandas to parse the column. Use this in Lab 15.
check = pd.read_csv("data/clean_sales.csv", parse_dates=["order_date"])
check.info()
print("Final shape:", check.shape)
 
