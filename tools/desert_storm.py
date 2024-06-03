import pandas as pd
import numpy as np

# Load data from a CSV file
data = pd.read_csv('data.csv')

# Exclude the first 5 based on the highest scores
sorted_data = data.sort_values(by='Score', ascending=False)
top5 = sorted_data.head(5)
others = sorted_data.iloc[5:]

# Filter eligible players who can participate next time
eligible_players = others[others['Participating Next'] == 'Y'].copy()

# Give priority to those who did not participate last time
eligible_players['priority'] = (eligible_players['Participated Last Time'] == 'N').astype(int)
eligible_players = eligible_players.sort_values(by='priority', ascending=False)

# Shuffle the eligible players
eligible_players = eligible_players.sample(frac=1, random_state=42).reset_index(drop=True)

# Select primary participants and reserves
primary_players = eligible_players.head(15)
reserves = eligible_players.iloc[15:25]

# Update participation status
data['Participating Next'] = 'N'  # Set all to 'N' first
data.loc[primary_players.index, 'Participating Next'] = 'Y'
data.loc[reserves.index, 'Participating Next'] = 'Y'

# Save the updated dataframe to a new CSV file
data.to_csv('updated_participation_status.csv', index=False)

print("Participants and reserves have been selected and saved.")