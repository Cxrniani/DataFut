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

