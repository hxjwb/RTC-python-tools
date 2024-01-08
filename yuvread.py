# Description: read yuv file and show rgb image
# Author: hxj

import cv2
import numpy as np

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='input.yuv', help='input yuv file')
    parser.add_argument('--width', type=int, default=1920, help='width')
    parser.add_argument('--height', type=int, default=1080, help='height')
    parser.add_argument('--framerate', type=int, default=24, help='framerate')
    parser.add_argument('--frame', type=int, default=-1, help='frame count')
    parser.add_argument('-c', type=bool, default=False, help='manually control Mode, no auto play')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # parse arguments

    args = parse_args()
    
    # set values
    yuvfile = args.file
    w = args.width
    h = args.height
    framerate = args.framerate
    frame = args.frame

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
    
    cur = -1
    play = not args.c
    rgb = None
    
    refresh = False
    
    while True:
        print ('frame', cur)
        if cur == frame - 1:
            play = False
        
        if play or refresh:
            yuv = yuvfile.read(h*w*3//2)
            cur += 1
        
            yuv_np = np.frombuffer(yuv, dtype=np.uint8)
        
            # use cv2 to convert yuv to rgb
            yuv_np = yuv_np.reshape(h*3//2, w)
            rgb = cv2.cvtColor(yuv_np, cv2.COLOR_YUV2BGR_I420)
            
            if refresh:
                refresh = False # refresh done
        
        cv2.imshow("YUV viewer", rgb)
        # if i == frame - 1:
        #     cv2.waitKey(0)
        # else:
        #     cv2.waitKey(waitKey_time)
        
        # press 'q' to exit, press 'space' to pause and continue, press left arrow to go back, press right arrow to go forward
        key = cv2.waitKey(waitKey_time)
        if key == ord('q'):
            break
        elif key == ord(' '):
            play = not play
        
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
            refresh = True        # Need continue loop to refresh the image
        
        
    yuvfile.close()
    cv2.destroyAllWindows()
    
    
    
    