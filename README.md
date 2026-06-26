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
uv run divide_into_frames.py <動画パス> <出力フォルダ> <切り出し長さ(秒)> <開始時刻>
```

#### 引数
- `動画パス`: 処理対象の動画ファイルパス
- `出力フォルダ`: 切り出した画像を保存するフォルダ（存在しない場合は自動作成されます）
- `切り出し長さ(秒)`: 切り出す秒数（例: `10`）
- `開始時刻`: 切り出しを開始するタイムスタンプ（例: `00:01:23` や秒数 `83`）

#### 実行例
```bash
uv run divide_into_frames.py input.mp4 ./frames 10 00:01:23
```

---

### 2. フレーム同期の基準合わせ (`sync_frames.py`)
複数カメラ等で切り出した画像群に対して、特定の同期基準フレーム番号（インデックス）を指定し、それより前の画像を削除し、以降の画像を `0000.jpg` から始まる連番にリネーム（シフト）して同期を合わせます。

#### 使い方
```bash
uv run sync_frames.py <対象フォルダ> <同期開始インデックス>
```

#### 引数
- `対象フォルダ`: 数値ファイル名（例: `0005.jpg`）の画像が含まれるフォルダ
- `同期開始インデックス`: 同期点とするフレーム番号（これ未満の画像は削除され、この画像が `0000.jpg` になります）

#### 実行例
```bash
uv run sync_frames.py ./frames 5
# 0000.jpg 〜 0004.jpg を削除
# 0005.jpg -> 0000.jpg, 0006.jpg -> 0001.jpg ... のようにリネーム
```

---

### 3. 同期フレームの収集・集約 (`get_sync_frames.py`)
指定したルートフォルダ配下を再帰的に検索し、指定されたファイル名（例: `0050.jpg`）を持つすべてのファイルを集約フォルダにコピーします。ファイル名が競合しないよう、コピー時には「`元の親フォルダ名_ファイル名`」に自動リネームされます。

#### 使い方
```bash
uv run get_sync_frames.py <検索ルートフォルダ> <出力フォルダ> <対象ファイル名>
```

#### 引数
- `検索ルートフォルダ`: 検索を開始するルートディレクトリのパス
- `出力フォルダ`: コピー先となるフォルダ
- `対象ファイル名`: 検索するファイル名（例: `0050.jpg`）

#### 実行例
```bash
uv run get_sync_frames.py ./camera_data ./sync_results 0050.jpg
# コピー例: ./camera_data/cam_A/0050.jpg -> ./sync_results/cam_A_0050.jpg
```

---

### 4. 周辺フレームの収集 (`collect_surrounding_frames.py`)
特定のターゲットフレーム番号を中心に、前後指定した範囲の画像のみを別フォルダにコピーして収集します。

#### 使い方
```bash
uv run collect_surrounding_frames.py -i <カメラフォルダ> -n <ターゲットフレーム番号> -r <前後範囲> -d <出力フォルダ>
```

#### オプション引数
- `-i`, `--camera_path`: 画像が格納されているカメラフォルダ（必須）
- `-n`, `--frame_number`: 中心となるターゲットのフレーム番号（必須）
- `-r`, `--frame_range`: 収集する前後の範囲（デフォルト: `10`）
- `-d`, `--destination_path`: 保存先の出力フォルダ（必須）

#### 実行例
```bash
uv run collect_surrounding_frames.py -i ./frames -n 50 -r 10 -d ./surrounding_frames
# 0040.jpg から 0060.jpg までの画像が ./surrounding_frames にコピーされます
```

---

### 5. 連番画像から動画を生成 (`create_video_from_images.py`)
指定されたフォルダ内の `.jpg` 画像（名前順にソート）をつなぎ合わせて、動画（MP4形式）を生成します。

#### 使い方
```bash
uv run create_video_from_images.py -i <入力フォルダ> -o <出力動画パス> -f <FPS>
```

#### オプション引数
- `-i`, `--input`: 画像が格納されている入力フォルダ（必須）
- `-o`, `--output`: 生成する動画のファイルパス（必須）
- `-f`, `--fps`: 1秒あたりのフレーム数（デフォルト: `30`）

#### 実行例
```bash
uv run create_video_from_images.py -i ./frames -o ./output_video.mp4 -f 30
```
