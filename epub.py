from zipfile import ZipFile
from pathlib import Path
import xml.etree.ElementTree as ET
import os.path

def get_images(epub_file: Path):
  with ZipFile(epub_file) as zf:
    opf_file = get_opf_file(zf)

    for page in get_pages(zf, opf_file):
      src = get_image(zf, page)
      if src is not None:
        yield zf.read(src)


def get_opf_file(zipfile: ZipFile) -> str:
  with zipfile.open('META-INF/container.xml') as fp:
    tree = ET.parse(fp)
    rootfile = tree.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
    return rootfile.attrib['full-path']

def get_pages(zipfile: ZipFile, opf_file: str):
  with zipfile.open(opf_file) as fp:
    tree = ET.parse(fp)
    for item in tree.iterfind('.//{http://www.idpf.org/2007/opf}item'):
      if item.attrib['media-type'] == 'application/xhtml+xml':
        yield item.attrib['href']

def get_image(zipfile: ZipFile, page: str) -> str:
  with zipfile.open(page) as fp:
    tree = ET.parse(fp)
    img = tree.find('.//{http://www.w3.org/1999/xhtml}img')
    if img is not None:
      path = os.path.join(os.path.dirname(page), img.attrib['src'])
      return resolve_path(path)

def resolve_path(path: str):
  """
  Eliminate .. from a path
  """
  parts = path.split('/')
  while '..' in parts:
    i = parts.index('..') - 1
    parts.pop(i)
    parts.pop(i)

  return '/'.join(parts)
