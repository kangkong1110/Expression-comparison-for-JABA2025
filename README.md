# Expression-comparison-for-JABA2025

## 概要（Overview）
このリポジトリは、OpenFaceを用いて抽出した顔のアクションユニットを比較し、コサイン類似度を計算・可視化するPythonスクリプトを含みます。学会発表「[発表タイトル]」（[学会名], [発表年月]）に関連しています。

## 特徴（Features）
- OpenFaceによる顔特徴量抽出の自動処理
- 2者間の表情類似度（コサイン類似度）の計算
- 類似度付きのフレーム画像出力（PILで画像合成）
- CSVによる類似度出力と統計処理の準備

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
   - [OpenFace Releases](https://github.com/TadasBaltrusaitis/OpenFace/releases) から `OpenFace_2.2.0_win_x64.zip` をダウンロードし、任意の場所に解凍してください  
     ※バイナリ版（.zip）を選んでください（ソースコード版ではありません）
   - OpenFace の公式セットアップガイドも参照すると安心です：  
     [OpenFace - Windows Installation](https://github.com/TadasBaltrusaitis/OpenFace/wiki/Windows-Installation)
   - **Visual C++ 2017 再頒布可能パッケージ**をインストールしてください（これがないと `.exe` が起動しません）  
     ダウンロード先：[Microsoft Visual C++ 再頒布可能パッケージ](https://visualstudio.microsoft.com/ja/downloads/)
   - **モデルファイルをダウンロード**してください：  
     解凍した OpenFace フォルダ内にある `download_models.ps1` を右クリック → 「PowerShellで実行」  
     これにより、必要な学習済みモデルファイルが `model/` 以下にダウンロードされます
   - 最後に、`FeatureExtraction.exe` のフルパスを確認して控えてください  
     例：`C:\Tools\OpenFace_2.2.0_win_x64\FeatureExtraction.exe`

3. **このリポジトリをクローン**
以下のコマンドをターミナルまたはコマンドプロンプトに入力して、このリポジトリをローカルにクローンしてください：
   ```bash
   git clone https://github.com/kangkong1110/Expression-comparison-for-JABA2025.git
   ```
   
4. **必要なPythonライブラリをインストール**
   ```bash
   cd Expression-comparison-for-JABA2025
   pip install -r requirements.txt
   
5. **CalcCosSimiVideos.py 内の以下の行を、自分の環境に合わせて編集**
   ```bash
   feature_exe = r"C:\Tools\OpenFace_2.2.0_win_x64\FeatureExtraction.exe"
   
6. **スクリプトを実行**
   ```bash
   CalcCosSimiVideos.py

## 使い方（Usage）
```bash
CalcCosSimiVideos.py
```

実行すると、コマンドプロンプト上で以下のように動画ファイルのパスを入力するよう求められます（例: "C:\Users\yourname\sample.mp4"）。引用符付きでそれぞれ入力してください。
※エクスプローラでファイルを右クリック → 「パスのコピー」でコピペできます。
```bash
見本動画のパスを入力してください：
比較動画のパスを入力してください：
```

**出力ファイル：**
- `combined_frames`：類似度付きフレーム画像
- `output.mp4`：類似度を記載した動画
- `summary.csv`：コサイン類似度のcsv
- 見本動画及び比較動画を分割したフレーム(動画名と同名フォルダに格納)

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

