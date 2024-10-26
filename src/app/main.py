import requests
from datetime import datetime, timedelta
from dateutil import parser
from dotenv import load_dotenv
import os
from database.services.fixtures import insert_fixture
from database.services.scores import insert_score
from database.services.standings import insert_standing
from database.services.cards import insert_card
from database.services.injuries import insert_injury

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Definindo o intervalo de tempo: uma semana atrás até hoje
thisMonth = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

url_fixtures = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
querystring = {
    "from": one_week_ago,  # Data inicial
    "to": thisMonth,  # Data final
    "league": "2",  # ID da UEFA Champions
    "season": "2024",  # Temporada
}

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

response = requests.get(url_fixtures, headers=headers, params=querystring)
data = response.json()

for fixture in data.get('response', []):
    # Informações básicas da partida
    home_team = fixture['teams']['home']['name']
    away_team = fixture['teams']['away']['name']
    fixture_id = fixture['fixture']['id']
    print(f"Partida: {home_team} vs {away_team}")
    
    # Data do jogo
    iso_date = fixture['fixture']['date']
    formatted_date = parser.isoparse(iso_date).strftime('%d/%m/%Y')
    print(f"Data do Jogo: {formatted_date}")

    # Inserir dados na tabela fixtures
    venue_name = fixture.get('venue', {}).get('name', 'Estádio não disponível')
    venue_city = fixture.get('venue', {}).get('city', 'Cidade não disponível')
    referee = fixture.get('referee', 'Árbitro não disponível')
    status = fixture['fixture']['status']['short']
    
    if insert_fixture(fixture_id, home_team, away_team, formatted_date, venue_name, venue_city, referee, status):
        print(f"Fixture inserido: {home_team} vs {away_team} em {venue_name}, {venue_city}, árbitro: {referee}")
    else:
        print(f"Fixture já existente: {home_team} vs {away_team}")

    # Classificação dos times
    standings_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
    standings_query = {
        "league": "2", 
        "season": "2024"
    }
    standings_response = requests.get(standings_url, headers=headers, params=standings_query)
    standings_data = standings_response.json()
    
    if standings_data.get('response'):
        for standing in standings_data['response'][0]['league']['standings'][0]:
            if standing['team']['id'] == fixture['teams']['home']['id']:
                if insert_standing(fixture_id, home_team, standing['rank']):
                    print(f"Classificação inserida: {home_team} na posição {standing['rank']}")
            if standing['team']['id'] == fixture['teams']['away']['id']:
                if insert_standing(fixture_id, away_team, standing['rank']):
                    print(f"Classificação inserida: {away_team} na posição {standing['rank']}")

    # Verificar o status da partida
    if status != 'NS':  # Verificar se o jogo já começou (diferente de 'Not Started')
        # Placar
        halftime_score = fixture['score']['halftime']
        fulltime_score = fixture['score']['fulltime']
        extratime_score = fixture['score']['extratime']
        penalty_score = fixture['score']['penalty']
        
        if insert_score(fixture_id, 
                        halftime_score['home'], halftime_score['away'],
                        fulltime_score['home'], fulltime_score['away'],
                        extratime_score['home'], extratime_score['away'],
                        penalty_score['home'], penalty_score['away']):
            print(f"Placar inserido para o fixture {fixture_id}:")
            print(f"  Intervalo: {halftime_score['home']} - {halftime_score['away']}")
            print(f"  Tempo Completo: {fulltime_score['home']} - {fulltime_score['away']}")
            print(f"  Tempo Extra: {extratime_score['home']} - {extratime_score['away']}")
            print(f"  Pênaltis: {penalty_score['home']} - {penalty_score['away']}")

        # Cartões - acessar eventos para verificar cartões
        url_events = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/events?fixture={fixture_id}"
        events_response = requests.get(url_events, headers=headers)
        events_data = events_response.json()

        if events_data.get('response'):
            for event in events_data['response']:
                if event['type'] == 'Card':
                    player_name = event['player']['name']
                    card_type = event['detail']  # Yellow Card / Red Card
                    team_name = event['team']['name']
                    if insert_card(fixture_id, player_name, team_name, card_type):
                        print(f"Cartão inserido: {team_name} - {player_name} ({card_type})")

        # Lesões - acessar o endpoint de lesões
        injuries_url = "https://api-football-v1.p.rapidapi.com/v3/injuries"
        injuries_query = {
            "fixture": fixture_id  # Usando o ID da partida
        }
        injuries_response = requests.get(injuries_url, headers=headers, params=injuries_query)
        injuries_data = injuries_response.json()

        if injuries_data.get('response'):
            for injury in injuries_data['response']:
                player_name = injury['player']['name']
                team_name = injury['team']['name']
                injury_reason = injury.get('reason', 'Motivo não disponível')
                injury_type = injury.get('type', 'Tipo não disponível')
                if insert_injury(fixture_id, player_name, team_name, injury_reason, injury_type):
                    print(f"Lesão inserida: {team_name} - {player_name}, Motivo: {injury_reason}, Tipo: {injury_type}")
    else:
        print(f"O jogo {fixture_id} ainda não começou.")

    print('-' * 40)
