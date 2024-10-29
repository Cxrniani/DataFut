import requests
from .api_config import HEADERS, BASE_URL

def fetch_events(fixture_id):
    url = f"{BASE_URL}/fixtures/events"
    querystring = {"fixture": fixture_id}
    response = requests.get(url, headers=HEADERS, params=querystring)
    return response.json().get('response', [])

def process_cards(events):
    cards = []
    for event in events:
        if event['type'] == 'Card':
            cards.append({
                'player_name': event['player']['name'],
                'card_type': event['detail'],
                'team_name': event['team']['name']
            })
    return cards