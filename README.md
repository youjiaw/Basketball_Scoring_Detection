# Basketball_Scoring_Detection

# 專題動機與目的
籃球是一項風靡全球的運動，根據教育部體育署的調查，有運動的民眾最常從事的運動項目中，籃球為第四名（8.8%），而沒有運動習慣的民眾最有可能從事的運動項目中，籃球則為第五名（3.6%）。而為確保比賽的公平性，每場籃球比賽都會錄製影片。近年來隨著方便快速的網路傳輸技術蓬勃發展，人們能輕鬆獲得大量的籃球比賽影片。透過這些影片，球迷得以關注喜愛的球星、教練能夠協助球隊分析戰術、球員亦可回顧自己的表現等。然而，觀看整段比賽影片是非常耗時的，在一場球賽中，最大亮點往往是進球的時刻，因此我們希望建立一個能在影片中自動判斷出進球時刻並剪輯進球片段的系統，幫助使用者快速得到想要的資訊。  
除此之外，我們也發現到近年來由於新冠病毒的肆虐，大大改變了民眾的運動模式。根據教育部體育署的調查，在家運動的比例（15.3%）較109年（9.0%）大幅增加6.3%，同時為了不群聚打球，熱愛籃球的民眾們只能個別練習相關的訓練動作，對於打球的熱忱往往大不如前，運動頻率隨之下降。因此，我們希望建構一個智慧籃球運動的程式，讓使用者能夠記錄與監測自己的運動狀況，並透過與其他使用者互動、比較的方式，在疫情期間也可以提升打球的動力，讓他們重拾運動熱忱同時提高個人的免疫力。

# 相關研究
欲判斷是否進球，最直覺的方法是透過籃球是否通過籃筐的位置來判定，此方法雖簡單明瞭，但此方法問題在於，觀賞者所獲取的籃球影片，通常不會同時提供兩種以上的視角，因此若單以拍攝影片之鏡頭視角來判斷，可能會發生籃球與籃筐位置確實重疊，但籃球卻未真正進入籃筐的情況，將會造成判斷錯誤的問題。以下是我們找到的相關研究:  


# 設計原理

# 程式碼說明
## 進球判斷程式碼說明
#### final.py

利用YOLOv4模型進行辨識，在判斷影片中的是否有進球後，將進球片段擷取出來。

檔案在Basketball_Scoring_Detection資料夾中，要執行此檔案需要先創建一個python3.6的環境

```bash
conda create --name (your env name) python=3.6
```

進入環境後執行以下指令下載requirements.txt

（執行網頁程式碼也需要此環境）

```bash
pip install -r requirements.txt
```

隨後下載model_datas到與final.py的同目錄下，並更改final.py第9、10行的影片輸入位置和名稱，及第13行的精華片段輸出位置，完成後即可使用。

```python
python final.py
```
<<<<<<< HEAD
## weather.py
用來取得未來八小時的天氣預報
=======

## 網頁程式碼說明

### 首頁
#### weather.py
用來取得未來八小時的天氣預報 
>>>>>>> 860c5736083e66f8a0eef4b8e987b7f83242113c
```python
python weather.py
```

#### future_games_2.py
取得未來七天的賽程及資訊

資料來源: https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{year}/league/00_full_schedule.json

year為賽季開始的年份

例如現在的賽季為2021年度: https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2021/league/00_full_schedule.json


function用法:
* get_NBA_schedule(year) -> return **list** of (date,
                                                time,
                                                game_status,
                                                visiting_team,
                                                vteam_record,
                                                home_team,
                                                hteam_record,
                                                seri,
                                                arena_city,
                                                arena_state)
```python
get_NBA_schedule('2021')
```

result

![img](./NBA_future_game_2/result.png)


### 上傳頁面
#### edit.py

MoviePyTest內有範例影片跟音樂
```python
audio = AudioFileClip(input_audio_name)
```
提供五首30秒音樂供使用者選擇，修改音樂檔名即可使用
```python
input_audio_name = "Run The Clock.mp3"
```

```python
AddSoundEffect(video, audio, origin_audio=false):
```
origin_audio用來選擇是否保留原影片的音軌

在此目錄執行edit.py可以看到加上音樂及慢動作兩種結果(同目錄)
```python
python edit.py
```
#### img_effect.py

每個函式代表不同的濾鏡

filter_imgs/origin.png為範例圖片
執行img_effect.py可以看到各種濾鏡的結果(同目錄)
```python
python img_effect.py
```

### 能力追蹤


# 網頁操作說明

## 網頁執行步驟
