import requests
from datetime import datetime, timedelta
from dateutil import parser
from .api_config import HEADERS, BASE_URL

def fetch_fixtures(league_id, season):
    thisMonth = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    url = f"{BASE_URL}/fixtures"
    querystring = {
        "from": one_week_ago,
        "to": thisMonth,
        "league": league_id,
        "season": season,
    }

    response = requests.get(url, headers=HEADERS, params=querystring)
    return response.json().get('response', [])

def process_fixture(fixture):
    # Process and return fixture data
    home_team = fixture['teams']['home']['name']
    away_team = fixture['teams']['away']['name']
    fixture_id = fixture['fixture']['id']
    iso_date = fixture['fixture']['date']
    formatted_date = parser.isoparse(iso_date).strftime('%d/%m/%Y')
    venue_name = fixture.get('venue', {}).get('name', 'Estádio não disponível')
    venue_city = fixture.get('venue', {}).get('city', 'Cidade não disponível')
    referee = fixture.get('referee', 'Árbitro não disponível')
    status = fixture['fixture']['status']['short']

    return {
        'id': fixture_id,
        'home_team': home_team,
        'away_team': away_team,
        'fixture_date': formatted_date,
        'venue_name': venue_name,
        'venue_city': venue_city,
        'referee': referee,
        'status': status
    }