import sys
import gzip
import io
import os
import yaml
import logging
from rlottie_python import LottieAnimation

CONFIG_PATH = os.path.expanduser('~/tgBuffer_to_gif_config.yaml')


def is_gzip(data):
    return data[:2] == b'\x1f\x8b'


def load_config(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    return None


def setup_logging(log_path):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(module)s.py[line:%(lineno)d] - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    output_path = sys.argv[1]
    config = load_config(CONFIG_PATH)

    if config and config.get('Debug', {}).get('enable', False):
        log_path = os.path.expanduser(config['Debug'].get('log_path', os.path.expanduser('~/tgs_to_gif.log')))
        setup_logging(log_path)
        logging.debug(f"[{output_path}] 调试日志功能已启用")

    hook_json_path = config['Debug'].get('hook_json_path', '') if config else ''

    if hook_json_path and os.path.exists(hook_json_path):
        hook_json_path = os.path.expanduser(hook_json_path)
        with open(hook_json_path, 'r') as file:
            data = file.read()
        logging.debug(f"[{output_path}] 从 {hook_json_path} 读取的数据")
    else:
        data = sys.stdin.buffer.read()
        if is_gzip(data):
            with gzip.GzipFile(fileobj=io.BytesIO(data)) as f:
                data = f.read()
        data = data.decode('utf-8')

    anim = LottieAnimation.from_data(data)
    anim.save_animation(output_path)

    if config and config.get('Debug', {}).get('enable', False):
        logging.debug(f"[{output_path}] 动画已保存到 {output_path}")


if __name__ == '__main__':
    main()
