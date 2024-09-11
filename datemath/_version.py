import os

current_dir = os.path.dirname(os.path.abspath(__file__))
version_file = os.path.join(current_dir, '../VERSION.txt')

with open(version_file, 'r') as f:
    __version__ = f.read().strip()