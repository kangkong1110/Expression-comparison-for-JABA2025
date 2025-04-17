#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
撮影した動画とそれを基にしたディープフェイク映像の表情を比較するために作成したコード。撮影した動画(見本動画)を左側、ディープフェイク映像を左側に置き、真ん中にコサイン類似度を色付きで表示する。
ffmpegのパスをあらかじめ通しておくこと、openfaceをインストールしてFeatureExtraction.exeの位置を把握しておくこと。
実行するとカレントディレクトリに、
・見本動画の画像を格納したフォルダ、
・比較動画の画像を格納したフォルダ、
・openfaceの結果を格納したprocessedフォルダ、
・フレームごとのコサイン類似度を書き込んだsummary.csv、
・コサイン類似度を書いた字幕sim.ass
・類似度付き比較動画output.mp4
が出力される。
実行中、一時的にtmp_hstack.mp4が生成されているが、最後まで処理が進むと自動で削除される。


OpenFace × ffmpeg 比較動画パイプライン
----------------------------------------------------
1. 動画 → 連番 JPEG 抽出
2. OpenFace FeatureExtraction
3. 行ごとの L2 正規化でコサイン類似度を計算
4. 左右フレームを hstack（tmp_hstack.mp4）
5. ASS 字幕で毎フレーム数値描画 → output.mp4
6. summary.csv・sim.ass を保存
"""

# ── 動画・字幕パラメータ ────────────────────────────────
FPS         = 25
FONT_SIZE   = 256
MARGIN_V    = 50
FONT_FILE   = r"C:/Windows/Fonts/arial.ttf"   # 任意の TTF
# ─────────────────────────────────────────────

from pathlib import Path
import argparse, subprocess, numpy as np, pandas as pd

AU_COLS = [
    " AU01_r"," AU02_r"," AU04_r"," AU05_r"," AU06_r",
    " AU07_r"," AU09_r"," AU10_r"," AU12_r"," AU14_r",
    " AU15_r"," AU17_r"," AU20_r"," AU23_r"," AU25_r",
    " AU26_r"," AU45_r",
]

# ---------- 共通ヘルパ ------------------------------------------------------
def sh(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)

def extract(src: Path, dst: Path):
    dst.mkdir(exist_ok=True)
    sh(["ffmpeg","-y","-i",str(src),"-q:v","2",str(dst/"%05d.jpg")])

def openface(frames: Path, exe: Path, gpu: int):
    cmd=[str(exe),"-fdir",str(frames),"-out_dir","processed"]
    if gpu>=0: cmd+=["-gpu",str(gpu)]
    sh(cmd)

def cosine(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """行ベースのコサイン類似度 (長さ = フレーム数)"""
    num = (a * b).sum(axis=1)                # ① 各行の内積
    na  = np.linalg.norm(a, axis=1)          # ② 各行の ‖a_i‖₂
    nb  = np.linalg.norm(b, axis=1)          # ③ 各行の ‖b_i‖₂
    den = na * nb                            # ④ 要素ごとの積
    return np.divide(num, den, out=np.zeros_like(num), where=den != 0)

# ---------- ASS 字幕生成 ----------------------------------------------------
ASS_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BorderStyle, Alignment, MarginL, MarginR, MarginV
Style: S,Arial,{FONT_SIZE},&H00FFFFFF,&H00000000,1,2,0,0,{MARGIN_V}

[Events]
Format: Layer, Start, End, Style, Text
"""

def ass_color(sim: float)->str:
    return ("&HFF0000&" if sim>=.96 else "&H00FF00&" if sim>=.91 else
            "&H00FFFF&" if sim>=.86 else "&H007FFF&" if sim>=.81 else "&H0000FF&")

def tc(frame:int)->str:          # hh:mm:ss.cc (centisecond)
    cs=int(frame*100/FPS); hh=cs//360000; mm=(cs%360000)//6000
    ss=(cs%6000)//100; cc=cs%100
    return f"{hh}:{mm:02d}:{ss:02d}.{cc:02d}"

def make_ass(sims: np.ndarray, out: Path):
    events=[f"Dialogue: 0,{tc(i)},{tc(i+1)},S,{{\\c{ass_color(s)}}}{s:.2f}"
            for i,s in enumerate(sims)]
    out.write_text(ASS_HEADER + "\n".join(events), encoding="utf-8")

# ---------- ffmpeg 合成 -----------------------------------------------------
def hstack(ldir: Path, rdir: Path, tmp: Path):
    sh([
        "ffmpeg","-y",
        "-framerate",str(FPS),"-i",str(ldir/"%05d.jpg"),
        "-framerate",str(FPS),"-i",str(rdir/"%05d.jpg"),
        "-filter_complex","[0:v][1:v]hstack=inputs=2",
        "-c:v","libx264","-pix_fmt","yuv420p",str(tmp)
    ])

def overlay(src: Path, ass: Path, dst: Path):
    fonts_dir=Path(FONT_FILE).parent.as_posix().replace("C:/","C\\:/")  # C: → C\:/ エスケープ
    sh([
        "ffmpeg","-y","-i",str(src),
        "-vf",f"subtitles={ass.as_posix()}:fontsdir='{fonts_dir}'",
        "-c:v","libx264","-pix_fmt","yuv420p",str(dst)
    ])

# ---------- メイン ----------------------------------------------------------
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model_video",required=True)
    ap.add_argument("--comp_video", required=True)
    ap.add_argument("--openface_exe",required=True)
    ap.add_argument("--gpu",type=int,default=-1)
    args=ap.parse_args()

    mv, cv = Path(args.model_video), Path(args.comp_video)
    md, cd = mv.with_suffix(""), cv.with_suffix("")

    extract(mv, md); extract(cv, cd)
    openface(md, Path(args.openface_exe), args.gpu)
    openface(cd, Path(args.openface_exe), args.gpu)

    dfm=pd.read_csv(Path("processed", md.name+".csv"), usecols=AU_COLS)
    dfc=pd.read_csv(Path("processed", cd.name+".csv"), usecols=AU_COLS)
    n=min(len(dfm),len(dfc))
    sims=cosine(dfm.iloc[:n].to_numpy(np.float32), dfc.iloc[:n].to_numpy(np.float32))
    pd.DataFrame({"Frame":range(1,n+1),"CosineSimilarity":sims}).to_csv("summary.csv", index=False)

    ass=Path("sim.ass"); tmp=Path("tmp_hstack.mp4")
    make_ass(sims, ass)
    hstack(md, cd, tmp)
    overlay(tmp, ass, Path("output.mp4"))
    tmp.unlink(missing_ok=True)

    print("✔ output.mp4 / summary.csv / sim.ass を生成しました")

if __name__=="__main__":
    main()
