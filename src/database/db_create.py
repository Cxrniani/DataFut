import sqlite3

# Cria/Conecta ao DB
conn = sqlite3.connect('datafut.db') 

# Cria um cursor
cursor = conn.cursor()

# Cria tabelas
cursor.execute('''
    CREATE TABLE fixtures (
        id INT PRIMARY KEY,
        home_team VARCHAR(100),
        away_team VARCHAR(100),
        fixture_date DATE,
        venue_name VARCHAR(255),
        venue_city VARCHAR(255),
        referee VARCHAR(100),
        status VARCHAR(10)
    );''')
cursor.execute('''
    CREATE TABLE scores (
        fixture_id INT PRIMARY KEY,
        halftime_home INT,
        halftime_away INT,
        fulltime_home INT,
        fulltime_away INT,
        extratime_home INT,
        extratime_away INT,
        penalty_home INT,
        penalty_away INT,
        FOREIGN KEY (fixture_id) REFERENCES fixtures(id)
    );''')
cursor.execute('''
    CREATE TABLE standings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fixture_id INT,
        team_name VARCHAR(100),
        position INT,
        FOREIGN KEY (fixture_id) REFERENCES fixtures(id)
    );''')
cursor.execute('''
    CREATE TABLE cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fixture_id INT,
        player_name VARCHAR(100),
        team_name VARCHAR(100),
        card_type VARCHAR(50),
        FOREIGN KEY (fixture_id) REFERENCES fixtures(id)
    );''')
cursor.execute('''
    CREATE TABLE injuries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fixture_id INT,
        player_name VARCHAR(100),
        team_name VARCHAR(100),
        injury_reason VARCHAR(255),
        injury_type VARCHAR(255),
        FOREIGN KEY (fixture_id) REFERENCES fixtures(id)
    );
''')

# Salva e fecha a conexão
conn.commit()
conn.close()
