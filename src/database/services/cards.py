from DataFut.src.database.utils.db_connection import get_db_connection

def insert_card(fixture_id, player_name, team_name, card_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO cards (fixture_id, player_name, team_name, card_type) 
        VALUES (?, ?, ?, ?)''', 
        (fixture_id, player_name, team_name, card_type))
    
    conn.commit()
    conn.close()