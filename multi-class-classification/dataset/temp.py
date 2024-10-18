import pandas as pd

# Read the three CSV files
df_hdfs = pd.read_csv('hdfs1.csv')
df_windows = pd.read_csv('windows1.csv')
df_apache = pd.read_csv('apache1.csv')

# Concatenate the DataFrames into one
combined_df = pd.concat([df_hdfs, df_windows, df_apache], ignore_index=True)

# Shuffle the rows randomly
combined_df = combined_df.sample(frac=1).reset_index(drop=True)

# Save the combined and shuffled DataFrame to a new CSV file
combined_df.to_csv('combined.csv', index=False)

print("The CSV files have been combined and shuffled into 'combined.csv'.")
