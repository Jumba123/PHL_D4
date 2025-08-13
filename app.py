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
    df["PPG"] = df["Points"] / df["Games Played"]
    df["PPG"] = df["PPG"].round(2)
    df.insert(7, "PPG", df.pop("PPG"))
    df = df.drop(columns=["Skater_ID", "Week", "Team","Goals Allowed"])

    Options = ["Points","PPG","Goals", "Assists"]
    Rank_Choice = st.pills("Rank By:", Options, default=Options[0], selection_mode="single")

    for option in Options:
        if Rank_Choice == option:
            df_temp = df.copy()

            # Group and sort by the selected stat
            df_temp = df_temp.groupby("Skaters", as_index=False).sum(option).sort_values(option, ascending=False)

            # Games played filter
            slider_gp = st.slider("Games Played", 0, df_temp['Games Played'].max().round(0).astype(int), 0)
            df_temp = df_temp[df_temp['Games Played'] >= slider_gp]

            # Rank and display
            df_temp['Rank'] = df_temp[option].rank(method='dense', ascending=False)
            df_temp.insert(0, f"Rank ({option})", df_temp.pop("Rank"))
            df_temp = df_temp.set_index(f"Rank ({option})")
            st.dataframe(df_temp)
            break  # Stop after the matching option is processed


    # if Rank_Choice == Options[0]:
    #     df0 = df.copy()
    #     df0 = df0.groupby("Skaters",as_index=False).sum(Options[0]).sort_values(Options[0],ascending=False)
        
    #     slider_gp = st.slider("Games Played", 0, df0['Games Played'].max().round(0).astype(int),0)
    #     df0 = df0[df0['Games Played'] >= slider_gp]

    #     df0['Rank'] = df0[Options[0]].rank(method='dense', ascending=False)
    #     df0.insert(0, f"Rank ({Options[0]})", df0.pop("Rank"))
    #     df0 = df0.set_index(f'Rank ({Options[0]})')
    #     st.dataframe(df0)
    # elif Rank_Choice == Options[1]:
    #     df1 = df.copy()
    #     df1 = df1.groupby("Skaters",as_index=False).sum(Options[1]).sort_values(Options[0],ascending=False)
        
    #     slider_gp = st.slider("Games Played", 0, df1['Games Played'].max().round(0).astype(int),0)
        
    #     df1 = df1[df1['Games Played'] >= slider_gp]
    #     df1['Rank'] = df1[Options[1]].rank(method='dense', ascending=False)
    #     df1.insert(0, f"Rank ({Options[1]})", df1.pop("Rank"))
    #     df1 = df1.set_index(f'Rank ({Options[1]})')
    #     st.dataframe(df1)


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
