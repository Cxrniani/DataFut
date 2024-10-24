import requests
from datetime import datetime, timedelta
from dateutil import parser
from dotenv import load_dotenv
import os

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
    print(f"Partida: {home_team} vs {away_team}")
    
    # Data do jogo
    iso_date = fixture['fixture']['date']
    formatted_date = parser.isoparse(iso_date).strftime('%d/%m/%Y')
    print(f"Data do Jogo: {formatted_date}")

    # Classificação dos times
    standings_url = "https://api-football-v1.p.rapidapi.com/v3/standings"
    standings_query = {
        "league": "2", 
        "season": "2024"
    }
    standings_response = requests.get(standings_url, headers=headers, params=standings_query)
    standings_data = standings_response.json()
    print("Classificação dos times:")
    
    if standings_data.get('response'):
        for standing in standings_data['response'][0]['league']['standings'][0]:
            if standing['team']['id'] == fixture['teams']['home']['id']:
                print(f"{fixture['teams']['home']['name']} está na posição {standing['rank']}")
            if standing['team']['id'] == fixture['teams']['away']['id']:
                print(f"{fixture['teams']['away']['name']} está na posição {standing['rank']}")

    # Informações do estádio e árbitro
    venue = fixture.get('venue', {})
    venue_name = venue.get('name', 'Estádio não disponível')
    venue_city = venue.get('city', 'Cidade não disponível')
    referee = fixture.get('referee', 'Árbitro não disponível')
    
    print(f"Estádio: {venue_name}, Cidade: {venue_city}")
    print(f"Árbitro: {referee}")

    # Verificar o status da partida
    status = fixture['fixture']['status']['short']
    if status != 'NS':  # Verificar se o jogo já começou (diferente de 'Not Started')
        # Placar
        home_goals = fixture['goals'].get('home', 'N/A')
        away_goals = fixture['goals'].get('away', 'N/A')
        print(f"Placar: {home_goals} - {away_goals}")
    
        # Informações detalhadas do placar
        halftime_score = fixture['score']['halftime']
        fulltime_score = fixture['score']['fulltime']
        extratime_score = fixture['score']['extratime']
        penalty_score = fixture['score']['penalty']
        
        print(f"Placar no intervalo: {halftime_score['home']} - {halftime_score['away']}")
        print(f"Placar final: {fulltime_score['home']} - {fulltime_score['away']}")
        
        if extratime_score['home'] is not None and extratime_score['away'] is not None:
            print(f"Placar no tempo extra: {extratime_score['home']} - {extratime_score['away']}")
        
        if penalty_score['home'] is not None and penalty_score['away'] is not None:
            print(f"Resultado nos pênaltis: {penalty_score['home']} - {penalty_score['away']}")

        # Cartões - acessar eventos para verificar cartões
        fixture_id = fixture['fixture']['id']
        url_events = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/events?fixture={fixture_id}"
        events_response = requests.get(url_events, headers=headers)
        events_data = events_response.json()

        print("Cartões:")
        if events_data.get('response'):
            for event in events_data['response']:
                if event['type'] == 'Card':
                    player_name = event['player']['name']
                    card_type = event['detail']  # Yellow Card / Red Card
                    team_name = event['team']['name']
                    print(f"{team_name} - {player_name} recebeu um {card_type}")
        
        # Lesões - acessar o endpoint de lesões
        injuries_url = "https://api-football-v1.p.rapidapi.com/v3/injuries"
        injuries_query = {
            "fixture": fixture_id  # Usando o ID da partida
        }
        injuries_response = requests.get(injuries_url, headers=headers, params=injuries_query)
        injuries_data = injuries_response.json()

        print("Lesões:")
        if injuries_data.get('response'):
            for injury in injuries_data['response']:
                player_name = injury['player']['name']
                team_name = injury['team']['name']
                injury_reason = injury.get('reason', 'Motivo não disponível')
                injury_type = injury.get('type', 'Tipo não disponível')
                print(f"{team_name} - {player_name} sofreu uma lesão: {injury_reason} (Tipo: {injury_type})")
        else:
            print("Nenhuma lesão registrada.")
    else:
        print("O jogo ainda não começou.")

    print('-' * 40)
