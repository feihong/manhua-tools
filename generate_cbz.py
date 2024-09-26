"""
Finds all .mobi files in ~/Downloads and converts them to .cbz files

"""
from pathlib import Path
import subprocess, zipfile, re


downloads_dir = Path('~/Downloads').expanduser()

def get_mobi_files():
  yield from downloads_dir.glob('*.mobi')

def get_images(mobi_file: Path):
  """
  Convert the given .mobi file to an .epub file and then extract the images from the .epub file
  """
  # Create temporary .epub file
  epub_file = mobi_file.with_suffix('.epub')
  cmd = ['ebook-convert', mobi_file, epub_file]
  subprocess.run(cmd)

  with zipfile.ZipFile(epub_file) as zf:
    for name in zf.namelist():
      if m := re.match(r'images/(\d{2,}\.[a-z]{3,4})', name):
        yield m.group(1), zf.read(name)

  # Delete temporary .epub file
  epub_file.unlink()

def generate_cbz_file(cbz_file, images):
  with zipfile.ZipFile(cbz_file, 'w') as zf:
    for name, data in images:
      zf.writestr(name, data)

for mobi_file in get_mobi_files():
  print(mobi_file)
  cbz_file = mobi_file.with_suffix('.cbz')
  generate_cbz_file(cbz_file, get_images(mobi_file))
