---
title: "As Promised---Skubal and Skenes Career K Projections"
date: 2025-06-19 17:50:00
draft: false
toc: false
tags:
  - python
  - data parsing
  - data extraction
  - data analysis
  - MLB Baseball
  - MLB Pitchers
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
  - Patrick Skenes
  - Tarik Skubal
  - Skenes
  - Skubal
  - Pittsburgh Pirates
  - Pirates
  - Detroit Tigers
  - Tigers
---

As in my [previous post](https://kspicer80.github.io/posts/2025-06-17-skubal-k-projections/) I promised to look at both Skenes and Skubal and their projected trajectories towards 3000 career strikeouts. If we're being honest, this benchmark is far from easy to achieve, only 19 pitchers in the history of baseball have done it before:

| Pitcher          | Strikeouts |
|------------------|-----------:|
| Nolan Ryan       |      5,714 |
| Randy Johnson    |      4,875 |
| Roger Clemens    |      4,672 |
| Steve Carlton    |      4,136 |
| Bert Blyleven    |      3,701 |
| Tom Seaver       |      3,640 |
| Don Sutton       |      3,574 |
| Gaylord Perry    |      3,534 |
| Walter Johnson   |      3,509 |
| Greg Maddux      |      3,371 |
| Phil Niekro      |      3,342 |
| Ferguson Jenkins |      3,192 |
| Pedro Martinez   |      3,154 |
| Bob Gibson       |      3,117 |
| Curt Schilling   |      3,116 |
| CC Sabathia      |      3,093 |
| John Smoltz      |      3,084 |
| Justin Verlander |      3,041 |
| Max Scherzer     |      3,000 |

(IIRC, CC Sabathia and Justin Verlander are also on this list too.) So, just making clear how hard this is to manage, I'd like to continue our analysis. I was also thinking about my initial [MLB post](https://kspicer80.github.io/posts/2025-06-15-skenes-vs-kershaw-career-strikeouts/) (where we were looking at Skenes and Kershaw). I can imagine a reader wondering how we determined what an "optimistic" versus "pessimistic" trajectory for Skenes ultimately is ... I figured I would answer that in my writeup here of our Skenes vs. Skubal's career K potential/trajectory. So let's go producing a similar side-by-side comparison for these two but with the initial steps not being left out/omitted.

So, the first thing is getting an average strikeout rate for this two pitchers. We can get their full stats from the same sources as previous. Those stats look like this:

| NAME          | SO  | G   | W   | L   | W%    | GS  | ERA  | CG | SHO | SV | IP    | H   | ER  | R   | HR  | BB  | HBP | GF | IBB | TBF  | WP | K/9  | BB/9 | K/BB | HR/9 | K%   | BB%  | WHIP | BABIP | RA   | ERA- | FIP  | FIP- | H/9  | PRAA |
| :------------ | :-- | :-- | :-- | :-- | :---- | :-- | :--- | :-- | :-- | :-- | :---- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :--- | :-- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---- | :--- | :--- | :--- | :--- | :--- | :--- |
| Tarik Skubal  | 759 | 120 | 48  | 33  | .593  | 117 | 3.18 | 1  | 1  | 0  | 661.2 | 537 | 234 | 252 | 78  | 148 | 24  | 1  | 0  | 2647 | 9  | 10.32 | 2.01 | 5.13 | 1.06 | 28.7 | 5.6  | 1.04 | .280  | 3.43 | 77   | 3.17 | 77   | 7.30 | 68.6 |
| Paul Skenes   | 267 | 38  | 15  | 9   | .625  | 38  | 1.89 | 1  | 0  | 0  | 229.0 | 154 | 48  | 53  | 15  | 54  | 8   | 0  | 0  | 879  | 3  | 10.49 | 2.12 | 4.94 | 0.59 | 30.4 | 6.1  | 0.91 | .260  | 2.08 | 45   | 2.45 | 61   | 6.05 | 40.1 |

If we want a simplified version:

| Player       | Strikeouts | Starts | Average K/Start |
|--------------|------------|--------|-----------------|
| Tarik Skubal | 759        | 117    | 6.05            |
| Paul Skenes  | 267        | 38     | 7.03            |

So, Skubal has a slightly lower average strikeouts per start than Skenes does so far. Given this we can use this information to derive an optimistic score (over their average) or pessimistic (assuming they largely perform under their average.)

That gives us the following visualization:

![skubal_vs_skenes_projections](/images/imgforblogposts/post_43/skubal_skenes_comparison.png)

As always, code is provided below:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import time
import logging
import argparse
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to scrape Tarik Skubal's stats from FanGraphs or ESPN with retries
def get_skubal_stats(max_retries=3, delay=2):
    url_fangraphs = "https://www.fangraphs.com/players/tarik-skubal/18846/stats?position=P"
    url_espn = "http://www.espn.com/mlb/player/stats/_/id/33794/tarik-skubal"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.fangraphs.com/'
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url_fangraphs, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', id='PitchingStandard')
            if not table:
                raise ValueError("Pitching stats table not found")
            career_row = table.find_all('tr', class_=['rgRow', 'rgAltRow'])[-1]
            cells = career_row.find_all('td')
            strikeouts = int(cells[13].text.strip())
            games_started = int(cells[5].text.strip())
            logging.info(f"Successfully scraped stats from FanGraphs: {strikeouts} strikeouts, {games_started} starts")
            return strikeouts, games_started
        except Exception as e:
            logging.warning(f"FanGraphs attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    headers['Referer'] = 'http://www.espn.com/'
    for attempt in range(max_retries):
        try:
            response = requests.get(url_espn, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_table = soup.find('table', class_='Table')
            if not stats_table:
                raise ValueError("Stats table not found on ESPN")
            career_row = stats_table.find('tr', class_='Table__TR--lg')
            cells = career_row.find_all('td')
            strikeouts = int(cells[13].text.strip())
            games_started = int(cells[3].text.strip())
            logging.info(f"Successfully scraped stats from ESPN: {strikeouts} strikeouts, {games_started} starts")
            return strikeouts, games_started
        except Exception as e:
            logging.warning(f"ESPN attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    logging.error(f"Scraping failed after {max_retries} attempts on both sites. Using fallback data.")
    logging.warning("Consider using --manual or checking https://www.fangraphs.com/players/tarik-skubal/18846/stats?position=P or http://www.espn.com/mlb/player/stats/_/id/33794/tarik-skubal")
    return 759, 117  # Updated fallback: Full career stats as of June 18, 2025

# Function to scrape Paul Skenes' stats from FanGraphs or ESPN with retries
def get_skenes_stats(max_retries=3, delay=2):
    url_fangraphs = "https://www.fangraphs.com/players/paul-skenes/24615/stats?position=P"
    url_espn = "http://www.espn.com/mlb/player/stats/_/id/42922/paul-skenes"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.fangraphs.com/'
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url_fangraphs, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', id='PitchingStandard')
            if not table:
                raise ValueError("Pitching stats table not found")
            career_row = table.find_all('tr', class_=['rgRow', 'rgAltRow'])[-1]
            cells = career_row.find_all('td')
            strikeouts = int(cells[13].text.strip())
            games_started = int(cells[5].text.strip())
            logging.info(f"Successfully scraped stats from FanGraphs: {strikeouts} strikeouts, {games_started} starts")
            return strikeouts, games_started
        except Exception as e:
            logging.warning(f"FanGraphs attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    headers['Referer'] = 'http://www.espn.com/'
    for attempt in range(max_retries):
        try:
            response = requests.get(url_espn, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_table = soup.find('table', class_='Table')
            if not stats_table:
                raise ValueError("Stats table not found on ESPN")
            career_row = stats_table.find('tr', class_='Table__TR--lg')
            cells = career_row.find_all('td')
            strikeouts = int(cells[13].text.strip())
            games_started = int(cells[3].text.strip())
            logging.info(f"Successfully scraped stats from ESPN: {strikeouts} strikeouts, {games_started} starts")
            return strikeouts, games_started
        except Exception as e:
            logging.warning(f"ESPN attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    logging.error(f"Scraping failed after {max_retries} attempts on both sites. Using fallback data.")
    logging.warning("Consider using --manual or checking https://www.fangraphs.com/players/paul-skenes/24615/stats?position=P or http://www.espn.com/mlb/player/stats/_/id/42922/paul-skenes")
    return 267, 38  # Fallback: 267 strikeouts, 38 starts (as of June 17, 2025)

# Function to get stats via manual input
def get_manual_stats(player):
    try:
        strikeouts = int(input(f"Enter {player}'s current strikeouts: "))
        starts = int(input(f"Enter {player}'s current starts: "))
        logging.info(f"Manually entered stats for {player}: {strikeouts} strikeouts, {starts} starts")
        return strikeouts, starts
    except ValueError:
        logging.error(f"Invalid input for {player}. Using fallback data.")
        return 759, 117 if player == "Tarik Skubal" else 267, 38

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Compare Tarik Skubal and Paul Skenes career strikeouts")
parser.add_argument('--manual', action='store_true', help='Manually input stats instead of scraping')
parser.add_argument('--no-scrape', action='store_true', help='Skip scraping and use fallback data')
parser.add_argument('--years', type=int, default=15, help='Number of projection years (default: 15)')
args = parser.parse_args()

# Get current stats
if args.manual:
    skubal_strikeouts, skubal_starts = get_manual_stats("Tarik Skubal")
    skenes_strikeouts, skenes_starts = get_manual_stats("Paul Skenes")
elif args.no_scrape:
    skubal_strikeouts, skubal_starts = 759, 117
    skenes_strikeouts, skenes_starts = 267, 38
    logging.info("Skipping scraping as per --no-scrape. Using fallback data: 759 strikeouts, 117 starts for Skubal; 267 strikeouts, 38 starts for Skenes")
else:
    skubal_strikeouts, skubal_starts = get_skubal_stats()
    skenes_strikeouts, skenes_starts = get_skenes_stats()

skubal_age = 23  # Updated to MLB debut age (September 2020)
skenes_age = 23  # As of June 17, 2025

# Assumptions
skubal_rates = {'optimistic': 6.5, 'average': 6.0, 'pessimistic': 5.5}
skenes_rates = {'optimistic': 7.5, 'average': 7.0, 'pessimistic': 6.5}
starts_per_season = 27  # Average of 25-30 starts
career_years = np.arange(0, args.years)
skubal_seasons = skubal_age + career_years
skenes_seasons = skenes_age + career_years
logging.info(f"Projecting for {len(career_years)} years, Skubal ages {skubal_age} to {skubal_seasons[-1]}, Skenes ages {skenes_age} to {skenes_seasons[-1]}")

# Function to project strikeouts
def project_strikeouts(strikeout_rate, starts_per_year, years, current_k):
    cumulative_k = [current_k]
    for i in range(1, len(years)):
        season_k = strikeout_rate * starts_per_year
        cumulative_k.append(cumulative_k[-1] + season_k)
    return cumulative_k

# Calculate projections
skubal_projections = {scenario: project_strikeouts(rate, starts_per_season, career_years, skubal_strikeouts) for scenario, rate in skubal_rates.items()}
skenes_projections = {scenario: project_strikeouts(rate, starts_per_season, career_years, skenes_strikeouts) for scenario, rate in skenes_rates.items()}

# Create DataFrame for visualization
df_skubal = pd.DataFrame({'age': skubal_seasons, **{f'skubal_{scenario}': proj for scenario, proj in skubal_projections.items()}})
df_skenes = pd.DataFrame({'age': skenes_seasons, **{f'skenes_{scenario}': proj for scenario, proj in skenes_projections.items()}})

# Save projections to CSV
csv_path = "/Users/spicy.kev/Documents/github/kspicer80.github.io/static/images/imgforblogposts/post_43/skubal_skenes_projections.csv"
try:
    pd.concat([df_skubal, df_skenes], axis=1).to_csv(csv_path, index=False)
    logging.info(f"Projections saved to {csv_path}")
except Exception as e:
    logging.error(f"Failed to save CSV to {csv_path}: {e}")

# Find years to reach 3000 strikeouts
target_k = 3000
reach_3000 = {'skubal': {}, 'skenes': {}}
for player, projections in [('skubal', skubal_projections), ('skenes', skenes_projections)]:
    seasons = skubal_seasons if player == 'skubal' else skenes_seasons
    for scenario in projections:
        years_to_3000 = np.where(np.array(projections[scenario]) >= target_k)[0]
        if len(years_to_3000) > 0:
            year_idx = years_to_3000[0]
            reach_3000[player][scenario] = {'age': seasons[year_idx], 'strikeouts': projections[scenario][year_idx]}
        else:
            reach_3000[player][scenario] = {'age': None, 'strikeouts': projections[scenario][-1]}

# Plotting with debugging
print("Skubal DataFrame:\n", df_skubal)
print("Skenes DataFrame:\n", df_skenes)

plt.figure(figsize=(12, 8))
for scenario in skubal_projections:
    plt.plot(df_skubal['age'], df_skubal[f'skubal_{scenario}'], label=f'Skubal {scenario.capitalize()} ({skubal_rates[scenario]} K/start)', linestyle='--', color=f'C{list(skubal_rates.keys()).index(scenario)}')
for scenario in skenes_projections:
    plt.plot(df_skenes['age'], df_skenes[f'skenes_{scenario}'], label=f'Skenes {scenario.capitalize()} ({skenes_rates[scenario]} K/start)', linestyle='-', color=f'C{list(skenes_rates.keys()).index(scenario)+3}')
plt.axhline(y=3000, color='r', linestyle='--', label='3000 Strikeouts')
plt.xlabel('Age')
plt.ylabel('Cumulative Strikeouts')
plt.title('Skubal vs. Skenes Career Strikeout Projection')
plt.legend()
plt.grid(True)

plt.tight_layout()

# Save plot with error handling
save_path = "/Users/spicy.kev/Documents/github/kspicer80.github.io/static/images/imgforblogposts/post_43/skubal_skenes_comparison.png"
try:
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    logging.info(f"Plot saved to {save_path}")
except Exception as e:
    print(f"Error saving plot: {e}")
    logging.error(f"Failed to save plot to {save_path}: {e}")

plt.show()

# Print results
print(f"Tarik Skubal Current Stats: {skubal_strikeouts} strikeouts in {skubal_starts} starts")
print(f"Paul Skenes Current Stats: {skenes_strikeouts} strikeouts in {skenes_starts} starts")
print(f"Projecting for {len(career_years)} years (Skubal ages {skubal_age} to {skubal_seasons[-1]}, Skenes ages {skenes_age} to {skenes_seasons[-1]})")
print("Career Strikeout Projections:")
for player in ['Skubal', 'Skenes']:
    projections = skubal_projections if player == 'Skubal' else skenes_projections
    for scenario, info in reach_3000[player.lower()].items():
        if info['age'] is not None:
            print(f"{player} {scenario.capitalize()} Scenario: Reaches 3000 strikeouts at age {info['age']} with {int(info['strikeouts'])} strikeouts")
        else:
            print(f"{player} {scenario.capitalize()} Scenario: Ends at {int(info['strikeouts'])} strikeouts by age {skubal_seasons[-1] if player == 'Skubal' else skenes_seasons[-1]}")
```





