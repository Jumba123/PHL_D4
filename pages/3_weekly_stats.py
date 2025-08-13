import streamlit as st
import pandas as pd

url = 'https://raw.githubusercontent.com/Jumba123/PHL_D4/refs/heads/main/PHL_D4_DATA.csv'

df = pd.read_csv(url)

def Pre_Process_CSV(df):
    df['Skaters'] = df['Skaters'].str.title()
    df['Games Played'] = df['Games Played'].astype(int)
    df['Goals'] = df['Goals'].astype(int)
    df['Assists'] = df['Assists'].astype(int)
    df['Goals Allowed'] = df['Goals Allowed'].astype(int)
    df['Win'] = df['Win'].astype(int)
    df['Loss'] = df['Loss'].astype(int)
    df['Week'] = df['Week'].astype(int)

    df["Points"] = df["Goals"] + df["Assists"]
    df.insert(5, "Points", df.pop("Points"))

    df["GAA"] = df["Goals Allowed"] / df["Games Played"]
    df["GAA"] = df["GAA"].round(2)
    df.insert(6, "GAA", df.pop("GAA"))
    
    df = df[['Skater_ID','Skaters', 'Position', 'Games Played', 'Goals', 'Assists', 'Points','Win', 'Loss', 'Goals Allowed', 'Week', 'Team']]
    
    return df

df = Pre_Process_CSV(df)
st.markdown(f"<h1 style='text-align: center;'>Weekly Stats</h1>", unsafe_allow_html=True)
st.markdown(f"<h6 style='text-align: center;'><em>Top 3 Scorers and Top Goalie *Min 4 GP* Each Week</em></h6>", unsafe_allow_html=True)

min_week = df["Week"].min()
max_week = df["Week"].max()

df = df.drop(columns=["Skater_ID","Win","Loss"])
df["GAA"] = (df["Goals Allowed"] / df["Games Played"]).round(2)
df.insert(2, "GAA", df.pop("GAA"))
df = df[['Skaters', 'Goals','Assists','Points','Team','Week','Games Played','Goals Allowed','GAA','Position']]

for i in range(min_week,max_week+1,1):
    st.markdown(f"<h4 style='text-align: left;'>Week {i}</h4>", unsafe_allow_html=True)
    df_temp = df.copy()
    df_temp = df_temp.query(f"Week == {i}")
    df_temp = df_temp.nlargest(3,"Points")
    df_temp = df_temp[['Skaters', 'Goals','Assists','Points','Team','Week']]
    st.table(df_temp.set_index('Skaters').drop(columns=["Week"]))

    # --- Top Goalie (min 4 GP) ---
    df_goalie_temp = df.copy()
    df_goalie_temp = df_goalie_temp.query(f"Week == {i} and Position == 'G' and `Games Played` >= 4")

    # Recalculate GAA after grouping
    df_goalie_temp["GAA"] = (df_goalie_temp["Goals Allowed"] / df_goalie_temp["Games Played"]).round(2)
    df_goalie_temp = df_goalie_temp.nsmallest(1, "GAA")
    df_goalie_temp = df_goalie_temp[['Skaters', 'GAA','Goals Allowed','Team','Week']]
    df_goalie_temp.rename(columns={'Skaters': 'Goalie'}, inplace=True)
    st.table(df_goalie_temp.set_index('Goalie').drop(columns=["Week"]))



    

# for option in Options:
#     if Rank_Choice == option:
#         df_temp = df.copy()

#         # Group and sort by the selected stat
#         df_temp = df_temp.groupby("Skaters", as_index=False).sum(option).sort_values(option, ascending=False)

#         # Games played filter
#         slider_gp = st.slider("Games Played", 0, df_temp['Games Played'].max().round(0).astype(int), 0)
#         df_temp = df_temp[df_temp['Games Played'] >= slider_gp]

#         # Rank and display
#         df_temp['Rank'] = df_temp[option].rank(method='dense', ascending=False)
#         df_temp.insert(0, f"Rank ({option})", df_temp.pop("Rank"))
#         df_temp = df_temp.set_index(f"Rank ({option})")
#         st.dataframe(df_temp)
#         break  # Stop after the matching option is processed