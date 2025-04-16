    """
    撮影した動画とそれを基にしたディープフェイク映像の表情を比較するために作成したコード。撮影した動画(見本動画)を左側、ディープフェイク映像を左側に置き、真ん中にコサイン類似度を色付きで表示する。
    ffmpegのパスをあらかじめ通しておくこと、所定の位置にopenfaceのFeatureExtraction.exeを配置すること。FeatureExtraction.exeの場所を揃えるより、コード書き換えた方が楽かも。
    実行すると
    ・カレントディレクトリに見本動画の画像を格納したフォルダ、
    ・比較動画の画像を格納したフォルダ、
    ・openfaceの結果を格納したprocessedフォルダ、
    ・それらを並べたcombined_framesフォルダ、
    ・結果を書き込んだsummary.csv、
    ・output_video
    が出力される。
    フレームを揃えるために、ffmpegで画像に分解してから単独人物用のopenfaceを実行している。
    """
import os
import subprocess
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

def extract_frames(video_path, output_dir):
    """
    ffmpegを使って動画を5桁連番（例:"00001.jpg"）の画像に変換する。
    """
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-q:v", "2",
        os.path.join(output_dir, "%05d.jpg")
    ]
    subprocess.run(cmd, check=True)

def run_openface(image_folder, feature_exe):
    """
    FeatureExtraction.exe を -fdir オプション付きで実行する
    """
    cmd = [
        feature_exe,
        "-fdir", image_folder
    ]
    subprocess.run(cmd, check=True)

def compute_cosine_similarity(vecA, vecB):
    """
    2つのベクトルのコサイン類似度を計算する
    """
    dot = np.dot(vecA, vecB)
    normA = np.linalg.norm(vecA)
    normB = np.linalg.norm(vecB)
    if normA == 0 or normB == 0:
        return 0.0
    return dot / (normA * normB)

def get_color(sim):
    """
    コサイン類似度に応じた文字色を返す
    """
    if sim >= 0.96:
        return "blue"
    elif sim >= 0.91:
        return "green"
    elif sim >= 0.86:
        return "yellow"
    elif sim >= 0.81:
        return "orange"
    else:
        return "red"

def combine_images_with_text(model_img_path, comp_img_path, output_path, sim_value, font_path=None):
    """
    見本動画と比較動画の画像を左右に結合し、
    画像の横中央かつ下部から1024pxの位置にフォントサイズ1024で
    コサイン類似度の値をオーバーレイして保存する。
    """
    # 画像を読み込み
    img1 = Image.open(model_img_path)
    img2 = Image.open(comp_img_path)
    
    # 高さが異なる場合、img2 を img1 の高さに合わせてリサイズ
    if img1.height != img2.height:
        img2 = img2.resize((img2.width, img1.height))
        
    total_width = img1.width + img2.width
    combined = Image.new("RGB", (total_width, img1.height))
    combined.paste(img1, (0, 0))
    combined.paste(img2, (img1.width, 0))
    
    draw = ImageDraw.Draw(combined)
    text = f"{sim_value:.2f}"
    
    try:
        if font_path:
            font = ImageFont.truetype(font_path, 1024)
        else:
            font = ImageFont.truetype("arial.ttf", 1024)
    except Exception as e:
        print("フォント読み込みに失敗しました。デフォルトフォントを使用します。", e)
        font = ImageFont.load_default()
    
    # textbbox でテキストのバウンディングボックスを取得
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (total_width - text_width) // 2
    y = max(img1.height - 1024, 0)
    color = get_color(sim_value)
    
    draw.text((x, y), text, fill=color, font=font)
    combined.save(output_path)

def create_video_from_frames(frames_folder, output_video, framerate=25):
    """
    ffmpegを使用して、指定フォルダ内の連番画像から動画を生成する。
    """
    cmd = [
        "ffmpeg",
        "-framerate", str(framerate),
        "-i", os.path.join(frames_folder, "%05d.jpg"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    subprocess.run(cmd, check=True)

def main():
    # 1. コマンドプロンプト上で見本動画と比較動画のパスを入力（引用符付き入力想定）
    model_video = input("見本動画のパスを入力してください: ").strip().strip('"')
    comp_video  = input("比較動画のパスを入力してください: ").strip().strip('"')
    
    # 2. 動画ファイルのベース名（拡張子除く）を取得し、それぞれの画像出力用フォルダを作成する
    model_name = os.path.splitext(os.path.basename(model_video))[0]
    comp_name  = os.path.splitext(os.path.basename(comp_video))[0]
    model_frames_dir = model_name
    comp_frames_dir  = comp_name
    os.makedirs(model_frames_dir, exist_ok=True)
    os.makedirs(comp_frames_dir, exist_ok=True)
    
    # 3. ffmpeg を使用して各動画をフレームごとの画像（5桁連番のJPEG）に変換する
    print("見本動画のフレーム抽出開始...")
    extract_frames(model_video, model_frames_dir)
    print("比較動画のフレーム抽出開始...")
    extract_frames(comp_video, comp_frames_dir)
    
    # 4. FeatureExtraction.exe を -fdir オプション付きで実行する
    feature_exe = r"C:\Users\yourname\OpenFace_2.2.0_win_x64\FeatureExtraction.exe"
    print("見本動画のOpenFace解析開始...")
    run_openface(model_frames_dir, feature_exe)
    print("比較動画のOpenFace解析開始...")
    run_openface(comp_frames_dir, feature_exe)
    
    # 5. カレントディレクトリ内の processed フォルダからCSVを読み込み、
    #    各行ごとにAU01_r～AU45_r の17次元データ（各カラムの直前に半角スペースあり）を取得する
    processed_dir = "processed"
    model_csv = os.path.join(processed_dir, model_name + ".csv")
    comp_csv  = os.path.join(processed_dir, comp_name + ".csv")
    
    print("CSV読み込み中…")
    df_model = pd.read_csv(model_csv)
    df_comp  = pd.read_csv(comp_csv)
    
    # CSV内の各AUのカラム名は先頭に半角スペースがある
    cols = [" AU01_r", " AU02_r", " AU04_r", " AU05_r", " AU06_r",
            " AU07_r", " AU09_r", " AU10_r", " AU12_r", " AU14_r",
            " AU15_r", " AU17_r", " AU20_r", " AU23_r", " AU25_r",
            " AU26_r", " AU45_r"]
    
    for col in cols:
        if col not in df_model.columns:
            raise KeyError(f"見本動画のCSVにカラム {col} が存在しません。")
        if col not in df_comp.columns:
            raise KeyError(f"比較動画のCSVにカラム {col} が存在しません。")
    
    vec_model = df_model[cols].to_numpy()
    vec_comp  = df_comp[cols].to_numpy()
    
    n_frames = min(vec_model.shape[0], vec_comp.shape[0])
    summary_list = []
    cosine_sim_list = []
    
    for i in range(n_frames):
        a = vec_model[i].astype(float)
        b = vec_comp[i].astype(float)
        sim = compute_cosine_similarity(a, b)
        sim = round(sim, 2)
        cosine_sim_list.append(sim)
        summary_list.append([i+1] + list(a) + list(b) + [sim])
    
    summary_columns = (["Frame"] +
                       [f"Model_{col.strip()}" for col in cols] +
                       [f"Comp_{col.strip()}" for col in cols] +
                       ["CosineSimilarity"])
    summary_df = pd.DataFrame(summary_list, columns=summary_columns)
    summary_csv_path = "summary.csv"
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"Summary CSVは {summary_csv_path} に保存されました。")
    
    # 6. 各フレームごとに、見本動画と比較動画の画像を左右に結合し、
    #    コサイン類似度をテキストオーバーレイした新たな画像を生成する（tqdmで進捗表示）
    combined_frames_dir = "combined_frames"
    os.makedirs(combined_frames_dir, exist_ok=True)
    
    print("各フレーム画像の結合＆テキスト描画開始…")
    for i in tqdm(range(n_frames), desc="画像合成中"):
        frame_num = i + 1
        filename = f"{frame_num:05d}.jpg"
        model_img_path = os.path.join(model_frames_dir, filename)
        comp_img_path  = os.path.join(comp_frames_dir, filename)
        output_img_path = os.path.join(combined_frames_dir, filename)
        sim_val = cosine_sim_list[i]
        combine_images_with_text(model_img_path, comp_img_path, output_img_path, sim_val)
    
    # 7. ffmpeg を使用して、結合画像から動画を生成し、カレントディレクトリに保存する
    output_video = "output.mp4"
    print("結合画像から動画生成中…")
    create_video_from_frames(combined_frames_dir, output_video, framerate=25)
    print(f"出力動画 {output_video} が作成されました。")
    
if __name__ == "__main__":
    main()
