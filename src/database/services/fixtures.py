from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists

def insert_fixture(id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status):
    if not record_exists("SELECT 1 FROM fixtures WHERE id = ?", (id,)):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO fixtures (id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
            (id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status))
        conn.commit()
        conn.close()
    conn.close()
