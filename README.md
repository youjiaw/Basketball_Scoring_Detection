# Basketball_Scoring_Detection
- [專題動機與目的](#專題動機與目的)
- [相關研究](#相關研究)
- [設計原理](#設計原理)
  - [系統模型](#系統模型)
  - [網頁架構](#網頁架構)
  - [資料庫](#資料庫)
- [程式碼說明](#程式碼說明)
  - [進球判斷程式碼說明](#進球判斷程式碼說明)
    - [做法](#做法)
    - [程式執行](#程式執行)
  - [網頁程式碼說明 (程式位置可能不只一個、就都放上去括號說分別是做什麼的就好)](#網頁程式碼說明-程式位置可能不只一個就都放上去括號說分別是做什麼的就好)
    - [首頁](#首頁)
      - [天氣與相關賽事(爬蟲相關)](#天氣與相關賽事爬蟲相關)
        - [天氣](#天氣)
        - [相關賽事](#相關賽事)
    - [註冊與登入、登出](#註冊與登入登出)
      - [註冊](#註冊)
      - [登入](#登入)
      - [登出](#登出)
    - [上傳頁面](#上傳頁面)
      - [影片剪輯](#影片剪輯)
      - [特效編輯](#特效編輯)
        - [加入音效](#加入音效)
        - [加入濾鏡](#加入濾鏡)
    - [能力追蹤](#能力追蹤)
      - [顯示投籃準確度](#顯示投籃準確度)
      - [顯示歷史紀錄](#顯示歷史紀錄)
      - [比較](#比較)
      - [防懶功能](#防懶功能)
- [網頁操作說明](#網頁操作說明)
  - [安裝教學 (如何進入網頁)](#安裝教學-如何進入網頁)
  - [網頁操作說明](#網頁操作說明-1)
# 專題動機與目的
  籃球是一項風靡全球的運動，根據教育部體育署的調查，有運動的民眾最常從事的運動項目中，籃球為第四名（8.8%），而沒有運動習慣的民眾最有可能從事的運動項目中，籃球則為第五名（3.6%）。而為確保比賽的公平性，每場籃球比賽都會錄製影片。近年來隨著方便快速的網路傳輸技術蓬勃發展，人們能輕鬆獲得大量的籃球比賽影片。透過這些影片，球迷得以關注喜愛的球星、教練能夠協助球隊分析戰術、球員亦可回顧自己的表現等。**然而，觀看整段比賽影片是非常耗時的，在一場球賽中，最大亮點往往是進球的時刻，因此我們希望建立一個能在影片中自動判斷出進球時刻並剪輯進球片段的系統，幫助使用者快速得到想要的資訊。**  
  除此之外，我們也發現到近年來由於新冠病毒的肆虐，大大改變了民眾的運動模式。根據教育部體育署的調查，在家運動的比例（15.3%）較109年（9.0%）大幅增加6.3%，同時為了不群聚打球，熱愛籃球的民眾們只能個別練習相關的訓練動作，對於打球的熱忱往往大不如前，運動頻率隨之下降。因此，我們希望**建構一個智慧籃球運動的程式，讓使用者能夠記錄與監測自己的運動狀況，並透過與其他使用者互動、比較的方式，在疫情期間也可以提升打球的動力，重拾運動熱忱同時提高個人的免疫力。**

# 相關研究
欲判斷是否進球，最直覺的方法是透過籃球是否通過籃筐的位置來判定，此方法雖簡單明瞭，但此方法問題在於，觀賞者所獲取的籃球影片，通常不會同時提供兩種以上的視角，因此若單以拍攝影片之鏡頭視角來判斷，可能會發生籃球與籃筐位置確實重疊，但籃球卻未真正進入籃筐的情況，將會造成判斷錯誤的問題。  
因此在這次專題中，需要解決
1. 辨識籃球和藍筐  
2. 確認是否進球  
這兩項問題，以下是我們找到的相關研究:  
* 參考文獻[1] Ratgeber, L., Ivankovic, Z., Gojkovic, Z., Milosevic, Z., Markoski, B., & Kostic–Zobenica, A. (2019). Video Mining in Basketball Shot and Game Analysis. Acta Polytechnica Hungarica, 16(1), 7-27.  
利用將畫面轉換成HSV顏色模型的方式辨識籃球和籃筐，並依照籃球在通過籃筐上方區域後是否通過籃框下方區域來決定是否進球。
  * 優點:每秒減少2/3的畫面使用來提高辨識速度而不影響準確度，因為利用球是否通過籃筐上方與下方作為判斷依據，這件事的發生不會快到以至於在減少的畫面集合中沒有被記錄下來
  * 缺點:籃球到籃筐下方區域時，可能會受到球員的干擾而影響判定結果，且此方法無法判斷籃球是從籃筐內部還是外部通過，可能會造成籃球與籃筐範圍重疊但未進入籃筐卻被誤判成進球的情況。  
* 參考文獻[2] Fu, X. B., Yue, S. L., & Pan, D. Y. (2021). Camera-based basketball scoring detection using convolutional neural network. International Journal of Automation and Computing, 18(2), 266-276.  
利用YOLO模型判斷出籃筐位置，並利用圖像差分找出移動中的物體，最後依照此物體是否有通過籃筐位置來判斷是否進球。
  * 優點:只要籃球有通過籃筐範圍就會被判斷成有進球，所以進球一定會被判斷出來
  * 缺點:無法判斷籃球是從籃筐內部還是外部通過，可能會造成籃球與籃筐範圍重疊但未進入籃筐卻被誤判成進球的情況。  
* 參考文獻[3] Huang, C. L., Shih, H. C., & Chen, C. L. (2006, July). Shot and scoring events identification of basketball videos. In 2006 IEEE International Conference on Multimedia and Expo (pp. 1885-1888). IEEE.  
用SVM(Support Vector Machine)來辨識籃球與籃筐，並將籃球依照是否被籃網覆蓋區分為在籃筐內、在籃筐外兩種類別。
  * 優點:可以在籃球和籃筐重疊時分辨出籃球是否在籃筐內
  * 缺點:過程中每一幀畫面都要判斷SVM的分數以確定籃球和籃筐的位置，故處理影片的速度較慢。  

# 設計原理
## 系統模型
所提方法的架構圖如下
<img width="1180" alt="image" src="https://user-images.githubusercontent.com/92151140/173359238-2b218262-b7e7-462b-b8a8-96640643f02a.png">
接下來會依序說明各步驟
* 物件辨識模型 (用來辨識籃球與籃框)
  * 採用YOLOv4
  * 主要架構為
    * Backbone：CSPDarknet53
    * Neck：SPP + PAN
    * Head：YOLOv4
    <img width="448" alt="image" src="https://user-images.githubusercontent.com/92151140/173353777-eaf6c56a-e1b0-4b12-917f-8598fa78777c.png">

* 判斷進球
  1. 籃球是否高於籃筐:在進球前籃球一定需要高於籃筐，所以我們利用籃球最低點的位置是否高於籃筐最高點作為投籃開始的判斷依據，而投籃結束的依據則是籃球最高點低於籃筐最低點，我們會在這段區間內進行進球的判斷  
  2. 籃球中心點是否位於籃框範圍內且被籃網覆蓋
    * 判斷籃球中心點座標是否位於籃筐範圍內：在投籃過程中，籃球中心點必定要進入籃筐範圍內才有可能是一顆投進的球，因此我們將此標準作為進球的第一步判斷
    * 判斷籃球在是否在籃筐內部：當上述成立時，代表這幀照片有兩種可能的情況：
      1. 籃球在籃筐內部
      2. 籃球與籃筐位置重疊，但籃球在籃筐外部
    * 為了解決誤判的情況，在訓練籃筐模型時將標記的類別分為兩種：有進球的籃筐與沒進球的籃筐，如果籃筐範圍內有籃球而且籃網將籃球覆蓋住，就會被標示為有進球，其餘則標成沒進球  
 ## 網頁架構
我們的網頁主要是依據下圖的functional map做設計
而網頁的架設是使用Django
<img width="903" alt="image" src="https://user-images.githubusercontent.com/92151140/173358558-a11d7dc9-9d9f-44ad-8cec-17edb8518364.png">    
## 資料庫
//TODO

# 程式碼說明
這部分的內容主要分為 1. 自動判斷進球時刻的剪輯系統 2. 前端網頁 這兩個部分
## 進球判斷程式碼說明
程式為`Basketball_Scoring_Detection/final.py`
### 做法 
利用YOLOv4模型進行辨識，在判斷影片中的是否有進球後，將進球片段擷取出來。(此處的詳細做法如**設計原理**中所示，這邊主要說明如何單獨執行此檔案)
### 程式執行
要執行此檔案需要先創建一個python3.6的環境

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

## 網頁程式碼說明 (程式位置可能不只一個、就都放上去括號說分別是做什麼的就好)
這部分的程式在`bballApp`
### 首頁
會顯示1. 目前天氣以及今天是否適合打球  2. 近七日的相關賽事  
#### 天氣與相關賽事(爬蟲相關)
用get取得json，並將內容篩選為我們所需的資料
##### 天氣
程式為`bballApp/mainsite/weather.py`  
作用:用來取得未來八小時的天氣預報  
資料來源1:https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-A89DDEBE-215B-4AE4-AA1B-7A7F52C58235&downloadType=WEB&format=JSON  

資料來源2:https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=fdac918f-b34b-4dd6-94b2-338ea65d1a3f&format=json  

```python
python weather.py
```

##### 相關賽事
程式為`bballApp/mainsite/future_game.py`  
作用:取得未來七天的賽程及資訊  
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

### 註冊與登入、登出
#### 註冊
程式為  
作用:註冊帳號並寄驗證信  
//TODO做法  

#### 登入
程式為  
作用:登入會員  
//TODO做法  

#### 登出
程式為  
作用:登出會員  
//TODO做法



### 上傳頁面
可以上傳 1. 想要剪輯精華的比賽影片  2. 個人訓練影片，剪輯完成後可自行加入特效  
#### 影片剪輯
參見 [進球判斷程式碼說明](#進球判斷程式碼說明)
#### 特效編輯
##### 加入音效
程式為  
作用:加入音效  
// TODO (求救 這個檔案去哪了QQ)  
edit.py

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
##### 加入濾鏡
程式為  
作用:加入濾鏡  
//TODO做法  

img_effect.py

每個函式代表不同的濾鏡

filter_imgs/origin.png為範例圖片
執行img_effect.py可以看到各種濾鏡的結果(同目錄)
```python
python img_effect.py
```

### 能力追蹤
這部分使用者可以監控自己的運動情況1. 投籃準確度 2. 查詢歷史紀錄 3. 與其他使用者比較 4. 防懶(會顯示持續運動天數或連續沒有運動的天數)
#### 顯示投籃準確度
程式為 //TODO程式位置  
作用: 顯示至目前為止的投籃準確度曲線  
//TODO做法

#### 顯示歷史紀錄
程式為 //TODO程式位置  
作用: 同標題  
//TODO做法  

#### 比較
程式為//TODO程式位置  
作用:可以比較 1. 持續天數 2. 平均投籃準確度  
//TODO做法  

#### 防懶功能
程式為 //TODO程式位置  
作用: 1. 告知使用者目前持續天數  2. 提醒使用者已經有幾天沒運動了  
//TODO做法  


# 網頁操作說明
## 安裝教學 (如何進入網頁)
執行網站需要linux系統，並創建虛擬環境

```bash
#安裝pip3
sudo apt-get -y install python3-pip
#安裝virtualenv
sudo pip3 install virtualenv
```

在目的資料夾中使用virtualenv建立一個虛擬環境

```bash
#建立虛擬環境
virtualenv VENV
#進入虛擬環境
source VENV/bin/activate
```
接著下載兩份requirements.txt，第二份在Basketball_Scoring_Detection資料夾裡

```bash
pip install -r requirements.txt
```

如果過程有報錯，可以嘗試使用conda下載，其中如果mysqlclient有報錯，需請嘗試執行第二行指令

```bash
conda install ...
conda install MySQLClient
```

最後下載bballApp的資料夾，進入裡面後，輸入以下指令以啟動server，完成後前往顯示的網站連結即可

```python
python3 manage.py makemigrations
python3 manage.py migrate
#啟動surver
python3 manage.py runserver
```

如果啟動後有cannot import ... 的報錯（requirements.txt裡下載的套件）

可以試看看重新下載一次該套件

```python
pip uninstall ...
pip install ...
```
## 網頁操作說明
### 首頁
這邊會顯示當前天氣、相關賽事以及是否適合打球，使用者可以選擇註冊或登入
<img width="1086" alt="image" src="https://user-images.githubusercontent.com/92151140/173490193-f9d09140-3835-4d7f-b0b6-a271609b762f.png">  

**註冊教學**
1. 填入圖中的相關資訊
<img width="750" alt="image" src="https://user-images.githubusercontent.com/92151140/173490330-97778d03-3004-49f7-8314-5475b7c1b770.png">  
2.  註冊完成
<img width="748" alt="image" src="https://user-images.githubusercontent.com/92151140/173490474-1901a226-4365-4d4f-9152-5a6f9106229a.png">  
p.s 要記得去電子信箱啟用帳號  
<img width="490" alt="image" src="https://user-images.githubusercontent.com/92151140/173490568-0a206f82-fdb6-407f-a2ca-92f4db422681.png">
登入後的頁面  
<img width="1227" alt="image" src="https://user-images.githubusercontent.com/92151140/174200967-2bf289cf-a27e-4fd5-9584-f9ae0fb1a645.png">
這邊會有 1. 上傳影片  2. 進入能力追蹤 可以按，下面說明點擊後的情境


### 上傳影片
1. 進入頁面後，可以選擇要上傳的是想要剪輯的比賽影片，或者是個人訓練影片 `註:只有上傳個人訓練影片才會計入能力追蹤`  
<img width="779" alt="image" src="https://user-images.githubusercontent.com/92151140/174219406-4fec08c6-2f15-4830-ae39-bdfc1d3a642c.png">  
2. 選擇完可以挑選mp4檔上傳  
<img width="779" alt="image" src="https://user-images.githubusercontent.com/92151140/174220312-66b3b074-3f2e-4fc4-ba05-fa0382f776e4.jpg">  
<img width="779" alt="image" src="https://user-images.githubusercontent.com/92151140/174220369-b6e290aa-2e9c-492e-91da-558f0cef32ec.png">  
<img width="779" alt="image" src="https://user-images.githubusercontent.com/92151140/174220445-81ad20c7-5aea-453b-b2a0-38ff35d3b54b.png">  
3. 剪輯中 ✂️  
<img width="771" alt="image" src="https://user-images.githubusercontent.com/92151140/174220629-238383aa-cb85-4864-a871-10c335cdba99.png">  
4. 剪輯完可以選擇直接下載片段或者是再進入`編輯特效`的功能，製作出有自己特色的精華片段
<img width="781" alt="image" src="https://user-images.githubusercontent.com/92151140/174220833-44b78414-383d-43df-aa2b-c48630b8fb6d.png">  
#### 編輯特效
再這邊我們可以選擇想要的濾鏡、音效以及是否想要慢動作  
<img width="1262" alt="image" src="https://user-images.githubusercontent.com/92151140/174221239-ffa908a9-d162-4fde-bda1-3d1eba86e9f6.png">  
5. 選擇完畢點擊製作影片，會再回到 **3.剪輯中 ✂️ **

### 能力追蹤
* 進入頁面後，顯示的是  
  * 至今為止的每日投籃準確率趨勢圖 `每日投籃趨勢值:使用者將每日的練習視頻上傳後，片中的進球比率即為該日投籃準確率`  
  * 防懶功能
    * 若有持續運動 ➡️ 顯示已持續運動幾天
    * 若持續**沒**運動 ➡️ 顯示已有幾天沒運動
<img width="1215" alt="image" src="https://user-images.githubusercontent.com/92151140/174201072-20a65669-798d-455c-a551-bae4d1e0bd75.png">

#### 查詢歷史紀錄
內容為至今為止上傳過的**個人訓練影片**，上面會顯示上傳日期、精華時長與該日的準確率  
<img width="1214" alt="image" src="https://user-images.githubusercontent.com/92151140/174201651-85d965fb-fa0a-4945-bf06-3739724d09bf.png">

#### 與其他使用者比較
使用者可自行選擇想要評比的項目  
<img width="758" alt="image" src="https://user-images.githubusercontent.com/92151140/174201861-4683a121-1214-4a03-9d92-e0b55e43c5fa.png">
##### 選擇比較準確率
會顯示目前的平均投籃準確率，以及和資料庫中其他使用者比較後之結果(綠底部分為使用者的資料)  
<img width="757" alt="image" src="https://user-images.githubusercontent.com/92151140/174201933-7fc3e483-f00b-44e2-b396-4da4bf90dab4.png">

##### 選擇比較持續天數
會顯示目前持續運動天數，以及和資料庫中其他使用者比較後之結果(綠底部分為使用者的資料)  
<img width="761" alt="image" src="https://user-images.githubusercontent.com/92151140/174202108-52dd9256-8e79-4654-a683-15a1390f6e22.png">

* 參考demo影片，影片網址:
* 注意事項
  * 註冊完如果沒收到信，可以去垃圾郵件的地方看看  
  * 在進入網站後，隨時點擊左上logo都可以回到首頁呦!
