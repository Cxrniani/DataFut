from .db_connection import get_db_connection

def record_exists(query, params):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Mudar ? para %s no MySQL
        query = query.replace('?', '%s')
        cursor.execute(query, params)
        return cursor.fetchone() is not None
