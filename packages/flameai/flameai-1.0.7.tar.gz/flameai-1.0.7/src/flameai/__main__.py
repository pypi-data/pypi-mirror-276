# Usage: python -m flameai
from ._env import check_hive_env, check_python_env, HAS_TORCH, num_gpus


def check_env():
    def text(e):
        return 'YES' if e == 0 else 'NO'
    print(f'Python: {text(check_python_env())}')
    print(f'Hive:   {text(check_hive_env())}')
    if HAS_TORCH:
        print(f'GPU:    {"YES" if num_gpus() >= 1 else "NO"}')


if __name__ == "__main__":
    check_env()
