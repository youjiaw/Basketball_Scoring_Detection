# Basketball_Scoring_Detection


# 程式碼說明
## img_effect.py

每個函式代表不同的濾鏡

filter_imgs/origin.png為範例圖片
執行img_effect.py可以看到各種濾鏡的結果(同目錄)
```python
python img_effect.py
```

## edit.py

MoviePyTest內有範例影片跟音樂
```python
audio = AudioFileClip(input_audio_name).subclip(45,52)
```
其中subclip表剪輯音樂，這裡代表剪45秒至52秒的地方

若只是要完成作業那就上傳很多30秒的音樂就好，這樣就不用剪
```python
AddSoundEffect(video, audio, origin_audio=false):
```
origin_audio用來選擇是否保留原影片的音軌

在此目錄執行edit.py可以看到加上音樂及慢動作兩種結果(同目錄)
```python
python edit.py
```
## weather.py
用來取得未來八小時的天氣預報 
```python
python weather.py
```

## future_games_2.py
取得未來七天的賽程及資訊

function用法:
* get_NBA_schedule(year): year為賽季開始的年份
例如現在的賽季為2021年度
```python
get_NBA_schedule('2021')
```

或著直接執行此程式 : 
```python
python future_games_2.py
```
執行結果存在NBA_future_game_2目錄
時間為台灣(UTC+8)時間
