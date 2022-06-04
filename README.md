# Basketball_Scoring_Detection

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