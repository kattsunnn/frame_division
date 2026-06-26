import cv2
import os
from pathlib import Path
import argparse

def create_video_from_images(image_folder, output_path, fps=30):
    folder_path = Path(image_folder)
    # Get all .jpg files and sort them to ensure correct frame order
    images = sorted([img for img in os.listdir(folder_path) if img.endswith(".jpg")])
    
    if not images:
        print("No images found in the target folder.")
        return

    # Read the first image to get dimensions
    first_image_path = folder_path / images[0]
    frame = cv2.imread(str(first_image_path))
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    # 'mp4v' is a standard codec for .mp4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"Creating video at: {output_path}")
    for image in images:
        image_path = folder_path / image
        video.write(cv2.imread(str(image_path)))
    
    video.release()
    print("Video generation complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a video from a folder of images")
    
    parser.add_argument("-i", "--input", dest="input_folder", required=True, help="Path to input images")
    parser.add_argument("-o", "--output", dest="output_video_path", required=True, help="Path to output video")
    parser.add_argument("-f", "--fps", type=int, default=30, help="Frames per second (default: 30)")
    args = parser.parse_args()

    # 実行部分
    create_video_from_images(args.input_folder, args.output_video_path, args.fps)

# Example Execution:
# create_video_from_images("./output_folder", "./output_video.mp4")