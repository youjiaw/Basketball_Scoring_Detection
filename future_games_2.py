import json
import datetime
import requests
import os

def get_NBA_schedule(year):

    # get NBA schedule data as JSON
    # year = '2021'
    r = requests.get('https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + year + '/league/00_full_schedule.json')
    json_data = r.json()

    r.close()

    # with open('NBA_future_game_2'+os.sep+'2021AllGames.json', 'w') as f:
    #     json.dump(json_data, f)

    # prepare output files
    # with open("NBA_future_game_2"+os.sep+"filtered_schedule.csv", "w") as fout:

        # fout = open("filtered_schedule.csv", "w")
        # fout.writelines('GameDate, GameID, Visitor, Home, HomeWin')
    # fout.writelines('GameDate, Time, Status, Visitor, Visit W-L Record, '
    #                 'Home, Home W-L Record, Seri, City, State')

    current_dt = datetime.datetime.now()

    time_delta = datetime.timedelta(hours=8)

    hasGame = True
    # loop through each month/game and write out stats to file
    for month_games in json_data['lscd']:
        if month_games['mscd']['mon']==current_dt.strftime("%B"):
            break
    else:
        print('no game')
        hasGame = False
    
    result = []

    if hasGame:
        for game in month_games['mscd']['g']:
            date_utc = game['gdtutc']
            time_utc = game['utctm']
            date_time_dt = datetime.datetime.strptime(date_utc+'-'+time_utc, "%Y-%m-%d-%H:%M") + time_delta
            if (date_time_dt - current_dt).days < 0 or (date_time_dt - current_dt).days >= 7:
                continue

            date_time_list = date_time_dt.strftime("%Y-%m-%d-%H-%M").split('-')

            date = '/'.join(date_time_list[:3])
            time = ':'.join(date_time_list[3:])

            

            game_status = game['stt']

            visiting_team = game['v']['ta']
            vteam_record = game['v']['re']

            home_team = game['h']['ta']
            hteam_record = game['h']['re']

            seri = game['seri']

            arena_city = game['ac']
            arena_state = game['as']
            



            # fout.write('\n' + date +','+ time +','+ game_status +',' + visiting_team
            #             + ','+ vteam_record+','+ home_team + ','+ hteam_record
            #             +','+ seri +','+ arena_city +','+ arena_state)
            result.append((date,
                           time,
                           game_status,
                           visiting_team,
                           vteam_record,
                           home_team,
                           hteam_record,
                           seri,
                           arena_city,
                           arena_state))

    
    

    return result

if __name__=='__main__':
    print(get_NBA_schedule('2021'))