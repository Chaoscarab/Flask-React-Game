import os
from flask import Flask, send_from_directory, json, request, render_template
from flaskwebgui import FlaskUI # import FlaskUI
from modules.get_enemies import get_enemies
from modules.take_turn import take_turn

app = Flask(__name__, static_folder='static/')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
@app.route('/json', methods=['GET', 'POST'])
def send_json():
    if request.method == 'POST':
        dataJson = request.get_json()
        print(dataJson['player'])
        if dataJson['task'] == 'getEnemies':
            data = {
                "array": get_enemies(dataJson["player"]['level'])
            }
            return json.dumps(data)
        if dataJson['task'] == 'turn':
            data = take_turn(dataJson)
            return json.dumps(data)


       

        
    if request.method == 'GET':
        data = {
            'hp': 20,
            'moves': [{ 'name': 'shoot \'n scoot', 'description': 'hits all enemies with a mid attack, consumes 2 ammo' }, {"name": 'punch',  'description': 'hits one enemy for a medium amount'},{"name": 'dodge',  'description': 'dodge the next attack'}, {"name":'reload',  'description': 'replenish ammo'}],
            'ammo': 6,
            'status': [],
            'xp': 0,
            'level': 1,
            'logs': ['GAME START'],
            'name': 'player'
        }
        return json.dumps(data)
    


if __name__ == "__main__":
# If you are debugging you can do that in the browser:
  # If you want to view the flaskwebgui window:
    FlaskUI(app=app, server="flask", width="800", height="500", port=5000).run()

#command to package app.
#python -m PyInstaller -w -F --add-data "templates;templates" --add-data "static;static" main.py

