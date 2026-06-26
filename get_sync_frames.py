import shutil
import argparse
from pathlib import Path

def get_sync_frames(root_dir, target_filename, output_dir):
    
    root_path = Path(root_dir)
    output_path = Path(output_dir)
    
    output_path.mkdir(parents=True, exist_ok=True)

    found_files = list(root_path.rglob(target_filename))

    if not found_files:
        print(f"警告: '{target_filename}' は '{root_dir}' 内に見つかりませんでした。")
        return

    print(f"検索結果: {len(found_files)} 件のファイルが見つかりました。コピーを開始します...")

    copied_count = 0
    
    for src_path in found_files:
        try:
            new_filename = f"{src_path.parent.name}_{src_path.name}"
            dst_path = output_path / new_filename
            counter = 1
            while dst_path.exists():
                stem = Path(new_filename).stem
                suffix = Path(new_filename).suffix
                dst_path = output_path / f"{stem}_{counter}{suffix}"
                counter += 1

            shutil.copy2(src_path, dst_path)
            
            print(f"コピー完了: {src_path.parent.name}/{src_path.name} -> {dst_path.name}")
            copied_count += 1

        except Exception as e:
            print(f"エラー発生 ({src_path}): {e}")

    print("-" * 30)
    print(f"処理完了: {copied_count} / {len(found_files)} ファイルをコピーしました。")
    print(f"出力先: {output_path.resolve()}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Recursively find and copy specific sync frames.",
        epilog="""Example:
  uv run get_sync_frames.py -i ./camera_data -o ./sync_results -f 0050.jpg
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the search root directory")
    parser.add_argument("-o", "--output", required=True, help="Path to the output destination directory")
    parser.add_argument("-f", "--filename", required=True, help="Target file name to search (e.g. 0050.jpg)")

    args = parser.parse_args()

    # 関数実行
    get_sync_frames(args.input, args.filename, args.output)