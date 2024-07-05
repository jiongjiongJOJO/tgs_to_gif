import gzip
import argparse
from rlottie_python import LottieAnimation


def convert_tgs_to_gif(input_path, output_file):
    with open(input_path, "rb") as f:
        json_lottie = gzip.decompress(f.read()).decode("utf-8")
        anim = LottieAnimation.from_data(json_lottie)
        anim.save_animation(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将TGS转换为GIF")
    parser.add_argument("-i", "--input", required=True, type=str, help="输入TGS文件路径")
    parser.add_argument("-o", "--output", required=True, type=str, help="输出的GIF文件路径")
    args = parser.parse_args()

    convert_tgs_to_gif(args.input, args.output)
