import shutil
from pathlib import Path
import argparse

def collect_frames(input_path, frame_number, frame_range, output_path):
    # Convert inputs to Path objects for cross-platform compatibility
    src_dir = Path(input_path)
    dst_dir = Path(output_path)
    
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
    parser = argparse.ArgumentParser(
        description="Collect surrounding frames from a camera directory.",
        epilog="""Example:
  uv run collect_surrounding_frames.py -i ./frames -n 50 -r 10 -o ./surrounding_frames
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-i", "--input", required=True, help="Path to the input directory containing images")
    parser.add_argument("-o", "--output", required=True, help="Path to the destination folder")
    parser.add_argument("-n", "--number", type=int, required=True, help="Target center frame number")
    parser.add_argument("-r", "--range", type=int, default=10, help="Range of frames to collect (default: 10)")

    args = parser.parse_args()

    # 実行部分
    collect_frames(args.input, args.number, args.range, args.output)

if __name__ == "__main__":
    main()