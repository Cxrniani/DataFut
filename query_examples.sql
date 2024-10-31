-- Listar todos os jogos (fixtures) com informações básicas
SELECT 
    id AS fixture_id,
    home_team,
    away_team,
    fixture_date,
    venue_name,
    venue_city,
    referee,
    status
FROM 
    fixtures
ORDER BY 
    fixture_date;

-- Obter detalhes de um jogo específico
SELECT 
    f.id AS fixture_id,
    f.home_team,
    f.away_team,
    f.fixture_date,
    f.venue_name,
    f.venue_city,
    f.referee,
    f.status,
    s.halftime_home,
    s.halftime_away,
    s.fulltime_home,
    s.fulltime_away,
    s.extratime_home,
    s.extratime_away,
    s.penalty_home,
    s.penalty_away
FROM 
    fixtures f
JOIN 
    scores s ON f.id = s.fixture_id
WHERE 
    f.id = ?;

-- Listar todos os cartões recebidos em um jogo
SELECT 
    c.player_name,
    c.team_name,
    c.card_type
FROM 
    cards c
WHERE 
    c.fixture_id = ?;

-- Listar todas as lesões ocorridas em um jogo
SELECT 
    i.player_name,
    i.team_name,
    i.injury_reason,
    i.injury_type
FROM 
    injuries i
WHERE 
    i.fixture_id = ?;

-- Listar todos os times e suas posições em um jogo
SELECT 
    t.team_name,
    t.position
FROM 
    teams t
WHERE 
    t.fixture_id = ?;

-- Obter a lista de jogos com resultados completos (incluindo tempos extras e pênaltis, se houver)
SELECT 
    f.id AS fixture_id,
    f.home_team,
    f.away_team,
    s.fulltime_home,
    s.fulltime_away,
    s.extratime_home,
    s.extratime_away,
    s.penalty_home,
    s.penalty_away
FROM 
    fixtures f
JOIN 
    scores s ON f.id = s.fixture_id
WHERE 
    f.status = 'FT';

-- Obter estatísticas resumidas de cartões por time
SELECT 
    c.team_name,
    COUNT(*) AS total_cards
FROM 
    cards c
JOIN 
    fixtures f ON c.fixture_id = f.id
GROUP BY 
    c.team_name
ORDER BY 
    total_cards DESC;

-- Obter estatísticas de lesões por time
SELECT 
    i.team_name,
    COUNT(*) AS total_injuries
FROM 
    injuries i
JOIN 
    fixtures f ON i.fixture_id = f.id
GROUP BY 
    i.team_name
ORDER BY 
    total_injuries DESC;
