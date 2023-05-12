# vid2frame

<h1>Get Frames from a Video</h1>

</hr>

<h2>Project Description</h2>
vid2frame uses Python script that provides two ways to extract frames from a video file. The first method involves determining the total number of frames in the video and looping through each frame to save it individually. The second method enables manual frame extraction by specifying the time interval between two frames and reading each subsequent frame. When manually extracting frame one may get blurred frame, this script includes multiple methods for selecting frames based on their level of blur, including Tenengrad, Laplacian, and wavelet-based methods. These methods use a threshold to determine whether a given frame is too blurry to be used for analysis. The script can be run either by importing the functions directly into a Python project or by using command line arguments to specify the input video, threshold, and output directory.


This script uses the popular OpenCV library for efficient video processing and is a useful tool for computer vision researchers and video enthusiasts. The output frames can be further analyzed for tasks like object detection, motion tracking, and more.

With vid2frame, extracting frames from a video has never been easier. Simply download the script and get started with your video processing tasks today!"
This repo helps captures frames from a Video. Instead of getting the available frame 


<h2>Run the script</h2>
There are two ways to run this script:

1. Importing the function
You can import the get_frames() function from the vid2frame module in your own Python code and use it as follows:

```
from getFrame import getFrame

# Define the input video file path
input_video = "path/to/video.mp4"

# Define the output directory path where frames will be saved
output_dir = "path/to/output_dir"

# Call the getFrames() function with the input arguments
getFrames(input_video, output_dir)
```

2. Using command-line arguments
You can also run the script from the command line using the following syntax:
```
python getFrame.py input_video output_dir [--manual] [--dist_per_frame DIST_PER_FRAME]
```
where input_video is the path to the input video file, output_dir is the path to the directory where the frames will be saved, --manual is an optional argument that specifies the second way to enables manual frame extraction, and --dist_per_frame is an optional argument that specifies the minimum time interval between two frames.

<strong>Full Argument list</strong>
```
usage: getFrame.py [-h] [--manual] [--start START] [--end END]
                   [--dist_per_frame DIST_PER_FRAME] [--top_crop TOP_CROP]
                   [--bottom_crop BOTTOM_CROP] [--left_crop LEFT_CROP]
                   [--right_crop RIGHT_CROP] [--method METHOD]
                   [--threshold THRESHOLD]
                   input_file output_dir

Get Desired Frame from a video

positional arguments:
  input_file            input video file path
  output_dir            output directory to store the frame

options:
  -h, --help            show this help message and exit
  --manual              Manually get frame
  --start START         Starting point(in ms) from which frame will be
                        acquired
  --end END             Ending point(in ms) till which frame will be acquired
  --dist_per_frame DIST_PER_FRAME
                        Minimum distance(in ms) between per frame
  --top_crop TOP_CROP   Pixel cropped from the Top
  --bottom_crop BOTTOM_CROP
                        Pixel cropped from the Bottom
  --left_crop LEFT_CROP
                        Pixel cropped from the Left
  --right_crop RIGHT_CROP
                        Pixel cropped from the Right
  --method METHOD       Methods to be used for detecting blur in the frame.
                        Choose between [NONE, TENANGRAD, LAPLACIAN, WAVELET]
  --threshold THRESHOLD
                        threshold value for identifying frame of some blurness
                        value based on the method used
```

<strong>Have include 'run.ipyb' notebook, where multiple examples are shown to extract frame from the videos present in the 'vid' directory and the results obtained is in the 'subject' directory</strong>

<h2>Some Results</h2>

<p><img alt="Image" title="icon" src="subject/I_100/frame_025.png" /></p>
<p><img alt="Image" title="icon" src="subject/I_100/frame_050.png" /></p>
<p><img alt="Image" title="icon" src="subject/I_100/frame_075.png" /></p>

