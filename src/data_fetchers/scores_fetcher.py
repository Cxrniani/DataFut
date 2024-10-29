def get_score(score_dict, key):
    return score_dict.get(key, {}).get('home', 0), score_dict.get(key, {}).get('away', 0)

def process_scores(fixture):
    scores = fixture['score']
    
    halftime_home, halftime_away = get_score(scores, 'halftime')
    fulltime_home, fulltime_away = get_score(scores, 'fulltime')
    extratime_home, extratime_away = get_score(scores, 'extratime')
    penalty_home, penalty_away = get_score(scores, 'penalty')
    
    return {
        'halftime_home': halftime_home,
        'halftime_away': halftime_away,
        'fulltime_home': fulltime_home,
        'fulltime_away': fulltime_away,
        'extratime_home': extratime_home,
        'extratime_away': extratime_away,
        'penalty_home': penalty_home,
        'penalty_away': penalty_away
    }