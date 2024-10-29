import requests
from .api_config import HEADERS, BASE_URL

def fetch_injuries(fixture_id):
    url = f"{BASE_URL}/injuries"
    querystring = {"fixture": fixture_id}
    response = requests.get(url, headers=HEADERS, params=querystring)
    return response.json().get('response', [])

def process_injuries(injuries):
    processed_injuries = []
    for injury in injuries:
        processed_injuries.append({
            'player_name': injury['player']['name'],
            'team_name': injury['team']['name'],
            'injury_reason': injury.get('reason', 'Motivo não disponível'),
            'injury_type': injury.get('type', 'Tipo não disponível')
        })
    return processed_injuries