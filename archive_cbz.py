from pathlib import Path
import re, shutil

downloads_dir = Path('~/Downloads').expanduser()
archive_dir = Path('~/Comics').expanduser()

for cbz_file in downloads_dir.glob('*.cbz'):
  if m := re.match(r'\[Kox\]\[(.*)\].*', cbz_file.name):
    sub_dir = archive_dir / m.group(1)
    sub_dir.mkdir(exist_ok=True)

    copy_file = sub_dir / cbz_file.name
    shutil.copy(cbz_file, copy_file)
    print(copy_file)
