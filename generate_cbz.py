"""
Finds all .mobi files in ~/Downloads and converts them to .cbz files

"""
from pathlib import Path
import subprocess, zipfile, re

import epub

downloads_dir = Path('~/Downloads').expanduser()

def get_ebook_files():
  for f in downloads_dir.iterdir():
    if re.match(r'.*\.(mobi|kepub\.epub)$', f.name):
      yield f

def get_images(ebook_file: Path):
  match ebook_file.suffix:
    case '.mobi':
      yield from get_images_from_mobi(ebook_file)
    case '.epub':
      yield from epub.get_images(ebook_file)

def get_images_from_mobi(mobi_file: Path):
  """
  Convert the given .mobi file to an .epub file and then extract the images from the .epub file
  """
  # Create temporary .epub file
  epub_file = mobi_file.with_suffix('.epub')
  cmd = ['ebook-convert', mobi_file, epub_file]
  subprocess.run(cmd)

  yield from epub.get_images(epub_file)

  # Delete temporary .epub file
  epub_file.unlink()

def generate_cbz_file(cbz_file, images):
  with zipfile.ZipFile(cbz_file, 'w') as zf:
    for i, data in enumerate(images, 1):
      zf.writestr(f'{i:06}.jpg', data)



for ebook_file in get_ebook_files():
  print(ebook_file)
  cbz_file = (ebook_file.parent / ebook_file.stem).with_suffix('.cbz')
  generate_cbz_file(cbz_file, get_images(ebook_file))
