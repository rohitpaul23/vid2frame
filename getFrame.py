import matplotlib.pyplot as plt
import numpy as np
import cv2
import pywt
from pathlib import Path
from utils import resizeImg
import argparse

def getFrame(inputFile,
             outputDir = 'subject', 
             manual = False,
             START = 0, 
             END = -1, 
             ms_per_frame = 40, 
             TOP_CROP = 0,
             BOTTOM_CROP = -1,
             LEFT_CROP = 0,
             RIGHT_CROP = -1,
             METHOD = 'NONE',
             THRESH = 0):
    
    print(f'Processing filename: {inputFile}')
    # Open the MP4 file
    cap = cv2.VideoCapture(f'{inputFile}')
    filename = inputFile.split('/')[-1]
    folderName = filename.split('.')[0]

    
    if not manual:
        result_folder = Path(f'{outputDir}/{folderName}_default')
        result_folder.mkdir(parents=True, exist_ok=True)

        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f'Total frame : {total_frames}')
        # Loop through each frame and save it as an image file
        for i in range(total_frames):
            # Read the frame
            ret, frame = cap.read()
            
            # Save the frame as an image file
            frame_path = f"{result_folder}/frame_{i+1:03d}.png"
            cv2.imwrite(frame_path, frame)
            
            # Print progress
            if i % 100 == 0:
                print(f"Processed frame {i+1}/{total_frames}")
            
        # Release the video object
        cap.release()

    else:

        result_folder = Path(f'{outputDir}/{folderName}_{ms_per_frame}')
        result_folder.mkdir(parents=True, exist_ok=True)

        time_ms = START
        if END == -1:
            totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            #print(totalFrame)
            fps = cap.get(cv2.CAP_PROP_FPS)
            #print(fps)
            END = int(totalFrame*fps) - 1
        
        #print(START, END)
        idx = 0
        while time_ms < END:
            #print(time_ms)

            # Set the position of the video to the desired time
            cap.set(cv2.CAP_PROP_POS_MSEC, time_ms)

            # Read the next frame
            ret, frame = cap.read()
            resizeFrame = resizeImg(frame[TOP_CROP:BOTTOM_CROP, LEFT_CROP:RIGHT_CROP, :], 640, 512)
            
            score = THRESH + 1
            
            if METHOD == 'LAPLACIAN':
                #LAPLACIAN FILTER
                # convert frame to grayscale and calculate Laplacian variance
                gray = cv2.cvtColor(resizeFrame, cv2.COLOR_BGR2GRAY)
                lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                score = lap_var
                
            elif METHOD == 'TENANGRAD':
                #TENENGRAD ALGORITHM
                # Convert the region of interest to grayscale
                gray = cv2.cvtColor(resizeFrame, cv2.COLOR_BGR2GRAY)

                # Apply Sobel filters to calculate the gradients
                gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
                gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

                # Calculate the squared gradients
                squared_gradients = gx**2 + gy**2

                # Calculate the average of the squared gradients and return the square root of this value
                avg_squared_gradients = np.mean(squared_gradients)
                sharpness = np.sqrt(avg_squared_gradients)
                score = sharpness
                
            elif METHOD == 'WAVELET':
                #WAVELET BASED METHOD
                # convert the image to grayscale
                gray = cv2.cvtColor(frame[:,350:800,:], cv2.COLOR_BGR2GRAY)
            
                # apply wavelet transform
                coeffs = pywt.wavedec2(gray, 'db4', level=1)
            
                # calculate the high-frequency coefficients
                H = coeffs[1]
            
                # calculate the variance of the high-frequency coefficients
                variance = np.var(H)
                score = variance
            
            # if Laplacian variance is above threshold, add frame to sharp_frames
            if score < THRESH:
                time_ms += 1
            else:
                #print(time_ms)
                idx = idx + 1
                
                # If the frame was read successfully, save it to a file
                if ret:
                    cv2.imwrite(f'{result_folder}/frame_{idx:03d}.png', resizeFrame)
                
                time_ms += ms_per_frame


if __name__ == '__main__':
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Get Desired Frame from a video')

    # add arguments
    parser.add_argument('input_file', type=str, help='input video file path')
    parser.add_argument('output_dir', type=str, default='subject', help='output directory to store the frame')
    parser.add_argument("--manual", action="store_true", help="Manually get frame")
    parser.add_argument('--start', type=int, default=0, help='Starting point(in ms) from which frame will be acquired')
    parser.add_argument('--end', type=int, default=-1, help='Ending point(in ms) till which frame will be acquired')
    parser.add_argument('--dist_per_frame', type=int, default=40, help='Minimum distance(in ms) between per frame')
    parser.add_argument('--top_crop', type=int, default=0, help='Pixel cropped from the Top')
    parser.add_argument('--bottom_crop', type=int, default=-1, help='Pixel cropped from the Bottom')
    parser.add_argument('--left_crop', type=int, default=0, help='Pixel cropped from the Left')
    parser.add_argument('--right_crop', type=int, default=-1, help='Pixel cropped from the Right')
    parser.add_argument('--method',
                        type=str, 
                        default='NONE', 
                        help='Methods to be used for detecting blur in the frame. Choose between [NONE, TENANGRAD, LAPLACIAN, WAVELET]'
                        )
    parser.add_argument('--threshold', 
                        type=float, 
                        default=0, 
                        help='threshold value for identifying frame of some blurness value based on the method used')

    # parse the command line arguments
    args = parser.parse_args()

    getFrame(inputFile = args.input_file,
             outputDir = args.output_dir, 
             manual = args.manual,
             START = args.start, 
             END = args.end, 
             ms_per_frame = args.dist_per_frame, 
             TOP_CROP = args.top_crop,
             BOTTOM_CROP = args.bottom_crop,
             LEFT_CROP = args.left_crop,
             RIGHT_CROP = args.right_crop,
             METHOD = args.method,
             THRESH = args.threshold
             )