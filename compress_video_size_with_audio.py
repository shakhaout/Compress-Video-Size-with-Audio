#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import cv2
import numpy as np
#ffpyplayer for playing audio
from ffpyplayer.player import MediaPlayer
import subprocess
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-input', help='Input the video')
parser.add_argument('-output', help='Output video file name')
args =parser.parse_args()
# # Reduce frame size

video_path=args.input
def PlayVideo(video_path):
    cap=cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Frame Count:",frame_count)
    print('Width: ',cap.get(3))
    print("Height: ",cap.get(4))
    FPS = cap.get(cv2.CAP_PROP_FPS)
    print('FPS:',FPS)
    player = MediaPlayer(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp_output.mp4',fourcc,FPS,(480,320))
    i=1
    pbar =tqdm(total=frame_count)
    while cap.isOpened():
        pbar.update(i)
        ret, frame=cap.read()
        audio_frame, val = player.get_frame()
        if not ret:
            print("End of video")
            break
        if cv2.waitKey(28) & 0xFF == ord("q"):
            break
        frame = cv2.resize(frame, dsize=(480,320))
        out.write(frame)
        cv2.imshow("Video", frame)
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
    cap.release()
    out.release()
    cv2.destroyAllWindows()
PlayVideo(video_path)


# # Extract audio 

command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn temp_audio.wav".format(args.input)

subprocess.call(command, shell=True)


# # Merge audio with muted video

cmd = 'ffmpeg -i temp_audio.wav -i temp_output.mp4 {}'.format(args.output)
subprocess.call(cmd)#Return to ‘0’ means the merge is successful

## remove the temporary files

os.remove('temp_output.mp4')
os.remove('temp_audio.wav')




