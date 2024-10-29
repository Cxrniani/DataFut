from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists

def insert_fixture(id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status):
    conn = None
    try:
        conn = get_db_connection() 
        cursor = conn.cursor()
        
        if not record_exists("SELECT 1 FROM fixtures WHERE id = ?", (id,)):
            cursor.execute('''INSERT INTO fixtures (id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status))
            conn.commit()
    except Exception as e:
        print(f"Erro ao inserir fixture: {e}")  # Tratamento de erro para depuração
    finally:
        if conn:  # Verifica se conn foi inicializada antes de fechar
            conn.close()

from ..utils.db_connection import get_db_connection

def get_all_fixtures():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, home_team, away_team, fixture_date, venue_name, venue_city, referee, status FROM fixtures")
        fixtures = cursor.fetchall()
        return [{'id': row[0], 'home_team': row[1], 'away_team': row[2], 'date': row[3], 'venue_name': row[4], 'venue_city': row[5], 'referee': row[6], 'status': row[7]} for row in fixtures]
    except Exception as e:
        print(f"Erro ao buscar fixtures: {e}")
        return []
    finally:
        if conn:
            conn.close()
