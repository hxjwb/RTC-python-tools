# Description: read yuv file and show rgb image with opencv
# Author: HUANG XIANGJIE

import cv2
import numpy as np

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='yuv file')
    
    parser.add_argument('-s', type=str, default='1920x1080', help='Input YUV size, default is 1920x1080')
    parser.add_argument('--framerate', type=int, default=24, help='Input YUV framerate')
    parser.add_argument('--frame', type=int, default=-1, help='frame count')

    parser.add_argument('-c', action='store_true', help='The video will pause at the beginning')
    parser.add_argument('-i', action='store_true', help='Iinformation will be shown on the image')
    
    args = parser.parse_args()
    return args

def get_info_str(f, frame, play):
    cur_percent = f / frame * 100
    cur_percent = round(cur_percent, 2)
    
    inforstr = '------- %.2f%% %d/%d ' % (cur_percent, f, frame)
    if play:
        inforstr += 'playing'
    else:
        inforstr += 'paused'
    inforstr += ' -------'
    
    return inforstr
if __name__ == '__main__':
    # parse arguments

    args = parse_args()
    
    # set values
    yuvfile = args.file
    
    try:
        w, h = args.s.split('x')
        w = int(w)
        h = int(h)
    except:
        print('Input YUV size is invalid. Please input like 1920x1080')
        exit(0)

    framerate = args.framerate
    frame = args.frame
    
    # TODO: check file exist and check w, h, framerate, frame is valid
    
    # read yuv file
    yuvfile = open(yuvfile, 'rb')
    
    # get frame count
    yuvfile.seek(0, 2)
    yuv_size = yuvfile.tell()
    yuvfile.seek(0, 0)
    frame_count = yuv_size // (h*w*3//2)
    print('frame_count', frame_count)
    
    if frame > frame_count:
        print('frame count is larger than total frame count')
        exit(0)
    
    if frame == -1:
        frame = frame_count # read all frames


    waitKey_time = int(1000 / framerate)
    
    cur = -1 # current frame
    
    play = not args.c # play or pause
    show_info = args.i # show info
    
    yuv_buffer = None
    refresh = False # when ctrl + left arrow or ctrl + right arrow, need refresh the image
    
    while True:
        
        inforstr = get_info_str(cur, frame, play)
        
        print('\r', end='')
        print(inforstr, end='')
        
        if cur == frame - 1:
            play = False
        
        if play or refresh or (cur == -1):
            yuv_buffer = yuvfile.read(h*w*3//2)
            cur += 1
            
        yuv_np = np.frombuffer(yuv_buffer, dtype=np.uint8)
        
        # use cv2 to convert yuv to rgb
        yuv_np = yuv_np.reshape(h*3//2, w)
        rgb = cv2.cvtColor(yuv_np, cv2.COLOR_YUV2BGR_I420)
            
        if show_info:
            # add text to image
            font = cv2.FONT_HERSHEY_SIMPLEX
            # transparent text background
            cv2.rectangle(rgb, (0, 0), (900, 50), (0, 0, 0), -1)
            cv2.putText(rgb, inforstr, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
        if refresh:
            refresh = False # refresh done
        
        cv2.imshow("YUV viewer", rgb)
        
        # press 'q' to exit, press 'space' to pause and continue, press left arrow to go back, press right arrow to go forward
        key = cv2.waitKey(waitKey_time)
        
        if key == ord('q'):
            print('\n') # print a new line
            break
        elif key == ord(' '):
            play = not play
        elif key == ord('i'):
            show_info = not show_info   
        elif key == 81: # left arrow
            if cur == 0:
                continue
            yuvfile.seek(-h*w*3//2*2, 1)
            cur -= 2
        elif key == 83 and play: # right arrow to fast forward
            if cur == frame - 1:
                continue
            yuvfile.seek(h*w*3//2, 1)
            cur += 1
            
        if key in [81, 83] and not play:
            if cur == frame - 1:
                continue
            refresh = True        # Need continue loop to refresh the image
        
        
    yuvfile.close()
    cv2.destroyAllWindows()
    
    
    
    