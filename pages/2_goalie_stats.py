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

def Goalie_Stats(df):
    df["GAA"] = df["Goals Allowed"] / df["Games Played"]
    df["GAA"] = df["GAA"].round(2)
    df.insert(2, "GAA", df.pop("GAA"))
    df = df.drop(columns=["Skater_ID", "Week", "Team", "Goals", "Assists"])
    df = df.query(f"Position == 'G' ")
        
    Options = ["GAA","Goals Allowed"]
    Rank_Choice = st.pills("Rank By:", Options, default=Options[0], selection_mode="single")

    for option in Options:
        if Rank_Choice == option:
            df_temp = df.copy()

            # Group and sort by the selected stat
            df_temp = df_temp.groupby("Skaters",as_index=False).sum("Goals Allowed").sort_values("Skaters",ascending=True)

            # Games played filter
            slider_gp = st.slider("Games Played", 0, df_temp['Games Played'].max().round(0).astype(int), 0)
            df_temp = df_temp[df_temp['Games Played'] >= slider_gp]

            # Rank and display
            df_temp = df_temp[['Skaters', 'Goals Allowed', 'GAA','Games Played', 'Win', 'Loss', 'Points']]
            df_temp['Rank'] = df_temp[option].rank(method='dense', ascending=True)
            df_temp.insert(0, f"Rank ({option})", df_temp.pop("Rank"))
            df_temp = df_temp.set_index(f"Rank ({option})")
            df_temp = df_temp.sort_values(f"Rank ({option})",ascending=True)
            st.dataframe(df_temp)
            break  # Stop after the matching option is processed









        # df = df.query(f"Position == 'G' ")
        # df = df.drop(columns=["Skater_ID", "Week", "Team", "Goals", "Assists"])
        # df = df.groupby("Skaters",as_index=False).sum("Goals Allowed").sort_values("Skaters",ascending=True)

        # slider_gp = st.slider("Games Played", 0, df['Games Played'].max().round(0).astype(int),0)

        # df["GAA"] = df["Goals Allowed"] / df["Games Played"]
        # df["GAA"] = df["GAA"].round(2)
        # df.insert(2, "GAA", df.pop("GAA"))

        # df = df[df['Games Played'] >= slider_gp]
        # df = df[['Skaters','Games Played', 'Goals Allowed', 'GAA', 'Win', 'Loss', 'Points']]
        # df['Rank'] = df['GAA'].rank(method='dense', ascending=True)
        # df.insert(0, "Rank (GAA)", df.pop("Rank"))
        # df = df.set_index('Rank (GAA)')
        # df = df.sort_values("Rank (GAA)",ascending=True)
        # st.dataframe(df)

def Goalie_Metrics(df,Goalie_Select):
    if Goalie_Select:
        df_Goalie = df.query(f"Skaters == '{Goalie_Select}' and Position == 'G' ").copy()
        # Aggregate overall goalie stats
        df_summary = df_Goalie.groupby("Skaters", as_index=False).sum(numeric_only=True)
        df_summary["GAA"] = (df_summary["Goals Allowed"] / df_summary["Games Played"]).round(2)
        df_summary.insert(2, "GAA", df_summary.pop("GAA"))

        # Metrics
        Gp, Goals_Allowed, Gaa, Win, Loss, Points = st.columns(6)
        Gp.metric("Games Played", df_summary["Games Played"].iloc[0])
        Goals_Allowed.metric("Goals Allowed", df_summary["Goals Allowed"].iloc[0])
        Gaa.metric("GAA", df_summary["GAA"].iloc[0])
        Win.metric("Win", df_summary["Win"].iloc[0])
        Loss.metric("Loss", df_summary["Loss"].iloc[0])
        Points.metric("Points", df_summary["Points"].iloc[0])

        # Per-week stats
        df_Goalie["GAA"] = (df_Goalie["Goals Allowed"] / df_Goalie["Games Played"]).round(2)
        df_Goalie.insert(2, "GAA", df_Goalie.pop("GAA"))
        df_Goalie = df_Goalie[['Week','Team','Skaters','Games Played','Goals Allowed','GAA','Win','Loss','Points']].set_index('Week')

        st.markdown(f"<h6 style='text-align: center;'><em>{Goalie_Select}'s Week by Week Stat Line</em></h6>", unsafe_allow_html=True)
        st.dataframe(df_Goalie)

df = Pre_Process_CSV(df)

Filtered_Goalie = df.query(f"Position == 'G' ")
Goalie_List = Filtered_Goalie["Skaters"].str.strip().drop_duplicates().sort_values(ascending=True)
Goalie_Select = st.selectbox("Choose Goalie", Goalie_List,index=None,placeholder="Please Select Goalie")

if Goalie_Select:
    st.markdown(f"<h1 style='text-align: center;'>{Goalie_Select} &#127954;&#129349;</h1>", unsafe_allow_html=True)
    Goalie_Metrics(df,Goalie_Select)
else:
    st.text("Goalie Stats")
    Goalie_Stats(df)