---
title: "WNBA Regular Season Blowouts"
date: 2025-07-05 00:05:00
draft: false
toc: false
tags:
  - python
  - data parsing
  - data extraction
  - data analysis
  - WNBA
  - WNBA Regular Season Statistics
  - Web Scraping
  - python for sports
  - pandas
  - seaborn
  - data visualization
  - scipy
  - matplotlib
  - numpy
  - BeautifulSoup
  - json
  - csv
  - kaggle
  - kaggle datasets
---

Given that we've been doing some work with the NBA and "blowouts" in a couple of different posts---one [here](https://kspicer80.github.io/posts/2025-05-24-nba-playoff-blowouts/) and another [here](https://kspicer80.github.io/posts/2026-06-24-nba-regular-season-blowouts/)---I thought we might look at the WNBA too. So, first step, I found a [Kaggle dataset](https://www.kaggle.com/datasets/rafaelgreca/wnba-games-box-score-since-1997) that gave us data up until 2020, if I remember correctly. We then wrote some code to update to the most latest games:

``` python
import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguegamelog
from datetime import datetime
import time

# --- Configuration ---
ORIGINAL_CSV = "1997-2020_officialBoxScore.csv"
UPDATED_CSV = "1997-2024_officialBoxScore.csv"
START_YEAR = 2020
END_YEAR = 2024

# Load the existing dataset
print(f"Loading existing dataset: {ORIGINAL_CSV}")
df_existing = pd.read_csv(ORIGINAL_CSV)

# List to store new game data
new_games = []

print(f"Fetching WNBA data from {START_YEAR} to {END_YEAR} using nba_api...")
for year in range(START_YEAR, END_YEAR + 1):
    season_str = f"{year}-{str(year+1)[2:]}"
    print(f"Fetching data for season: {season_str}")

    try:
        # Fetch league game log for the season
        game_logs = leaguegamelog.LeagueGameLog(
            league_id='10',  # WNBA League ID
            season=season_str,
            season_type_all_star='Regular Season'
        ).get_data_frames()[0]

        if game_logs.empty:
            print(f"No game log data found for {season_str}.")
            continue

        # Debug: Print available columns
        print(f"Available columns for {season_str}: {game_logs.columns.tolist()}")

        # Group by game_id to process each game
        games = game_logs.groupby('GAME_ID')
        for game_id, game_data in games:
            # Each game should have two teams
            if len(game_data) != 2:
                print(f"Skipping game {game_id}: Expected 2 teams, found {len(game_data)}")
                continue

            team1_data = game_data.iloc[0]
            team2_data = game_data.iloc[1]

            # Determine home and away teams (approximate based on MATCHUP)
            if 'MATCHUP' in team1_data and '@' in team1_data['MATCHUP']:
                away_team = team1_data
                home_team = team2_data
            else:
                home_team = team1_data
                away_team = team2_data

            # Game date
            game_date = pd.to_datetime(team1_data['GAME_DATE']).strftime('%Y-%m-%d')

            # Determine winner
            home_points = home_team['PTS']
            away_points = away_team['PTS']
            if home_points > away_points:
                home_result = 'Win'
                away_result = 'Loss'
                winner = home_team['TEAM_ABBREVIATION']
            else:
                home_result = 'Loss'
                away_result = 'Win'
                winner = away_team['TEAM_ABBREVIATION']

            # Calculate team possessions (simplified)
            def calculate_possessions(fga, to, fta):
                return fga + to + 0.4 * fta  # Simplified approximation

            # Map data to features for both teams
            for team_data, loc, rslt, oppt_data in [
                (home_team, 'Home', home_result, away_team),
                (away_team, 'Away', away_result, home_team)
            ]:
                fga = team_data['FGA']
                fgm = team_data['FGM']
                fg_pct = (fgm / fga * 100) if fga > 0 else 0
                two_pa = team_data['FGA'] - team_data.get('FG3A', 0)
                two_pm = two_pa - (team_data.get('FG3A', 0) - team_data.get('FG3M', 0))
                two_p_pct = (two_pm / two_pa * 100) if two_pa > 0 else 0
                three_pa = team_data.get('FG3A', 0)
                three_pm = team_data.get('FG3M', 0)
                three_p_pct = (three_pm / three_pa * 100) if three_pa > 0 else 0
                fta = team_data['FTA']
                ftm = team_data['FTM']
                ft_pct = (ftm / fta * 100) if fta > 0 else 0
                orb = team_data.get('OREB', 0)
                drb = team_data.get('DREB', 0)
                trb = orb + drb
                to = team_data.get('TO', 0)  # Use 'TO' instead of 'TURNOVERS'
                ast = team_data['AST']
                stl = team_data['STL']
                blk = team_data['BLK']
                pf = team_data['PF']
                pts = team_data['PTS']
                min_played = 240  # Approximate as 48 minutes * 5 players

                # Opponent stats
                oppt_fga = oppt_data['FGA']
                oppt_fgm = oppt_data['FGM']
                oppt_fg_pct = (oppt_fgm / oppt_fga * 100) if oppt_fga > 0 else 0
                oppt_two_pa = oppt_fga - oppt_data.get('FG3A', 0)
                oppt_two_pm = oppt_two_pa - (oppt_data.get('FG3A', 0) - oppt_data.get('FG3M', 0))
                oppt_two_p_pct = (oppt_two_pm / oppt_two_pa * 100) if oppt_two_pa > 0 else 0
                oppt_three_pa = oppt_data.get('FG3A', 0)
                oppt_three_pm = oppt_data.get('FG3M', 0)
                oppt_three_p_pct = (oppt_three_pm / oppt_three_pa * 100) if oppt_three_pa > 0 else 0
                oppt_fta = oppt_data['FTA']
                oppt_ftm = oppt_data['FTM']
                oppt_ft_pct = (oppt_ftm / oppt_fta * 100) if oppt_fta > 0 else 0
                oppt_orb = oppt_data.get('OREB', 0)
                oppt_drb = oppt_data.get('DREB', 0)
                oppt_trb = oppt_orb + oppt_drb
                oppt_to = oppt_data.get('TO', 0)
                oppt_ast = oppt_data['AST']
                oppt_stl = oppt_data['STL']
                oppt_blk = oppt_data['BLK']
                oppt_pf = oppt_data['PF']
                oppt_pts = oppt_data['PTS']

                # Advanced stats calculations
                team_poss = calculate_possessions(fga, to, fta)
                oppt_poss = calculate_possessions(oppt_fga, oppt_to, oppt_fta)

                treb_pct = (trb * 100) / (trb + oppt_trb) if (trb + oppt_trb) > 0 else 0
                asst_pct = (ast / fgm) * 100 if fgm > 0 else 0
                ts_pct = pts / (2 * (fga + (fta * 0.44))) * 100 if (fga + (fta * 0.44)) > 0 else 0
                efg_pct = (fgm + (three_pm / 2)) / fga * 100 if fga > 0 else 0
                oreb_pct = (orb * 100) / (orb + oppt_drb) if (orb + oppt_drb) > 0 else 0
                dreb_pct = (drb * 100) / (drb + oppt_orb) if (drb + oppt_orb) > 0 else 0
                to_pct = (to * 100) / (fga + 0.44 * fta + to) if (fga + 0.44 * fta + to) > 0 else 0
                stl_pct = (stl * 100) / team_poss if team_poss > 0 else 0
                blk_pct = (blk * 100) / team_poss if team_poss > 0 else 0
                blkr = (blk * 100) / oppt_two_pa if oppt_two_pa > 0 else 0
                pps = pts / fga if fga > 0 else 0
                fic = pts + orb + (0.75 * drb) + ast + stl + blk - (0.75 * fga) - (0.375 * fta) - to - (0.5 * pf)
                fic40 = (fic * 40 * 5) / min_played if min_played > 0 else 0
                ortg = (pts * 100) / team_poss if team_poss > 0 else 0
                drtg = (oppt_pts * 100) / team_poss if team_poss > 0 else 0
                ediff = ortg - drtg
                play_pct = fgm / (fga - orb + to) if (fga - orb + to) > 0 else 0
                ar = (ast * 100) / (fga - 0.44 * fta + ast + to) if (fga - 0.44 * fta + ast + to) > 0 else 0
                ast_to = ast / to if to > 0 else 0
                pace = (team_poss * 48 * 5) / min_played if min_played > 0 else 0
                stl_to = stl / to if to > 0 else 0

                # Opponent advanced stats
                oppt_treb_pct = (oppt_trb * 100) / (oppt_trb + trb) if (oppt_trb + trb) > 0 else 0
                oppt_asst_pct = (oppt_ast / oppt_fgm) * 100 if oppt_fgm > 0 else 0
                oppt_ts_pct = oppt_pts / (2 * (oppt_fga + (oppt_fta * 0.44))) * 100 if (oppt_fga + (oppt_fta * 0.44)) > 0 else 0
                oppt_efg_pct = (oppt_fgm + (oppt_three_pm / 2)) / oppt_fga * 100 if oppt_fga > 0 else 0
                oppt_oreb_pct = (oppt_orb * 100) / (oppt_orb + drb) if (oppt_orb + drb) > 0 else 0
                oppt_dreb_pct = (oppt_drb * 100) / (oppt_drb + orb) if (oppt_drb + orb) > 0 else 0
                oppt_to_pct = (oppt_to * 100) / (oppt_fga + 0.44 * oppt_fta + oppt_to) if (oppt_fga + 0.44 * oppt_fta + oppt_to) > 0 else 0
                oppt_stl_pct = (oppt_stl * 100) / oppt_poss if oppt_poss > 0 else 0
                oppt_blk_pct = (oppt_blk * 100) / oppt_poss if oppt_poss > 0 else 0
                oppt_blkr = (oppt_blk * 100) / two_pa if two_pa > 0 else 0
                oppt_pps = oppt_pts / oppt_fga if oppt_fga > 0 else 0
                oppt_fic = oppt_pts + oppt_orb + (0.75 * oppt_drb) + oppt_ast + oppt_stl + oppt_blk - (0.75 * oppt_fga) - (0.375 * oppt_fta) - oppt_to - (0.5 * oppt_pf)
                oppt_fic40 = (oppt_fic * 40 * 5) / min_played if min_played > 0 else 0
                oppt_ortg = (oppt_pts * 100) / oppt_poss if oppt_poss > 0 else 0
                oppt_drtg = (pts * 100) / oppt_poss if oppt_poss > 0 else 0
                oppt_ediff = oppt_ortg - oppt_drtg
                oppt_play_pct = oppt_fgm / (oppt_fga - oppt_orb + oppt_to) if (oppt_fga - oppt_orb + oppt_to) > 0 else 0
                oppt_ar = (oppt_ast * 100) / (oppt_fga - 0.44 * oppt_fta + oppt_ast + oppt_to) if (oppt_fga - 0.44 * oppt_fta + oppt_ast + oppt_to) > 0 else 0
                oppt_ast_to = oppt_ast / oppt_to if oppt_to > 0 else 0
                oppt_pace = (oppt_poss * 48 * 5) / min_played if min_played > 0 else 0
                oppt_stl_to = oppt_stl / oppt_to if oppt_to > 0 else 0

                game_record = {
                    'gmDate': game_date,
                    'seasonType': 'Regular',
                    'season': season_str,
                    'teamWins': 0,
                    'teamLosses': 0,
                    'teamAbbr': team_data['TEAM_ABBREVIATION'],
                    'teamLoc': loc,
                    'teamRslt': rslt,
                    'teamDayOff': 0,
                    'teamPTS': pts,
                    'teamAST': ast,
                    'teamTO': to,
                    'teamMin': min_played,
                    'teamSTL': stl,
                    'teamBLK': blk,
                    'teamPF': pf,
                    'teamFGA': fga,
                    'teamFGM': fgm,
                    'teamFG%': fg_pct,
                    'team2PA': two_pa,
                    'team2PM': two_pm,
                    'team2P%': two_p_pct,
                    'team3PA': three_pa,
                    'team3PM': three_pm,
                    'team3P%': three_p_pct,
                    'teamFTA': fta,
                    'teamFTM': ftm,
                    'teamFT%': ft_pct,
                    'teamORB': orb,
                    'teamDRB': drb,
                    'teamTRB': trb,
                    'teamTREB%': treb_pct,
                    'teamASST%': asst_pct,
                    'teamTS%': ts_pct,
                    'teamEFG%': efg_pct,
                    'teamOREB%': oreb_pct,
                    'teamDREB%': dreb_pct,
                    'teamTO%': to_pct,
                    'teamSTL%': stl_pct,
                    'teamBLK%': blk_pct,
                    'teamBLKR': blkr,
                    'teamPPS': pps,
                    'teamFIC': fic,
                    'teamFIC40': fic40,
                    'teamOrtg': ortg,
                    'teamDrtg': drtg,
                    'teamEDiff': ediff,
                    'teamPlay%': play_pct,
                    'teamAR': ar,
                    'teamPoss': team_poss,
                    'teamAST/TO': ast_to,
                    'teamPace': pace,
                    'teamSTL/TO': stl_to,
                    'opptWins': 0,
                    'opptLosses': 0,
                    'opptAbbr': oppt_data['TEAM_ABBREVIATION'],
                    'opptLoc': 'Away' if loc == 'Home' else 'Home',
                    'opptRslt': 'Loss' if rslt == 'Win' else 'Win',
                    'opptDayOff': 0,
                    'opptPTS': oppt_pts,
                    'opptAST': oppt_ast,
                    'opptTO': oppt_to,
                    'opptMin': min_played,
                    'opptSTL': oppt_stl,
                    'opptBLK': oppt_blk,
                    'opptPF': oppt_pf,
                    'opptFGA': oppt_fga,
                    'opptFGM': oppt_fgm,
                    'opptFG%': oppt_fg_pct,
                    'oppt2PA': oppt_two_pa,
                    'oppt2PM': oppt_two_pm,
                    'oppt2P%': oppt_two_p_pct,
                    'oppt3PA': oppt_three_pa,
                    'oppt3PM': oppt_three_pm,
                    'oppt3P%': oppt_three_p_pct,
                    'opptFTA': oppt_fta,
                    'opptFTM': oppt_ftm,
                    'opptFT%': ft_pct,
                    'opptORB': oppt_orb,
                    'opptDRB': oppt_drb,
                    'opptTRB': oppt_trb,
                    'opptTREB%': oppt_treb_pct,
                    'opptASST%': oppt_asst_pct,
                    'opptTS%': oppt_ts_pct,
                    'opptEFG%': oppt_efg_pct,
                    'opptOREB%': oppt_oreb_pct,
                    'opptDREB%': oppt_dreb_pct,
                    'opptTO%': oppt_to_pct,
                    'opptSTL%': oppt_stl_pct,
                    'opptBLK%': oppt_blk_pct,
                    'opptBLKR': oppt_blkr,
                    'opptPPS': oppt_pps,
                    'opptFIC': oppt_fic,
                    'opptFIC40': oppt_fic40,
                    'opptOrtg': oppt_ortg,
                    'opptDrtg': oppt_drtg,
                    'opptEDiff': oppt_ediff,
                    'opptPlay%': oppt_play_pct,
                    'opptAR': oppt_ar,
                    'opptPoss': oppt_poss,
                    'opptAST/TO': oppt_ast_to,
                    'opptPace': oppt_pace,
                    'opptSTL/TO': oppt_stl_to,
                    'matchWinner': winner
                }
                new_games.append(game_record)

        print(f"Processed {len(games)} games for season {season_str}.")
        time.sleep(1)  # Respect API rate limits

    except Exception as e:
        print(f"Error fetching data for season {season_str}: {e}")
        continue

# Create a DataFrame for new data
if new_games:
    df_new = pd.DataFrame(new_games)
    # Ensure columns match the existing dataset
    df_new = df_new[df_existing.columns]
    # Combine datasets
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    # Save the updated dataset
    df_combined.to_csv(UPDATED_CSV, index=False)
    print(f"Updated dataset saved as {UPDATED_CSV} with {len(df_combined)} rows.")
else:
    print("No new data was collected.")
```

Now, with the updated dataset, we can write some code to plot the blowouts and their proportions over time:

![blowout_counts](/images/imgforblogposts/post_45/wnba_blowout_counts.png)

![blowout_proportions](/images/imgforblogposts/post_45/wnba_blowout_proportions.png)

Script to produce this is here:

``` python
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file (replace 'wnba_games.csv' with your actual file path)
df = pd.read_csv('1997-2025_officialBoxScore.csv')

# Calculate margin of victory
df['margin'] = abs(df['teamPTS'] - df['opptPTS'])

# Identify blowout games (margin > 20)
df['is_blowout'] = df['margin'] > 20

# Group by season to get blowout counts and total games
blowout_counts = df.groupby('season').agg({
    'is_blowout': 'sum',  # Count of blowout games
    'gmDate': 'count'     # Total games
}).rename(columns={'gmDate': 'total_games', 'is_blowout': 'blowout_games'})

# Calculate proportion of blowout games
blowout_counts['blowout_proportion'] = blowout_counts['blowout_games'] / blowout_counts['total_games']

# Plot 1: Number of blowout games per season
plt.figure(figsize=(10, 6))
plt.plot(blowout_counts.index, blowout_counts['blowout_games'], marker='o')
plt.title('Number of WNBA Blowout Games (Margin > 20) per Season')
plt.xlabel('Season')
plt.ylabel('Number of Blowout Games')
plt.grid(True)
plt.xticks(blowout_counts.index, rotation=45)
plt.tight_layout()
plt.savefig('wnba_blowout_counts.png')
plt.close()

# Plot 2: Proportion of blowout games per season
plt.figure(figsize=(10, 6))
plt.plot(blowout_counts.index, blowout_counts['blowout_proportion'], marker='o', color='orange')
plt.title('Proportion of WNBA Blowout Games (Margin > 20) per Season')
plt.xlabel('Season')
plt.ylabel('Proportion of Blowout Games')
plt.grid(True)
plt.xticks(blowout_counts.index, rotation=45)
plt.tight_layout()
plt.savefig('wnba_blowout_proportions.png')
plt.close()
```

Perhaps we could overlay the graphs with the NBA---maybe a project for another time.
