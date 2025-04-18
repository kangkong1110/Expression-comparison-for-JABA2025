# Expression-comparison-for-JABA2025

## 概要（Overview）
このリポジトリは、**2者間の顔表情の類似度を動画上で可視化**するツールです。  
OpenFaceを用いて抽出した顔のアクションユニット（表情筋の動き）をもとに、各フレームの類似度（コサイン類似度）を計算し、比較動画の下部に数値として表示します。
ディープフェイクで作成した動画の類似度を定量的に評価する目的で作成しました。

本ツールは、**行動分析学会第43回年次大会**でのポスター発表  
「[発表タイトル]」に関連して開発されたものです。  

## 特徴（Features）
- OpenFaceによる17種類のアクションユニット抽出
- 見本動画と比較動画の**コサイン類似度をフレーム単位で計算**
- 類似度を数値として**色付き字幕(青～赤)で可視化**
- 類似度をcsvに出力

## 必要環境（Requirements）
- Python 3.10.9  
  ※それ以前のバージョンでも動作する可能性がありますが、確認はしていません
- Windows環境
  ※macOS や Linux ではフォント読み込みなど一部動作しない可能性があります
- 必要なPythonライブラリは `requirements.txt` に記載
- OpenFace (https://github.com/TadasBaltrusaitis/OpenFace)  
  - 本リポジトリは OpenFace の `FeatureExtraction.exe` を外部から呼び出します  
  - 利用には別途 OpenFace のダウンロードとライセンス確認が必要です
- ffmpeg (http://ffmpeg.org/)
## セットアップ手順（Installation）

1. **ffmpeg をインストール**
   - [公式サイト](https://ffmpeg.org/download.html) から Windows 版をダウンロード（例: `ffmpeg-release-essentials.zip`）
   - 解凍後、`bin` フォルダ（例: `C:\ffmpeg\bin`）のパスを **環境変数 Path に追加**
     - 方法: 「スタート」→「環境変数の編集」→「Path」→ `C:\ffmpeg\bin` を追加

2. **OpenFace をセットアップ**
   - [OpenFace Releases](https://github.com/TadasBaltrusaitis/OpenFace/releases) から**OpenFace_2.2.0_win_x64.zip**をダウンロードし、任意の場所に解凍してください  
     ※バイナリ版（.zip）を選んでください（ソースコード版ではありません）。
     OpenFace の公式セットアップガイドも参照すると分かりやすいです： 
     [OpenFace - Windows Installation](https://github.com/TadasBaltrusaitis/OpenFace/wiki/Windows-Installation)
   - **Visual C++ 2017 再頒布可能パッケージ**をインストールしてください（これがないと `.exe` が起動しません）  
     ダウンロード先：[Microsoft Visual C++ 再頒布可能パッケージ](https://visualstudio.microsoft.com/ja/downloads/)
   - **モデルファイルをダウンロード**してください：  
     解凍した OpenFace フォルダ内にある `download_models.ps1` を右クリック → 「PowerShellで実行」  
     これにより、必要な学習済みモデルファイルが `model/` 以下にダウンロードされます
   - 最後に、`FeatureExtraction.exe` のフルパスを確認して控えてください。
     例：`C:\Tools\OpenFace_2.2.0_win_x64\FeatureExtraction.exe`

3. **このリポジトリをクローン**
以下のコマンドをターミナルまたはコマンドプロンプトに入力して、このリポジトリをローカルにクローンしてください：
   ```bash
   git clone https://github.com/kangkong1110/Expression-comparison-for-JABA2025.git
   ```
   
4. **必要なPythonライブラリをインストール**
   ```bash
   pip install numpy pandas
   
## 使い方（Usage）
コマンドプロンプトで、パスを変更した以下のコマンドを入力してください。
```bash
python CalcCosSimiVideos_fast.py ^
  --model_video "path/to/originalvideo.mp4" ^
  --comp_video  "path/to/deepfake.mp4" ^
  --openface_exe "path/to/OpenFace/FeatureExtraction.exe"
```

**引数の説明**
- `--model_video`: 基準となる見本動画(出力動画の左側に表示されます)
- `--comp_video`: 比較対象の動画(出力動画の右側に表示されます)
- `--openface_exe`: OpenFaceのFeatureExtraction.exeのフルパス

**出力ファイル：**
- 見本動画及び比較動画を分割したフレーム(5桁の連番.jpg。動画名と同名フォルダに格納)
- `processed`：openfaceによる処理結果ファイル
- `summary.csv`：各フレームのコサイン類似度一覧
- `sim.ass`：コサイン類似度を記載した字幕ファイル
- `output.mp4`：類似度つき比較動画

## 使用ライブラリとライセンス

本プロジェクトでは、顔特徴量抽出にOpenFaceの「Feature Extraction.exe」を使用しています。
OpenFaceを外部から呼び出しており、本リポジトリにはOpenFace本体は含まれていません。
OpenFaceは、カーネギーメロン大学が提供する非商用研究目的限定のライセンスで配布されています。

詳細なライセンスについては、以下をご参照ください：
https://github.com/TadasBaltrusaitis/OpenFace/blob/master/OpenFace-license.txt

## 引用(Citation)
OpenFaceの使用に際しては、以下の論文を引用する必要があります：

- Tadas Baltrušaitis, Amir Zadeh, Yao Chong Lim, and Louis-Philippe Morency,
  "OpenFace 2.0: Facial Behavior Analysis Toolkit",
  IEEE International Conference on Automatic Face and Gesture Recognition, 2018.

