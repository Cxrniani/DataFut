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
        player_name = injury['player']['name'] if 'player' in injury and 'name' in injury['player'] else 'Jogador não disponível'
        team_name = injury['team']['name'] if 'team' in injury and 'name' in injury['team'] else 'Equipe não disponível'
        injury_reason = injury['player'].get('reason', 'Motivo não disponível')
        injury_type = injury['player'].get('type', 'Tipo não disponível') 

        processed_injuries.append({
            'player_name': player_name,
            'team_name': team_name,
            'injury_reason': injury_reason,
            'injury_type': injury_type
        })
    return processed_injuries
