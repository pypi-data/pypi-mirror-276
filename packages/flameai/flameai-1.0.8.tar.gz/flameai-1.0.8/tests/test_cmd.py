import subprocess


def test_hey():
    res = subprocess.run(['hey', '-n', 'World'],
                         capture_output=True,
                         text=True)
    assert res.returncode == 0
    assert res.stdout == 'Hey, World!\n'
