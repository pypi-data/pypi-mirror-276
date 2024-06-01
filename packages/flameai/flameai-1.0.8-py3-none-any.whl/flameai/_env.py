import subprocess


HAS_TORCH = None
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


def check_python_env() -> int:
    """
    Run 'python --version' to check if Python is installed and in the system PATH.
    Return the exit code of the command: 0 if Python is found, 1 if not.
    """
    try:
        return subprocess.run(['python', '--version'], check=True, capture_output=True).returncode
    except FileNotFoundError:
        return 1


def check_hive_env() -> int:
    """
    Run 'hive --version' to check if Hive is installed and in the system PATH.
    Return the exit code of the command: 0 if Hive is found, 1 if not.
    """
    try:
        return subprocess.run(['hive', '--version'], check=True, capture_output=True).returncode
    except FileNotFoundError:
        return 1


def cpu():
    """Get the CPU device."""
    return torch.device('cpu')


def gpu(i: int = 0):
    """Get a GPU device."""
    return torch.device(f'cuda:{i}')


def num_gpus() -> int:
    """Get the number of available GPUs."""
    return torch.cuda.device_count()


def try_gpu(i: int = 0):
    """Return gpu(i) if it exists, otherwise return cpu()."""
    if num_gpus() >= i + 1:
        return gpu(i)
    return cpu()


if __name__ == '__main__':
    print('check_python_env:', check_python_env())
    print('check_hive_env:', check_hive_env())
    if HAS_TORCH:
        print('try_gpu:', try_gpu())
