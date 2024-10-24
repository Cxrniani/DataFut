from DataFut.src.database.utils.db_connection import get_db_connection

def insert_standing(fixture_id, team_name, position):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO standings (fixture_id, team_name, position) 
        VALUES (?, ?, ?)''', 
        (fixture_id, team_name, position))
    
    conn.commit()
    conn.close()