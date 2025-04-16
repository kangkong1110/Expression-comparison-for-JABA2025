# Expression-comparison-for-JABA2025

## 概要（Overview）
このリポジトリは、OpenFaceを用いて抽出した顔のアクションユニットを比較し、コサイン類似度を計算・可視化するPythonスクリプトを含みます。学会発表「[発表タイトル]」（[学会名], [発表年月]）に関連しています。

## 特徴（Features）
- OpenFaceによる顔特徴量抽出の自動処理
- 2者間の表情類似度（コサイン類似度）の計算
- 類似度付きのフレーム画像出力（PILで画像合成）
- CSVによる類似度出力と統計処理の準備

## 必要環境（Requirements）
- Python 3.10.9 python3の以前のバージョンでも動く可能性はありますが、動作確認はしていません。
- 必要なライブラリは `requirements.txt` に記載されています
- OpenFace（https://github.com/TadasBaltrusaitis/OpenFace）
  - 本リポジトリは OpenFace の `FeatureExtraction.exe` を外部から呼び出します
  - 利用には別途 OpenFace のダウンロードとライセンス確認が必要です

## セットアップ手順（Installation）

1. ffmpegをインストールし、パスを環境変数に追加
2. OpenFace をインストールし、`FeatureExtraction.exe` のパスを確認
3. このリポジトリをクローン
4. ライブラリをインストール：
   ```bash
   pip install -r requirements.txt
5. CalcCosSimiVideos.py内の     feature_exe = r"C:\Users\yourname\OpenFace_2.2.0_win_x64\FeatureExtraction.exe"　にセットアップ手順2で確認したパスを入力する
6. コマンドプロンプト上で実行する

## 使い方（Usage）
`python CalcCosSimiVideos.py`

コマンドプロンプト上で以下の表示が出てくるため、動画のパスを引用付きで入力する("C:\Users\yourname\sample.mp4")。エクスプローラ上でパスのコピーをしてください。
見本動画のパスを入力してください：
比較動画のパスを入力してください：

出力：
類似度付きフレーム画像(combined_frames)
類似度を記載した動画(output.mp4)
コサイン類似度のcsv(summary.csv)
見本動画及び比較動画を分割したフレーム

## 使用ライブラリとライセンス

本プロジェクトでは、顔特徴量抽出にOpenFaceの「Feature Extraction.exe」を使用しています。
OpenFaceは、カーネギーメロン大学が提供する非商用研究目的限定のライセンスで配布されています。
詳細は、以下のリンクをご参照ください：
https://github.com/TadasBaltrusaitis/OpenFace/blob/master/OpenFace-license.txt

## 引用(Citation)
OpenFaceの使用に際しては、以下の論文を引用する必要があります：

- Tadas Baltrušaitis, Amir Zadeh, Yao Chong Lim, and Louis-Philippe Morency,
  "OpenFace 2.0: Facial Behavior Analysis Toolkit",
  IEEE International Conference on Automatic Face and Gesture Recognition, 2018.

