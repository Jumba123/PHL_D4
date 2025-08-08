import altair as alt
import streamlit as st
import pandas as pd

pc_file = r"M:\Python Programs\PHL\PHL_D4_DATA.csv"
# python -m streamlit run "m:/Python Programs/PHL/main.py"
lp_file = r"C:\Users\Jm633\OneDrive\Desktop\Python\PHL\PHL_D4_DATA.csv"

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
        st.text("Skater Stats")
        df = df.drop(columns=["Skater_ID","Week", "Team", "Goals Allowed"])
        df = df.query(f"Position == 'S' ")
        df = df.groupby("Skaters",as_index=False).sum("Points").sort_values("Points",ascending=False)
        df['Rank'] = df['Points'].rank(method='dense', ascending=False)
        df.insert(0, "Rank (Points)", df.pop("Rank"))
        df = df.set_index('Rank (Points)')
        st.dataframe(df)

def Goalie_Stats(df):
        df = df.drop(columns=["Skater_ID", "Week", "Team", "Goals", "Assists"])
        df = df.query(f"Position == 'G' ")
        df = df.groupby("Skaters",as_index=False).sum("Goals Allowed").sort_values("Skaters",ascending=True)
        df["GAA"] = df["Goals Allowed"] / df["Games Played"]
        df["GAA"] = df["GAA"].round(2)
        df.insert(2, "GAA", df.pop("GAA"))

        df['Rank'] = df['GAA'].rank(method='dense', ascending=True)
        df.insert(0, "Rank (GAA)", df.pop("Rank"))
        df = df.set_index('Rank (GAA)')

        df = df[['Skaters','Games Played', 'Goals Allowed', 'GAA', 'Win', 'Loss', 'Points']]
        df = df.sort_values("Rank (GAA)",ascending=True)
        st.dataframe(df)

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

        df_Skater = df_Skater[['Week','Team', 'Skaters', 'Goals','Assists','Points', 'Win', 'Loss']]
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

def Goalie_Metrics(df,Goalie_Select):
    if Goalie_Select:
        df_Goalie = df.query(f"Skaters == '{Goalie_Select}' and Position == 'G' ")
        df = df.drop(columns=["Skater_ID", "Week", "Team", "Goals", "Assists"])
        df = df.query(f"Skaters == '{Goalie_Select}' and Position == 'G' ")
        df = df.groupby("Skaters").sum("Goals Allowed").sort_values("Goals Allowed",ascending=False)

        df["GAA"] = df["Goals Allowed"] / df["Games Played"]
        df["GAA"] = df["GAA"].round(2)
        df.insert(2, "GAA", df.pop("GAA"))

        Gp, Goals_Allowed, Gaa, Win, Loss, Points = st.columns(6)
        Gp.metric("Games Played",df["Games Played"])
        Goals_Allowed.metric("Goals Allowed",df["Goals Allowed"])
        Gaa.metric("GAA",df["GAA"])
        Win.metric("Win",df["Win"])
        Loss.metric("Loss",df["Loss"])
        Points.metric("Points",df["Points"])

        df_Goalie["GAA"] = df_Goalie["Goals Allowed"] / df_Goalie["Games Played"]
        df_Goalie["GAA"] = df_Goalie["GAA"].round(2)
        df_Goalie.insert(2, "GAA", df_Goalie.pop("GAA"))

        df_Goalie = df_Goalie[['Week','Team', 'Skaters','Games Played', 'Goals Allowed', 'GAA', 'Win', 'Loss', 'Points']]
        st.dataframe(df_Goalie)

def Skater_Fun(df):
    Filtered_Skaters = df.query(f"Position == 'S' ")
    Skater_List = Filtered_Skaters["Skaters"].str.strip().drop_duplicates().sort_values(ascending=True)
    Skater_Select = st.selectbox("Choose Skater", Skater_List,index=None,placeholder="Please Select Skater")
    if Skater_Select:
        Skater_Metrics(df,Skater_Select)
        # Skater_Graph(df,Skater_Select)
    else:
        Skater_Stats(df)

def Goalie_Fun(df):
    Filtered_Goalie = df.query(f"Position == 'G' ")
    Goalie_List = Filtered_Goalie["Skaters"].str.strip().drop_duplicates().sort_values(ascending=True)
    Goalie_Select = st.selectbox("Choose Goalie", Goalie_List,index=None,placeholder="Please Select Goalie")
    if Goalie_Select:
        Goalie_Metrics(df,Goalie_Select)
    else:
        Goalie_Stats(df)
    
st.title("PHL D4 Player Data (Week 1 - 3 Not Included)")
df = Pre_Process_CSV(df)
Skater_Fun(df)
Goalie_Fun(df)

