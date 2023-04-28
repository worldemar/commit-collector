import os
import subprocess
import argparse

class Directory:
    def __init__(self, dir_name):
        self.old_dir = os.path.abspath(os.curdir)
        self.new_dir = os.path.abspath(dir_name)
    def __enter__(self):
        os.chdir(self.new_dir)
    def __exit__(self, exc_type, exc_value, exc_tb):
        os.chdir(self.old_dir)


def parse_args():
    parser = argparse.ArgumentParser(description='Collects the git log for a repo')
    parser.add_argument('--author', help='author to collect commits from')
    return parser.parse_args()

def collect_one_repo(repo_name, author):
    with Directory(repo_name):
        return subprocess.check_output([
            'git', 'log',
            f'--author={author}',
            '--pretty=format: %ai %h %ae %s']).splitlines()


def collect_all_repos(author):
    data = []
    for repo_name in os.listdir('.'):
        if os.path.isdir(repo_name) and os.path.isdir(os.path.join(repo_name,'.git')):
            data += collect_one_repo(repo_name, author)
    return data


def main():
    args = parse_args()
    data = collect_all_repos(args.author)
    data.sort()
    for d in data:
        try:
            print(d.decode('utf-8'))
        except:
            print(d)


if __name__ == '__main__':
    main()
