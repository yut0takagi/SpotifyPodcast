import subprocess
from pydub import AudioSegment
from pathlib import Path

# ディレクトリ定義
base_dir = Path(__file__).resolve().parent.parent
generated_data_dir = base_dir / "generated_data"
generated_episodes_dir = base_dir / "generated_episodes"
intro_path = base_dir / "src" / "intro.mp3"
outro_path = base_dir / "src" / "outro.mp3"

# 出力先ディレクトリがなければ作成
generated_episodes_dir.mkdir(exist_ok=True)

# ステージングされた.wavファイルを取得
def get_staged_wav_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        stdout=subprocess.PIPE,
        text=True
    )
    staged_files = result.stdout.strip().split("\n")
    return [Path(f) for f in staged_files if f.endswith(".wav") and f.startswith("generated_data/")]

# 音声ファイルの結合処理
def combine_audio(input_path: Path, output_path: Path):
    intro = AudioSegment.from_mp3(intro_path)
    outro = AudioSegment.from_mp3(outro_path)
    main = AudioSegment.from_wav(input_path)

    final = intro + main + outro
    final.export(output_path, format="wav")
    print(f"✅ 出力: {output_path.name}")

# メイン処理
def main():
    staged_wavs = get_staged_wav_files()

    if not staged_wavs:
        print("⚠️ ステージングされたWAVファイルが見つかりません。")
        return

    for input_wav in staged_wavs:
        output_wav = generated_episodes_dir / input_wav.name
        combine_audio(input_wav, output_wav)

if __name__ == "__main__":
    main()