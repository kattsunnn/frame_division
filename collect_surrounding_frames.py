import shutil
from pathlib import Path
import argparse

def collect_frames(camera_path, frame_number, frame_range, destination_path):
    # Convert inputs to Path objects for cross-platform compatibility
    src_dir = Path(camera_path)
    dst_dir = Path(destination_path)
    
    center_frame = int(frame_number)
    offset = int(frame_range)
    
    # Ensure the destination directory exists
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Source: {src_dir}")
    print(f"Destination: {dst_dir}")

    collected_count = 0
    
    # Iterate through the calculated range
    for i in range(center_frame - offset, center_frame + offset + 1):
        # Format the number to 4 digits (e.g., 0005.jpg)
        filename = f"{i:04d}.jpg"
        source_file = src_dir / filename
        
        if source_file.exists():
            shutil.copy(source_file, dst_dir / filename)
            print(f"Copied: {filename}")
            collected_count += 1
        else:
            print(f"File not found: {filename}")

    print(f"\nTask complete. {collected_count} frames saved to {dst_dir}")

def main():
    parser = argparse.ArgumentParser(description="Collect surrounding frames")
    
    parser.add_argument("-i", "--camera_path", help="Path to the camera", required=True)
    parser.add_argument("-n", "--frame_number", type=int, help="Target frame number", required=True)
    parser.add_argument("-r", "--frame_range", type=int, help="Range of frames to collect", default=10)
    parser.add_argument("-d", "--destination_path", help="Destination folder", required=True)

    args = parser.parse_args()

    # 実行部分
    collect_frames(args.camera_path, args.frame_number, args.frame_range, args.destination_path)

if __name__ == "__main__":
    main()