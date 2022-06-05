import json
import datetime
import requests
import os

# get NBA schedule data as JSON
year = '2021'
r = requests.get('https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + year + '/league/00_full_schedule.json')
json_data = r.json()

# prepare output files
with open("NBA_future_game_2"+os.sep+"filtered_schedule.csv", "w") as fout:

    # fout = open("filtered_schedule.csv", "w")
    # fout.writelines('GameDate, GameID, Visitor, Home, HomeWin')
    fout.writelines('GameDate, Time, Status, Visitor, Home, Visit W-L Record, Home W-L Record, Seri, City, State')

    current_dt = datetime.datetime.now() 

    time_delta = datetime.timedelta(hours=8)

    # loop through each month/game and write out stats to file
    for i in range(len(json_data['lscd'])):
        for j in range(len(json_data['lscd'][i]['mscd']['g'])):
            # gamedate = json_data['lscd'][i]['mscd']['g'][j]['gdte']
            date_utc = json_data['lscd'][i]['mscd']['g'][j]['gdtutc']
            # gamedate_dt = datetime.datetime.strptime(gamedate, "%Y-%m-%d")
            time_utc = json_data['lscd'][i]['mscd']['g'][j]['utctm']

            date_time_dt = datetime.datetime.strptime(date_utc+'-'+time_utc, "%Y-%m-%d-%H:%M") + time_delta
            
            if (date_time_dt - current_dt).days < 0 or (date_time_dt - current_dt).days >= 7:
                continue

            date_time_list = date_time_dt.strftime("%Y-%m-%d-%H-%M").split('-')

            date = '/'.join(date_time_list[:3])
            time = ':'.join(date_time_list[3:])

            

            # game_id = json_data['lscd'][i]['mscd']['g'][j]['gid']
            game_status = json_data['lscd'][i]['mscd']['g'][j]['stt']

            visiting_team = json_data['lscd'][i]['mscd']['g'][j]['v']['ta']
            vteam_record = json_data['lscd'][i]['mscd']['g'][j]['v']['re']

            home_team = json_data['lscd'][i]['mscd']['g'][j]['h']['ta']
            hteam_record = json_data['lscd'][i]['mscd']['g'][j]['h']['re']

            seri = json_data['lscd'][i]['mscd']['g'][j]['seri']

            arena_city = json_data['lscd'][i]['mscd']['g'][j]['ac']
            arena_state = json_data['lscd'][i]['mscd']['g'][j]['as']
            



            fout.write('\n' + date +','+ time +','+ game_status +',' + visiting_team
                        +','+ home_team + ','+ vteam_record+ ','+ hteam_record
                        +','+ seri +','+ arena_city +','+ arena_state)

            # don't access scores for games that haven't been played yet
            # if(gamedate_dt < current_dt):  
            #     home_team_won = json_data['lscd'][i]['mscd']['g'][j]['h']['s'] > json_data['lscd'][i]['mscd']['g'][j]['v']['s']
            #     fout.write(','+ str(home_team_won))

            
    # fout.close()
    r.close()
