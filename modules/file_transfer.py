# modules/file_transfer.py
import shutil
import os

def copy_file(src, dst_dir='files'):
    os.makedirs(dst_dir, exist_ok=True)
    try:
        filename = os.path.basename(src)
        dst_path = os.path.join(dst_dir, filename)
        shutil.copy(src, dst_path)
        return f"File copied: {src} → {dst_path}"
    except Exception as e:
        return f"Unable to copy: {e}"