from django.conf import settings
import cv2
import time
import sys
import traceback
import os
import tqdm
from . import img_effect

input_video_dir = settings.MEDIA_ROOT


def main(f, targetdir, filename):
        
    video_path = input_video_dir + "/" +targetdir + "/" + filename
    output_path = input_video_dir + "/filtered_videos"

    video_capture = cv2.VideoCapture(video_path)
    video_capture.set(1, 0)

    frame_w = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_final = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out_video_path = os.path.join(output_path, filename)
    print(video_path)
    print(out_video_path)

    video_writer = cv2.VideoWriter(out_video_path, fourcc, frame_fps, (frame_w, frame_h))

    # start reading video
    try:
        while True:
            ret, img = video_capture.read()
            if ret != True:
                print("-1")
                break
            frame_index = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_index > frame_final:
                print("-2")
                break


            if f == 1:
                img = img_effect.grayscale(img)
            elif f == 2:
                img = img_effect.HDR(img)
            elif f == 3:
                img = img_effect.bright(img, 60)
            elif f == 4:
                img, c = img_effect.pencil_sketch(img)
            elif f == 5:
                g, img = img_effect.pencil_sketch(img)
            elif f == 6:
                img = img_effect.sepia(img)
            elif fourcc == 7:
                img = img_effect.sharpen(img)
            elif f == 8:
                img = img_effect.summer(img)
            elif f == 9:
                img = img_effect.winter(img)
            elif f == 10:
                img = img_effect.invert(img)


            video_writer.write(img)

    except:
        pass
    
    finally:
        video_capture.release()
        video_writer.release()
       