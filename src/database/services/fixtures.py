from DataFut.src.database.utils.db_connection import get_db_connection

def insert_fixture(id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO fixtures (id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
        (id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status))
    
    conn.commit()
    conn.close()
