import zipfile
import xml.etree.ElementTree as ET
import glob

with open('project_definition.txt', 'w', encoding='utf-8') as outfile:
    for file in glob.glob('*.docx'):
        outfile.write(f"--- Reading {file} ---\n")
        try:
            with zipfile.ZipFile(file) as docx:
                xml_content = docx.read('word/document.xml')
                tree = ET.XML(xml_content)
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                for p in tree.findall('.//w:p', ns):
                    texts = p.findall('.//w:t', ns)
                    if texts:
                        outfile.write(''.join([t.text for t in texts if t.text]) + '\n')
        except Exception as e:
            outfile.write(f"Failed: {e}\n")
