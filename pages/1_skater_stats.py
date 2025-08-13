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

def Skater_Stats(df):
    df["PPG"] = df["Points"] / df["Games Played"]
    df["PPG"] = df["PPG"].round(2)
    df.insert(7, "PPG", df.pop("PPG"))
    df = df.drop(columns=["Skater_ID", "Week", "Team","Goals Allowed"])
    df = df.query(f"Position == 'S' ")
        
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

def Skater_Metrics(df,Skater_Select):
        df_Skater = df.query(f"Skaters == '{Skater_Select}' and Position == 'S' ")
        df = df.drop(columns=["Skater_ID","Week", "Team", "Goals Allowed"])
        df = df.query(f"Skaters == '{Skater_Select}' and Position == 'S' ")
        df = df.groupby("Skaters").sum("Points").sort_values("Points",ascending=False)

        df["PPG"] = df["Points"] / df["Games Played"]
        df["PPG"] = df["PPG"].round(2)
        df.insert(4, "PPG", df.pop("PPG"))
        
        Gp, Goals, Assists, Points, Ppg, Win, Loss = st.columns(7)
        Gp.metric("Games Played",df["Games Played"])
        Goals.metric("Goals",df["Goals"])
        Assists.metric("Assists",df["Assists"])
        Points.metric("Points",df["Points"])
        Ppg.metric("PPG",df["PPG"])
        Win.metric("Win",df["Win"])
        Loss.metric("Loss",df["Loss"])

        df_Skater = df_Skater[['Week', 'Skaters', 'Goals','Assists','Points','Team', 'Win', 'Loss', 'Games Played']].set_index('Week')
        st.markdown(f"<h6 style='text-align: center;'><em>{Skater_Select}'s Week by Week Stat Line</em></h6>", unsafe_allow_html=True)
        st.dataframe(df_Skater)

def Skater_Graph(df,Skater_Select):

    df = df.query(f"Skaters == '{Skater_Select}' and Position == 'S'").copy()
    df['Total_Points'] = df.groupby('Skaters')['Points'].cumsum()
    st.line_chart(df, x="Week", y="Total_Points")

    # df['Week'] = df['Week'].astype(int)
    # df['Week'].fillna(0, inplace=True)
    # Min_Week = df['Week'].min()
    # Max_Week = df['Week'].max()
    # st.dataframe(df['Week'])
    # chart = alt.Chart(df).mark_line().encode(
    #     x=alt.X('Week:Q',axis=alt.Axis(title="Week",values=list(range(int(Min_Week), int(Max_Week) + 1))), scale=alt.Scale(domain=[Min_Week, Max_Week])),
    #     y=alt.Y('Total_Points:Q',axis=alt.Axis(title="Total_Points")),
    #     tooltip=['Week:Q', 'Total_Points:Q']
    # ).interactive()

    # st.altair_chart(chart, use_container_width=True)

df = Pre_Process_CSV(df)

Filtered_Skaters = df.query(f"Position == 'S' ")
Skater_List = Filtered_Skaters["Skaters"].str.strip().drop_duplicates().sort_values(ascending=True)
Skater_Select = st.selectbox("Choose Skater", Skater_List,index=None,placeholder="Please Select Skater")

if Skater_Select:
    st.markdown(f"<h1 style='text-align: center;'>{Skater_Select} &#127954;</h1>", unsafe_allow_html=True)
    Skater_Metrics(df,Skater_Select)
    # Skater_Graph(df,Skater_Select)
else:
    st.title("Skater Stats")
    Skater_Stats(df)