import sys
from rlottie_python import LottieAnimation


def main():
    data = sys.stdin.read()
    output_path = sys.argv[1]

    anim = LottieAnimation.from_data(data)
    anim.save_animation(output_path)


if __name__ == '__main__':
    main()
