import json
import requests
from flask import Flask
from flask_cors import CORS
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    '''Default route that return all data.'''

    # Requests and Soups
    req = requests.get('https://www.mg.superesportes.com.br/futebol/atletico-mg/')
    res_g4 = requests.get('https://www.mg.superesportes.com.br/campeonatos/2021/brasileirao/serie-a/')
    soup = BeautifulSoup(req.content, 'html.parser')
    soup_g4 = BeautifulSoup(res_g4.content, 'html.parser')

    # Response
    response = {'proximos': {'jogos': []}, 'ultimos': {'jogos': []}, 'tabela': []}

    # Titles
    titles = soup.find_all('span', {'class': 'd-flex d-flex__align-end mb-10 f-22 green-01 txt-bold personal-font'})

    response['proximos']['title'] = titles[0].text
    response['ultimos']['title'] = titles[1].text

    # All games
    games = soup.find_all('div', {'class': 'card-game'})

    for gm in games:
        g = {}

        teams = gm.find_all('span', {'class': 'd-flex d-flex__align-baseline'})
        x = gm.find('span', {'class': 'f-14 pl-10 pr-10'}).text
        label = gm.find('h4', {'class': 'f-12 gray-50'}).text
        
        team1_name = teams[0].find('label', {'class': 'f-14 gray-42 txt-uppercase pl-10'}).text
        team1_img = teams[0].find('img', {'class': 'shield shield--small'})['src']
        
        if gm.find('label', {'class': 'd-flex gray-42 f-16 txt-uppercase pl-10'}) != None:
            result_team1 = gm.find('label', {'class': 'd-flex gray-42 f-16 txt-uppercase pl-10'}).text
        
        else:
            result_team1 = ''

        team2_name = teams[1].find('label', {'class': 'f-14 gray-42 txt-uppercase pr-10'}).text
        team2_img = teams[1].find('img', {'class': 'shield shield--small'})['src']
        
        if gm.find('label', {'class': 'd-flex gray-42 f-16 txt-uppercase pr-10'}) != None:
            result_team2 = gm.find('label', {'class': 'd-flex gray-42 f-16 txt-uppercase pr-10'}).text
        
        else:
            result_team2 = ''

        g['time1_name'] = team1_name
        g['time1_img'] = team1_img
        g['resultado_time1'] = result_team1

        g['x'] = x
        g['label'] = label

        g['time2_name'] = team2_name
        g['time2_img'] = team2_img
        g['resultado_time2'] = result_team2

        if g['resultado_time1'] == '' and g['resultado_time2'] == '':
            response['proximos']['jogos'].append(g)

        else:
            response['ultimos']['jogos'].append(g)


    # table
    table = soup_g4.find('table', {'class': 'table table-cup table-striped margin-bottom-25'})
    tbody = table.find('tbody')
    trs = table.find_all('tr')

    del trs[0]

    for tr in trs:
        team = {}

        tds = tr.find_all('td')

        team['posicao'] = tds[0].find('b').text
        team['img'] = tds[1].find('img')['src']
        team['nome'] = tds[1].find('span').text
        team['pontos'] = tds[2].text
        team['jogos'] = tds[3].text

        response['tabela'].append(team)

    return json.dumps(response)

if __name__ == '__main__':
    app.run()