import requests
from bs4 import BeautifulSoup
import datetime
import os
import re

# def _to_string(input):
#     return str(input.prettify())+'\n'

def _game_date(input):
    f = input.find("h3", class_="Card__Header__Title Card__Header__Title--no-theme")
    return f.string

def _all_games_html_frags(input):
    f_list = input.find_all("section", class_="Scoreboard bg-clr-white flex flex-auto justify-between")
    return f_list


def _game_time(input):
    f = input.find("div", class_="ScoreCell__Time ScoreboardScoreCell__Time h9 clr-gray-03")
    return f.string

def _guest_html_frag(input):
    f = input.find("li", class_="ScoreboardScoreCell__Item flex items-center relative pb2 ScoreboardScoreCell__Item--away")
    return f

def _home_html_frag(input):
    f = input.find("li", class_="ScoreboardScoreCell__Item flex items-center relative pb2 ScoreboardScoreCell__Item--home")
    return f

def _team_name(input):
    f = input.find("div", class_="ScoreCell__TeamName ScoreCell__TeamName--shortDisplayName truncate db")
    return f.string

def _team_info(input):
    f_list = input.find_all("span", class_="ScoreboardScoreCell__Record")
    # return map(lambda x: x.string, f_list)
    return f_list

def _game_info(input):
    f = input.find("div", class_="ScoreboardScoreCell__Note clr-gray-05 n9 w-auto")
    return f.string

def games_html():
    OUTPUT_DIR = '.' + os.sep + 'NBA_FUTURE_GAME' + os.sep
    central_time = datetime.datetime.now() + datetime.timedelta(hours=-13)
    for _ in range(7):

        today = str(central_time.year)+'{:0>2d}'.format(central_time.month)+'{:0>2d}'.format(central_time.day)
        url = f'https://www.espn.com/nba/scoreboard/_/date/{today}'
        # url = f'https://www.espn.com/nba/scoreboard/_/date/20220605'
        content = requests.get(url).content
        soup = BeautifulSoup(content,'html.parser')
        games = soup.find('section', class_='Card gameModules')
        if(games.find('h4', class_="n5 tc pv6 clr-gray-05")!=None):
            print(today + ': No game')
        else:
            with open(OUTPUT_DIR + today + '.txt', 'w') as f:
                date = _game_date(games)
                print('game date :', date)
                f.write(date+'\n')

                for game_frag in _all_games_html_frags(games):
                    time = _game_time(game_frag)
                    print('time:', time)
                    if time!=None:
                        f.write(time+'\n')

                    pattern = r'\d+-\d+'

                    print('\n\nGuest:\n')
                    f.write('\n\nGuest:\n\n')
                    guest_f = _guest_html_frag(game_frag)

                    team_name = _team_name(guest_f)
                    print(team_name)
                    f.write(team_name+'\n')
                    # print('\t', end='')
                    # for info in _team_info(guest_f):
                    #     print(info, end=' ')

                    # print()


                    f_list = _team_info(guest_f)
                    print(f_list[0].string)
                    f.write(f_list[0].string+'\n')

                    re_result = re.search(pattern, str(f_list[1])).group(0)
                    print(re_result)
                    f.write(re_result+'\n')
                    # print(f_list)

                    print('\n\nHome:\n')
                    f.write('\n\nHome:\n\n')
                    home_f = _home_html_frag(game_frag)

                    team_name = _team_name(home_f)
                    print(team_name)
                    f.write(team_name+'\n')
                    # print('\t', end='')
                    # for info in _team_info(home_f):
                    #     print(info, end=' ')

                    # print()

                    f_list = _team_info(home_f)
                    print(f_list[0].string)
                    f.write(f_list[0].string+'\n')

                    re_result = re.search(pattern, str(f_list[1])).group(0)
                    
                    print(re_result)
                    f.write(re_result+'\n')
                    # print(f_list)
                    
                    
                    game_info = _game_info(game_frag)
                    print('\n\n'+game_info+'\n\n\n')
                    f.write('\n\n'+game_info+'\n\n\n\n')


        central_time += datetime.timedelta(days=1)
        


if __name__=='__main__':
    games_html()