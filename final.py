import cv2
import time
import sys
import traceback
import os
import tqdm

# ----------modify input video here----------
input_video_dir = "/Users/apple/Desktop/專題/籃球/training and testing datas/final_test"
video_name = "final_test" + ".mp4"

# ----------modify ouput highlight video here----------
highlight_saving_dir = "/Users/apple/Desktop/"

# ----------modify cfg and weight file here----------
# basketball
CONFIG_b = 'model_datas/basketball_data/cfg/yolov4-basketball.cfg'
WEIGHT_b = 'model_datas/basketball_data/weights/yolov4-basketball_best_2.weights'
class_dir_b = "model_datas/basketball_data/obj.names"
# shot
CONFIG_s = 'model_datas/shot_data/cfg/yolov4-shot.cfg'
WEIGHT_s = 'model_datas/shot_data/weights/yolov4-shot_best.weights'
class_dir_s = "model_datas/shot_data/obj.names"

# --------------------paramaters--------------------
# initial skip frames
frame_batch_init = 10

score_indexes = []#
shot_start_indexes = []#
shot_start_frame = 0

is_shooting = 0
is_score_f = 0
scoring_frames = 0
scoring_frames_target = 2

# hoop's position
(h0, h1, h2, h3) = (0, 0, 0, 0)

# skip frame
checking_times = 3
shot_end_check = checking_times
frame_batch = frame_batch_init
previous_ball_height = 0
ball_overlapping_hoop = 0;
ball_is_dropping = 0

# 讀取模型與訓練權重         
def initNet():
    # basketball
    net_b = cv2.dnn.readNet(CONFIG_b, WEIGHT_b)
    model_b = cv2.dnn_DetectionModel(net_b)
    model_b.setInputParams(size=(608, 608), scale=1 / 255.0, swapRB=True)
    
    # shot
    net_s = cv2.dnn.readNet(CONFIG_s, WEIGHT_s)
    model_s = cv2.dnn_DetectionModel(net_s)
    model_s.setInputParams(size=(608, 608), scale=1/255.0, swapRB=True)
    
    return model_b, model_s

def adjust_skip_frame_batch(y_ball): 
    global frame_batch
    global previous_ball_height
    # above hoop
    if y_ball < h3:
        frame_batch = 5
        global ball_is_dropping
        if y_ball > previous_ball_height: # start going down
            ball_is_dropping = 1
            frame_batch = 1

def Detect_Basketball(classes, confs, boxes):
    Biggest_ball = 0
    for box in boxes:
        if box[2] + box[3] > Biggest_ball:
            Biggest_ball = box[2] + box[3]
    for (classid, conf, box) in zip(classes, confs, boxes):
        if box[2] + box[3] == Biggest_ball:
            x, y, w, h = box
            (x2, y2) = (x + w, y + h)

            # append ball's center to trace
            if classid == 0:
                center = (int((x + x2) / 2), int((y + y2) / 2))
                global is_shooting
                if y + h < h1:  # ball is higher than hoop
                    is_shooting = 1
                    if frame_batch_init > 0:
                        adjust_skip_frame_batch(center[1])
                else:
                    # whether score
                    if is_shooting == 1 and y > h3:
                        global shot_end_check
                        if shot_end_check > 0:
                            shot_end_check -= 1
                        else:
                            global scoring_frames
                            global shot_start_frame

                            if scoring_frames >= scoring_frames_target:
                                global is_score_f
                                is_score_f = 1
                                shot_start_indexes.append(shot_start_frame)
                                # print("score!")
                                
                            global frame_batch
                            global ball_is_dropping
                            ball_is_dropping = 1
                            shot_start_frame = 0
                            scoring_frames = 0
                            is_shooting = 0
                            frame_batch = frame_batch_init
                            shot_end_check = checking_times


                global previous_ball_height
                previous_ball_height = y
                
                global ball_overlapping_hoop
                if center[0]>h0 and center[0]<h2 and center[1]>h1 and center[1]<h3:
                    ball_overlapping_hoop = 1
                else:
                    ball_overlapping_hoop = 0
                    

def Detect_Hoop(classes, confs, boxes):
    highest_conf = 0
    for conf in confs:
        if conf > highest_conf:
            highest_conf = conf
    for (classid, conf, box) in zip(classes, confs, boxes):
        if conf == highest_conf:
            x, y, w, h = box
            (x2, y2) = (x + w, y + h)
        
            global scoring_frames
            if classid == 0:
                scoring_frames += 1
            # use not score as hoop
            global h0, h1, h2, h3
            (h0, h1, h2, h3) = (x, y, x2, y2)


def save_highlight_frames():
    score_count = len(shot_start_indexes)

    if score_count<=0:
        return
    
    print("The video has ",score_count," scoring shots.")
        
    video_path = input_video_dir + "/" + video_name
    output_path = highlight_saving_dir
    output_video_name = video_name

    video_capture = cv2.VideoCapture(video_path)
    video_capture.set(1, 0)

    frame_w = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_final = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video_path = os.path.join(output_path, output_video_name)
    # print(out_video_path)
    label_video_writer = cv2.VideoWriter(out_video_path, fourcc, frame_fps, (frame_w, frame_h))

    frame_init = 0
    frame_length = frame_final - frame_init

    print('start makeing highlight video    ')
    print("start: ",shot_start_indexes)
    print("end  : ",score_indexes)
    pbar = tqdm.tqdm(total=frame_length, mininterval=0.001)

    target = 0
    frames_before_hoop_height = int(frame_fps)
    print("frames_before_hoop_height:",frames_before_hoop_height)
    if frames_before_hoop_height >= shot_start_indexes[0]:
        target = score_indexes[0]
        
    last_score_end = score_indexes[score_count-1]

    # start reading video
    try:
        while True:
            ret, img = video_capture.read()
            pbar.update(1)
            if ret != True:
                break;
            frame_index = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_index > frame_final:
                break;
            if frame_index > last_score_end:
                print("reach the last scoring shot.")
                break;
            
            # ---- highlight check ----
            if (frame_index + frames_before_hoop_height) in shot_start_indexes:
                target = score_indexes[shot_start_indexes.index(frame_index + frames_before_hoop_height)]
                
            if frame_index <= target:
                label_video_writer.write(img)

    except:
        pass
    
    finally:
        pbar.close()
        video_capture.release()
        label_video_writer.release()
       
if __name__ == '__main__':
    
    start = time.time()

    video_path = input_video_dir + "/" + video_name
    video_capture = cv2.VideoCapture(video_path)
    video_capture.set(1, 0)
    
    frame_final = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print('-----------------------------------')
    print('      start    ')
    print('-----------------------------------')
    print('process frame length: ', frame_final)

    pbar = tqdm.tqdm(total=frame_final, mininterval=0.001)

    model_b, model_s = initNet()
    success = fail = 0
    number = 1

    skip_count = 0
    # start reading video
    try:
        while True:
            ret, img = video_capture.read()
            pbar.update(1)
            if ret != True:
                # print("Read video error")
                break;

            frame_index = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))

            if frame_index > frame_final:
                # print("Reach setting final frame")
                break;

            # skip some not shooting frame
            skip_count += 1
            if(skip_count < frame_batch):
                continue
            skip_count = 0

            # start detect
            classes, confs, boxes = model_b.detect(img, 0.4, 0.1)
            classes_s, confs_s, boxes_s = model_s.detect(img, 0.4, 0.1)

            if len(boxes) == 0:  # detect none
                fail += 1
            else:
                success += 1
                Detect_Basketball(classes, confs, boxes)

            # draw shot result
            if len(boxes_s) != 0:
                Detect_Hoop(classes_s, confs_s, boxes_s)

            number += 1
            
            if previous_ball_height < h3 and shot_start_frame==0:
                shot_start_frame = frame_index
            
            if is_score_f:
                score_indexes.append(frame_index)
                shot_start_frame = 0
                is_score_f = 0;

    except Exception as e:
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        line_num = lastCallStack[1]  # 取得發生的行號
        func_name = lastCallStack[2]  # 取得發生的函數名稱
        error_infor = "line {}, in {}: [{}] {}".format(line_num, func_name, error_class, detail)
        print(detail)
        print(error_infor)

    finally:
        pbar.close()
        video_capture.release()

    print('※ {} 張內， 辨識{} 張、省略 {} 張'.format(frame_final, number, frame_final-number))
    end = time.time()
    print("執行時間：%f 分" % float((end - start) / 60))
    
    
    # save shot list and making highlight video
    save_highlight_frames()

    