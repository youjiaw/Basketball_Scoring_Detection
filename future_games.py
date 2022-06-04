import requests
from bs4 import BeautifulSoup
import datetime
import os

def _to_string(input):
    return str(input.prettify())+'\n'

def games_html():
    OUTPUT_DIR = '.' + os.sep + 'NBA_FUTURE_GAME' + os.sep
    central_time = datetime.datetime.now() + datetime.timedelta(hours=-13)
    for _ in range(7):

        today = str(central_time.year)+'{:0>2d}'.format(central_time.month)+'{:0>2d}'.format(central_time.day)
        url = f'https://www.espn.com/nba/scoreboard/_/date/{today}'
        # url = f'https://www.espn.com/nba/scoreboard/_/date/20220605'
        content = requests.get(url).content
        soup = BeautifulSoup(content,'html.parser')
        games = soup.find_all('section', class_='Card gameModules')
        if(games[0].find('h4', class_="n5 tc pv6 clr-gray-05")!=None):
            print(today + ': No game')
        else:
            # with open(today+'.php', 'w') as f:
            #     f.write("<?php\necho ('")
            #     f.writelines(map(_to_string, games))
            #     f.write("');\n?>")
            with open(OUTPUT_DIR + today + '.txt', 'w') as f:
                f.writelines(map(_to_string, games))

        central_time += datetime.timedelta(days=1)
        


if __name__=='__main__':
    games_html()