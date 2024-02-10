import cv2
import os

video = cv2.VideoCapture('line_data3.avi')

frame_count = 0
image_counter = 0

# Get the directory of the currently running script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Create a directory to save images if it doesn't exist
output_directory = os.path.join(current_directory, 'video_images')
os.makedirs(output_directory, exist_ok=True)

# Path to image counter file
image_counter_file = os.path.join(output_directory, 'image_counter.txt')

# Check if image counter file exists, if not create one with starting value 0
if not os.path.exists(image_counter_file):
    with open(image_counter_file, 'w') as f:
        f.write('0')

# Read the current image counter from the file
with open(image_counter_file, 'r') as f:
    image_counter = int(f.read())

while True:
    ret, frame = video.read()

    if not ret:
        break

    # Get the current frame count
    frame_count = int(video.get(cv2.CAP_PROP_POS_FRAMES))

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the current position (in seconds) of the video file
    current_position_sec = video.get(cv2.CAP_PROP_POS_MSEC) / 1000

    # Draw the current position and total duration of the video on the frame
    cv2.putText(frame, f"Time: {current_position_sec:.2f} sec / {total_frames / video.get(cv2.CAP_PROP_FPS):.2f} sec",
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show the video frame
    cv2.imshow('The video', frame)

    key = cv2.waitKey(15) & 0xFF

    if key == ord('s'):
        image_counter += 1
        frame_name = os.path.join(output_directory, f'img{image_counter}V.jpg')
        cv2.imwrite(frame_name, frame)

        # Update image counter file
        with open(image_counter_file, 'w') as f:
            f.write(str(image_counter))

        # Show a message to the user
        cv2.putText(frame, f"Image saved as img{image_counter}.jpg", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('The video', frame)
        cv2.waitKey(500)  # Show the message for 1 second

    elif key == ord('q'):  # Press 'q' to quit
        break

    elif key == ord('p'):  # Press 'p' to pause
        while True:
            key2 = cv2.waitKey(0) & 0xFF
            if key2 == ord('p'):
                break

video.release()
cv2.destroyAllWindows()
