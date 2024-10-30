from flask import Flask, render_template, jsonify
from database.services.fixtures import get_all_fixtures
from database.services.scores import get_score
from database.services.standings import get_standings
from database.services.cards import get_cards
from database.services.injuries import get_injuries

app = Flask(__name__)

@app.route('/')
def index():
    fixtures = get_all_fixtures()
    return render_template('index.html', fixtures=fixtures)

@app.route('/fixture/<int:fixture_id>')
def fixture_details(fixture_id):
    score = get_score(fixture_id)
    fixtures = get_all_fixtures()
    
    fixture = next((f for f in fixtures if f['id'] == fixture_id), None)

    cards = get_cards(fixture_id)
    injuries = get_injuries(fixture_id)

    return jsonify({
        'score': score,
        'fixture': fixture,
        'cards': cards,
        'injuries': injuries
    })

if __name__ == '__main__':
    app.run(debug=True)