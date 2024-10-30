from data_fetchers.fixture_fetcher import fetch_fixtures, process_fixture
from data_fetchers.standings_fetcher import fetch_standings, process_standings
from data_fetchers.events_fetcher import fetch_events, process_cards
from data_fetchers.injuries_fetcher import fetch_injuries, process_injuries

from database.services.fixtures import insert_fixture, fixture_exists
from database.services.scores import insert_score
from database.services.standings import insert_standing
from database.services.cards import insert_card
from database.services.injuries import insert_injury

LEAGUE_ID = "2"  # ID da UEFA Champions
SEASON = "2024"

fixtures = fetch_fixtures(LEAGUE_ID, SEASON)

def lambda_handler(event, context):
    for fixture in fixtures:
        fixture_data = process_fixture(fixture)

        if not fixture_exists(fixture_data['id']):
            insert_fixture(**fixture_data)

        if fixture_exists(fixture_data['id']):
            standings_data = fetch_standings(LEAGUE_ID, SEASON)
            home_standing, away_standing = process_standings(standings_data, fixture['teams']['home']['id'], fixture['teams']['away']['id'])

            if home_standing:
                insert_standing(fixture_data['id'], fixture_data['home_team'], home_standing['rank'])

            if away_standing:
                insert_standing(fixture_data['id'], fixture_data['away_team'], away_standing['rank'])

            if fixture_data['status'] != 'NS':
                scores = fixture['score']
                insert_score(
                    fixture_data['id'], 
                    scores['halftime']['home'], scores['halftime']['away'],
                    scores['fulltime']['home'], scores['fulltime']['away'],
                    scores['extratime']['home'], scores['extratime']['away'],
                    scores['penalty']['home'], scores['penalty']['away']
                )

                events = fetch_events(fixture_data['id'])
                cards = process_cards(events)
                for card in cards:
                    insert_card(fixture_data['id'], card['player_name'], card['team_name'], card['card_type'])

                injuries = fetch_injuries(fixture_data['id'])
                processed_injuries = process_injuries(injuries)
                for injury in processed_injuries:
                    insert_injury(
                        fixture_data['id'], injury['player_name'], injury['team_name'], 
                        injury['injury_reason'], injury['injury_type']
                    )
