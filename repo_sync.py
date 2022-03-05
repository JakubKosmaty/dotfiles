import subprocess


def main():
    subprocess.check_call(('git', 'pull'))
    subprocess.check_call(('git', 'add', '.'))
    subprocess.check_call(('git', 'commit', '-m', 'Auto Sync'))
    subprocess.check_call(('git', 'push'))


if __name__ == "__main__":
    main()
