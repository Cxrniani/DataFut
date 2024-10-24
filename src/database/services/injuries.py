from DataFut.src.database.utils.db_connection import get_db_connection


def insert_injury(fixture_id, player_name, team_name, injury_reason, injury_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO injuries (fixture_id, player_name, team_name, injury_reason, injury_type) 
        VALUES (?, ?, ?, ?, ?)''', 
        (fixture_id, player_name, team_name, injury_reason, injury_type))
    
    conn.commit()
    conn.close()