import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotting import subplots, individual_plots


df = pd.read_csv("gaming_laptops2_cleaned.csv")
print(df.head())
df.info()

print('Starting EDA : ...')
print("\n")

print(df['Price'].describe())
print(df['GPU'].value_counts())
print(df['CPU'].value_counts())

subplots(df)