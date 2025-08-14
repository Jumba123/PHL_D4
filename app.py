import altair as alt
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

def Home_Page (df):
    Options = ["Points","PPG","Goals", "Assists"]
    Rank_Choice = st.pills("Rank By:", Options, default=Options[0], selection_mode="single")

    for option in Options:
        if Rank_Choice == option:
            df_temp = df.copy()
            
            # Group and sort by the selected stat
            df_temp = df_temp.groupby("Skaters", as_index=False).sum("Points")
            
            df_temp["PPG"] = df_temp["Points"] / df_temp["Games Played"]
            df_temp["PPG"] = df_temp["PPG"].round(2)
            df_temp.insert(7, "PPG", df_temp.pop("PPG"))
            df_temp = df_temp.drop(columns=["Skater_ID", "Week","Goals Allowed"])
            df_temp = df_temp.sort_values(option, ascending=False)


            # Games played filter
            slider_gp = st.slider("Games Played", 0, df_temp['Games Played'].max().round(0).astype(int), 0)
            df_temp = df_temp[df_temp['Games Played'] >= slider_gp]

            # Rank and display
            df_temp['Rank'] = df_temp[option].rank(method='dense', ascending=False)
            df_temp.insert(0, f"Rank ({option})", df_temp.pop("Rank"))
            df_temp = df_temp.set_index(f"Rank ({option})")
            st.dataframe(df_temp)
            break  # Stop after the matching option is processed

df = Pre_Process_CSV(df)
st.markdown(f"<h1 style='text-align: center;'>PHL D4 Data (Week 1-3 Not Included)</h1>", unsafe_allow_html=True)

Skater_Link, Goalie_Link, Weekly_Link= st.columns(3,border=True)
with Skater_Link:
    Skater_Link = st.button("Skater")
with Goalie_Link:
    Goalie_Link = st.button("Goalie")
with Weekly_Link:
    Weekly_Link = st.button("Weekly")
if Skater_Link:
    st.switch_page("pages/1_skater_stats.py")
if Goalie_Link:
    st.switch_page("pages/2_goalie_stats.py")
if Weekly_Link:
    st.switch_page("pages/3_weekly_stats.py")

Home_Page(df)
