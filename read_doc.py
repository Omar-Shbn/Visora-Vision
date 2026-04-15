import zipfile
import xml.etree.ElementTree as ET
import glob
import sys

# find all docx files
for file in glob.glob('*.docx'):
    print(f"Reading {file}...")
    try:
        with zipfile.ZipFile(file) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text = '\n'.join([''.join([t.text for t in p.findall('.//w:t', ns) if t.text]) for p in tree.findall('.//w:p', ns)])
            print(text)
    except Exception as e:
        print(f"Failed to read {file}: {e}")
