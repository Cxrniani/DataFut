from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists
from ..utils.db_connection import get_db_connection

def get_cards(fixture_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT player_name, team_name, card_type FROM cards WHERE fixture_id = ?", (fixture_id,))
        cards = cursor.fetchall()
        return [{'player_name': row[0], 'team_name': row[1], 'card_type': row[2]} for row in cards]
    except Exception as e:
        print(f"Erro ao buscar cards: {e}")
        return []
    finally:
        if conn:
            conn.close()

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