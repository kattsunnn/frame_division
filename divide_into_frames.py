import ffmpeg
from pathlib import Path

def divide_into_frames(video_path, output_dir, start_time, duration):
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        output_pattern = output_dir / '%04d.jpg'
        stream = ffmpeg.input(str(video_path), ss=start_time, t=duration)
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
    import sys

    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    duration = sys.argv[3]
    start_time = sys.argv[4]

    # 修正箇所: 固定文字列ではなく、上の変数を入れる
    divide_into_frames(
        video_path=input_path, 
        output_dir=output_dir, 
        start_time=start_time, 
        duration=duration
    )