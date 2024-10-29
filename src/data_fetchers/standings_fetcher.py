import requests
from .api_config import HEADERS, BASE_URL

def fetch_standings(league_id, season):
    url = f"{BASE_URL}/standings"
    querystring = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=querystring)
    return response.json().get('response', [])

def process_standings(standings_data, home_team_id, away_team_id):
    if standings_data:
        standings = standings_data[0]['league']['standings'][0]
        home_standing = next((s for s in standings if s['team']['id'] == home_team_id), None)
        away_standing = next((s for s in standings if s['team']['id'] == away_team_id), None)
        return home_standing, away_standing
    return None, None