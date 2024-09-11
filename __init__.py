from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  

# Appel à l'API GitHub pour récupérer les commits
def get_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Route pour extraire les minutes d'une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour afficher le graphique des commits
@app.route('/commits/')
def commits_graph():
    commits_data = get_commits()
    
    # Extraire les minutes des commits
    commit_times = [datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').minute for commit in commits_data]
    
    return render_template('commits.html', commit_times=commit_times)
@app.route('/')
def hello_world():
    return render_template('hello.html')
  #test comit

@app.route('/histogramme/')
def histogramme():
    return render_template('histogramme.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
if __name__ == "__main__":
  app.run(debug=True)
