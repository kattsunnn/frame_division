# Frame Division & Sync Tools

動画からのフレーム（連番画像）切り出し、複数カメラ映像のフレーム同期調整、特定フレーム周辺の収集、および連番画像からの動画生成を行うためのPythonスクリプト群です。

## 目次

1. [セットアップ](#セットアップ)
2. [スクリプト一覧と使い方](#スクリプト一覧と使い方)
   - [1. 動画からフレーム切り出し (`divide_into_frames.py`)](#1-動画からフレーム切り出し-divide_into_framespy)
   - [2. フレーム同期の基準合わせ (`sync_frames.py`)](#2-フレーム同期の基準合わせ-sync_framespy)
   - [3. 同期フレームの収集・集約 (`get_sync_frames.py`)](#3-同期フレームの収集集約-get_sync_framespy)
   - [4. 周辺フレームの収集 (`collect_surrounding_frames.py`)](#4-周辺フレームの収集-collect_surrounding_framespy)
   - [5. 連番画像から動画を生成 (`create_video_from_images.py`)](#5-連番画像から動画を生成-create_video_from_imagespy)

---

## セットアップ

本プロジェクトは `uv` を使用して依存関係を管理しています。

### 1. 依存ライブラリのインストール
プロジェクトのルートディレクトリで以下のコマンドを実行するだけで、自動的に仮想環境の構築と依存関係のインストールが行われます。
```bash
uv sync
```

### 2. ffmpegのインストール（`divide_into_frames.py` を使用する場合のみ）
`divide_into_frames.py` はシステムにインストールされた `ffmpeg` コマンドを呼び出します。お使いのOS環境に応じて `ffmpeg` をインストールし、パス（PATH）を通しておいてください。

---

## スクリプト一覧と使い方

### 1. 動画からフレーム切り出し (`divide_into_frames.py`)

動画ファイルから指定した開始時間・長さの区間を切り出し、ネイティブFPSを維持した高画質連番画像（`0000.jpg`〜）として出力します。

#### 使い方
```bash
uv run divide_into_frames.py -i <動画パス> -o <出力フォルダ> [-d <切り出し長さ(秒)>] [-s <開始時刻>]
```

#### オプション引数
- `-i`, `--input`: 処理対象 of 動画ファイルパス（必須）
- `-o`, `--output`: 切り出した画像を保存するフォルダ（存在しない場合は自動作成されます）（必須）
- `-d`, `--duration`: 切り出す秒数またはタイムスタンプ（任意、指定がない場合は動画の最後まで切り出します）
- `-s`, `--start`: 切り出しを開始するタイムスタンプまたは秒数（任意、指定がない場合は動画の最初から切り出します）

#### 実行例
```bash
uv run divide_into_frames.py -i input.mp4 -o ./frames -d 10 -s 00:01:23
```

---

### 2. フレーム同期の基準合わせ (`sync_frames.py`)

複数カメラ等で切り出した画像群に対して、特定の同期基準フレーム番号（インデックス）を指定し、それより前の画像を削除し、以降の画像を `0000.jpg` から始まる連番にリネーム（シフト）して同期を合わせます。

#### 使い方
```bash
uv run sync_frames.py -i <対象フォルダ> -n <同期開始インデックス>
```

#### オプション引数
- `-i`, `--input`: 数値ファイル名（例: `0005.jpg`）の画像が含まれるフォルダ（必須）
- `-n`, `--index`: 同期点とするフレーム番号（これ未満の画像は削除され、この画像が `0000.jpg` になります）（必須）

#### 実行例
```bash
uv run sync_frames.py -i ./frames -n 5
# 0000.jpg 〜 0004.jpg を削除
# 0005.jpg -> 0000.jpg, 0006.jpg -> 0001.jpg ... のようにリネーム
```

---

### 3. 同期フレームの収集・集約 (`get_sync_frames.py`)

指定したルートフォルダ配下を再帰的に検索し、指定されたファイル名（例: `0050.jpg`）を持つすべてのファイルを集約フォルダにコピーします。ファイル名が競合しないよう、コピー時には「`元の親フォルダ名_ファイル名`」に自動リネームされます。

#### 使い方
```bash
uv run get_sync_frames.py -i <検索ルートフォルダ> -o <出力フォルダ> -f <対象ファイル名>
```

#### オプション引数
- `-i`, `--input`: 検索を開始するルートディレクトリのパス（必須）
- `-o`, `--output`: コピー先となるフォルダ（必須）
- `-f`, `--filename`: 検索するファイル名（例: `0050.jpg`）（必須）

#### 実行例
```bash
uv run get_sync_frames.py -i ./camera_data -o ./sync_results -f 0050.jpg
# コピー例: ./camera_data/cam_A/0050.jpg -> ./sync_results/cam_A_0050.jpg
```

---

### 4. 周辺フレームの収集 (`collect_surrounding_frames.py`)

特定のターゲットフレーム番号を中心に、前後指定した範囲の画像のみを別フォルダにコピーして収集します。

#### 使い方
```bash
uv run collect_surrounding_frames.py -i <入力フォルダ> -o <出力フォルダ> -n <ターゲットフレーム番号> [-r <前後範囲>]
```

#### オプション引数
- `-i`, `--input`: 画像が格納されている入力フォルダのパス（必須）
- `-o`, `--output`: 保存先の出力フォルダのパス（必須）
- `-n`, `--number`: 中心となるターゲットのフレーム番号（必須）
- `-r`, `--range`: 収集する前後の範囲（任意、デフォルト: `10`）

#### 実行例
```bash
uv run collect_surrounding_frames.py -i ./frames -o ./surrounding_frames -n 50 -r 10
# 0040.jpg から 0060.jpg までの画像が ./surrounding_frames にコピーされます
```

---

### 5. 連番画像から動画を生成 (`create_video_from_images.py`)

指定されたフォルダ内の `.jpg` 画像（名前順にソート）をつなぎ合わせて、動画（MP4形式）を生成します。

#### 使い方
```bash
uv run create_video_from_images.py -i <入力フォルダ> -o <出力動画パス> [-f <FPS>]
```

#### オプション引数
- `-i`, `--input`: 画像が格納されている入力フォルダのパス（必須）
- `-o`, `--output`: 生成する動画のファイルパス（必須）
- `-f`, `--fps`: 1秒あたりのフレーム数（任意、デフォルト: `30`）

#### 実行例
```bash
uv run create_video_from_images.py -i ./frames -o ./output_video.mp4 -f 30
```
