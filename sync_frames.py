import os
from pathlib import Path
import argparse

def sync_frames(target_dir, sync_start_index):
    target_path = Path(target_dir)
    
    files = sorted(target_path.glob('*.jpg'))

    if not files:
        print("画像ファイルが見つかりませんでした。")
        return

    processed_count = 0
    deleted_count = 0

    for file_path in files:
        try:
            current_num = int(file_path.stem)

            if current_num < sync_start_index:
                file_path.unlink()
                deleted_count += 1

            else:
                # 同期点以降 -> リネーム (0始まりにシフト)
                new_num = int(current_num - sync_start_index)
                
                # 新しいファイル名を作成 (例: f"{0:05d}.jpg" -> "00000.jpg")
                new_name = f"{new_num:04d}{file_path.suffix}"
                new_path = target_path / new_name

                # 自分自身と同じ名前でなければリネーム実行
                if file_path != new_path:
                    file_path.rename(new_path)
                
                processed_count += 1

        except ValueError:
            print(f"スキップ (数値ファイル名ではありません): {file_path.name}")
            continue

    print("-" * 30)
    print(f"完了しました。")
    print(f"削除した枚数: {deleted_count} 枚")
    print(f"リネーム後の総枚数: {processed_count} 枚")

if __name__ == '__main__':
    
    import sys

    target_dir = sys.argv[1]
    sync_start_index = float(sys.argv[2])


    sync_frames(target_dir, sync_start_index)
    