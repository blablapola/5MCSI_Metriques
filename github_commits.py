import requests
from collections import defaultdict
from datetime import datetime

def get_commits():
    url = "https://api.github.com/repos/blablapola/5MCSI_Metriques/commits"
    response = requests.get(url)

    if response.status_code == 200:
        commits = response.json()
        commit_per_minute = defaultdict(int)

        for commit in commits:
            commit_date_str = commit['commit']['author']['date']
            commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
            commit_minute = commit_date.strftime("%Y-%m-%d %H:%M")
            commit_per_minute[commit_minute] += 1

        # Préparer les données pour le graphique
        chart_data = [["Minute", "Nombre de commits"]]
        for minute, count in sorted(commit_per_minute.items()):
            chart_data.append([minute, count])

        return chart_data
    else:
        return [["Minute", "Nombre de commits"]]
