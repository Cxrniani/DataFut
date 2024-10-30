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
    # Processa e retorna os dados do fixture
    home_team = fixture['teams']['home']['name']
    away_team = fixture['teams']['away']['name']
    fixture_id = fixture['fixture']['id']
    iso_date = fixture['fixture']['date']
    formatted_date = parser.isoparse(iso_date).strftime('%d/%m/%Y')
    fixture_date = parser.isoparse(iso_date).date()

    # Corrigindo a referência ao 'venue' e 'referee' dentro de 'fixture'
    venue_name = fixture['fixture']['venue']['name'] if 'venue' in fixture['fixture'] else 'Estádio não disponível'
    venue_city = fixture['fixture']['venue']['city'] if 'venue' in fixture['fixture'] else 'Cidade não disponível'
    referee = fixture['fixture']['referee'] if 'referee' in fixture['fixture'] else 'Árbitro não disponível'
    
    status = fixture['fixture']['status']['short']

    return {
        'id': fixture_id,
        'home_team': home_team,
        'away_team': away_team,
        'fixture_date': fixture_date,
        'venue_name': venue_name,
        'venue_city': venue_city,
        'referee': referee,
        'status': status
    }
