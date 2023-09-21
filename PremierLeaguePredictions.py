import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(
    page_title="EPL Predictions",
    page_icon="epl.jpg",
)

st.title("Premier League Match Day 6 Predictions")

DATA_URL = "https://www.football-data.co.uk/mmz4281/2324/E0.csv"


@st.cache_data
def load_data():
    dataset = pd.read_csv(DATA_URL)
    premier_league_data = dataset[['Date', 'Time', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
    premier_league_data.rename(columns={"FTHG": "Home Goals", "FTAG": "Away Goals"}, inplace=True)
    return premier_league_data


def create_overall_statistics(data, home_team, away_team):
    average_home_goals_scored = data['Home Goals'].mean()
    # print(f"Average home goals scored: {average_home_goals_scored :.2f}")

    average_away_goals_scored = data['Away Goals'].mean()
    # print(f"Average away goals scored: {average_away_goals_scored :.2f}")

    home_team_data = data[data['HomeTeam'] == home_team]
    away_team_data = data[data['AwayTeam'] == away_team]

    # compute statistics for home team
    avg_home_team_goals_scored_at_home = home_team_data['Home Goals'].mean()
    # print(f"Home team average goals scored at home {avg_home_team_goals_scored_at_home :.2f}")

    avg_home_team_goals_conceded_at_home = home_team_data['Away Goals'].mean()
    # print(f"Home team average goals conceded at home {avg_home_team_goals_conceded_at_home :.2f}")

    # compute statistics for away team
    avg_away_team_goals_scored_away = away_team_data['Away Goals'].mean()
    # print(f"Away team average goals scored away {avg_away_team_goals_scored_away :.2f}")

    avg_away_team_goals_conceded_away = away_team_data['Home Goals'].mean()
    # print(f"Away team average goals conceded away {avg_away_team_goals_conceded_away :.2f}")

    home_team_attacking_strength = avg_home_team_goals_scored_at_home / average_home_goals_scored
    # print(f"Home team attacking strength : {home_team_attacking_strength: .2f}")

    home_team_defensive_strength = avg_home_team_goals_conceded_at_home / average_away_goals_scored
    # print(f"Home team defensive strength : {home_team_defensive_strength: .2f}")

    away_team_attacking_strength = avg_away_team_goals_scored_away / average_away_goals_scored
    # print(f"Away team attacking strength: {away_team_attacking_strength :.2f}")

    away_team_defensive_strength = avg_away_team_goals_conceded_away / average_home_goals_scored
    # print(f"Away team defensive strength: {away_team_defensive_strength}")

    home_team_score_expectance = home_team_attacking_strength * away_team_defensive_strength * average_home_goals_scored
    # print(f"Home team score expectance: {home_team_score_expectance}")

    away_team_score_expectance = away_team_attacking_strength * home_team_defensive_strength * average_away_goals_scored
    # print(f"Away team score expectance: {away_team_score_expectance}")

    return home_team_score_expectance, away_team_score_expectance


# this function find the occurrence of goals inside poisson dist and return the probability to happen
def team_goals_probability(number_of_goals, poisson_dist):
    goals = 0
    prob = None
    for i in range(0, 10000):
        if poisson_dist[i] == number_of_goals:
            goals += 1
            prob = goals / 10000
    return goals, prob


loading_state = st.text("Loading Previous results...")
data = load_data()
loading_state.text("Load Complete")

match_day = {1: "Liverpool - West Ham", 2: 'Brentford - Everton', 3: 'Crystal Palace - Fulham',
             4: "Luton - Wolves", 5: "Man City - Nott\'m Forest", 6: "Burnley - Man United",
             7: "Arsenal - Tottenham", 8: "Brighton - Bournemouth", 9: "Chelsea - Aston Villa",
             10: "Sheffield United - Newcastle"}
image_source = {"Liverpool": "https://resources.premierleague.com/premierleague/badges/rb/t14.svg",
                "West Ham": "https://resources.premierleague.com/premierleague/badges/rb/t21.svg",
                "Brentford": "https://resources.premierleague.com/premierleague/badges/rb/t94.svg",
                "Everton": "https://resources.premierleague.com/premierleague/badges/rb/t11.svg",
                "Crystal Palace": "https://resources.premierleague.com/premierleague/badges/rb/t31.svg",
                "Fulham": "https://resources.premierleague.com/premierleague/badges/rb/t54.svg",
                "Luton": "https://resources.premierleague.com/premierleague/badges/rb/t102.svg",
                "Wolves": "https://resources.premierleague.com/premierleague/badges/rb/t39.svg",
                "Man City": "https://resources.premierleague.com/premierleague/badges/rb/t43.svg",
                "Nott\'m Forest": "https://resources.premierleague.com/premierleague/badges/rb/t17.svg",
                "Burnley": "https://resources.premierleague.com/premierleague/badges/rb/t90.svg",
                "Man United": "https://resources.premierleague.com/premierleague/badges/rb/t1.png",
                "Arsenal": "https://resources.premierleague.com/premierleague/badges/rb/t3.svg",
                "Tottenham": "https://resources.premierleague.com/premierleague/badges/rb/t6.svg",
                "Brighton": "https://resources.premierleague.com/premierleague/badges/rb/t36.svg",
                "Bournemouth": "https://resources.premierleague.com/premierleague/badges/rb/t91.svg",
                "Chelsea": "https://resources.premierleague.com/premierleague/badges/rb/t8.svg",
                "Aston Villa": "https://resources.premierleague.com/premierleague/badges/rb/t7.svg",
                "Sheffield United": "https://resources.premierleague.com/premierleague/badges/rb/t49.svg",
                "Newcastle": "https://resources.premierleague.com/premierleague/badges/rb/t4.png"
                }
team_color = {"Liverpool": "red",
              "West Ham": "brown",
              "Brentford": "#ff8d33",
              "Everton": "blue",
              "Crystal Palace": "#1711e0",
              "Fulham": "black",
              "Luton": "#e0ae11",
              "Wolves": "#e09211",
              "Man City": "#0bdeef",
              "Nott\'m Forest": "#ef2a0b",
              "Burnley": "#8e2b4e",
              "Man United": "#d12f07",
              "Arsenal": "#ff0101",
              "Tottenham": "#a5bfcc",
              "Brighton": "#228bbf",
              "Bournemouth": "#e50e21",
              "Chelsea": "#0e1ee5",
              "Aston Villa": "#a4266f",
              "Sheffield United": "#e31343",
              "Newcastle": "#d5c0c5"}

choose_match = st.selectbox(label='Select a match', options=match_day.values())
home_team = choose_match.split("-")[0].strip()
away_team = choose_match.split("-")[1].strip()


col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{home_team} home results")
with col2:
    st.image(image_source.get(home_team))

filtered_data = data[data["HomeTeam"] == home_team]
st.write(filtered_data)

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{away_team} away results")
with col2:
    if image_source.get(away_team) is not None:
        st.image(image_source.get(away_team))
filtered_data = data[data["AwayTeam"] == away_team]
st.write(filtered_data)

# compute λ for each team
expected_goals_home, expected_goals_away = create_overall_statistics(data, home_team, away_team)

# draw a sample from poisson dist based on scoring expectancy
home_team_poisson = np.random.poisson(lam=expected_goals_home, size=100000)
away_team_poisson = np.random.poisson(lam=expected_goals_away, size=100000)


# calculate the probability for each team to score from 0 to 5 goals
home_chances = []
away_chances = []

for i in range(0, 6):
    h_goals_occurrences_in_poisson_dist, h_prob = team_goals_probability(i, home_team_poisson)
    home_chances.append(h_prob)
    a_goals_occurrences_in_poisson_dist, a_prob = team_goals_probability(i, away_team_poisson)
    away_chances.append(a_prob)

prob_dist = {
    "Probalities of home team to score": home_chances,
    "Probalities of away team to score": away_chances
}

# the probabilities for each team to score again each other
prob_df = pd.DataFrame(prob_dist)

# plot the poisson distribution for both team
st.subheader(f"{home_team} vs {away_team} scoring probabilities")
plt.plot(prob_df.index, prob_df['Probalities of home team to score'], marker='o', color=team_color.get(home_team), label=home_team)
plt.plot(prob_df.index, prob_df['Probalities of away team to score'], marker='o', color=team_color.get(away_team), label=away_team)
plt.xlabel("Goals to score")
plt.ylabel("Probability of scoring")
plt.legend()
st.pyplot(plt)

# create the dot matrix in order to be able to compute the probability of winning for each team
# also we can see the chances of each score to occur
home_team_prob = pd.DataFrame(home_chances, columns=['Probabilities'])
away_team_prob = pd.DataFrame(away_chances, columns=['Probabilities'])

# diagonal sum : prob to have tie
# upper diagonal sum : prob of away team to win
# lower diagonal sum : prob of home team to win
final_probabilities = home_team_prob.dot(away_team_prob.T)

tie_prob = 0
home_win = 0
away_win = 0
for i in range(0, 6):
    for j in range(0, 6):
        if i == j:
            tie_prob += final_probabilities[i][j]
        elif i > j:
            away_win += final_probabilities[i][j]
        else:
            home_win += final_probabilities[i][j]

# print(f"Home win prob: {home_win}")
# print(f"Away win prob: {away_win}")
# print(f"Tie: {tie_prob}")


test = {
    home_team: [home_win],
    "Tie": [tie_prob],
    away_team: [away_win]

}
chart_data = pd.DataFrame(test)
# print(chart_data.head())

data = pd.melt(chart_data.reset_index(), id_vars=["index"])

# Horizontal stacked bar chart
domain = [home_team, "Tie", away_team]
range_ = [team_color.get(home_team), "gray", team_color.get(away_team)]
chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title=""),
        color=alt.Color("variable", scale=alt.Scale(domain=domain, range=range_), type="nominal", title=""),
        order=alt.Order("variable", sort="ascending"),
    )
)

st.subheader("Final Predictions")
col1, col2, col3 = st.columns(3)

with col1:
    st.image(image_source.get(home_team))
with col2:
    st.subheader(f"vs")
with col3:
    st.image(image_source.get(away_team))
st.altair_chart(chart, use_container_width=True)

