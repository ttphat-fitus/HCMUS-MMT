# modules/file_transfer.py
import shutil, os

def copy_file(src_path, dst_dir='files'):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src_path, dst_dir)
