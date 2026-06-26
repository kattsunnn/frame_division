import ffmpeg
from pathlib import Path

def divide_into_frames(video_path, output_dir, start_time=None, duration=None):
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        output_pattern = output_dir / '%04d.jpg'
        
        input_opts = {}
        if start_time is not None:
            input_opts['ss'] = start_time
        if duration is not None:
            input_opts['t'] = duration

        stream = ffmpeg.input(str(video_path), **input_opts)
        stream = ffmpeg.output(stream, str(output_pattern), **{
                    'qscale:v': 2,       # 高画質
                    'start_number': 0,   # ここで 0 始まりを指定（デフォルトは1）
                    'vsync': '0'         # ネイティブFPSを維持
                })
        ffmpeg.run(stream)
        print(f"完了しました: {output_dir.resolve()}")
        
    except ffmpeg.Error as e:
            print("エラーが発生しました")
            if e.stderr:
                print(e.stderr.decode())

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Divide a video into high-quality image frames.",
        epilog="""Example:
  uv run divide_into_frames.py -i input.mp4 -o ./frames -d 10 -s 00:01:23
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input video file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory to save frames")
    parser.add_argument("-d", "--duration", help="Duration to extract (in seconds or timestamp) (default: until the end of the video)")
    parser.add_argument("-s", "--start", help="Start time to extract (in seconds or timestamp) (default: start from the beginning)")

    args = parser.parse_args()

    divide_into_frames(
        video_path=args.input, 
        output_dir=args.output, 
        start_time=args.start, 
        duration=args.duration
    )