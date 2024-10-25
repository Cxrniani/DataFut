from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists

def insert_card(fixture_id, player_name, team_name, card_type):
    if not record_exists("SELECT 1 FROM cards WHERE fixture_id = ? AND player_name = ? AND card_type = ?", (fixture_id, player_name, card_type)):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cards (fixture_id, player_name, team_name, card_type) 
            VALUES (?, ?, ?, ?)''', 
            (fixture_id, player_name, team_name, card_type))
        conn.commit()
        conn.close()