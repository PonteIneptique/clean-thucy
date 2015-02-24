from lxml import etree
from copy import deepcopy
import re
pattern = re.compile('\s+')

with open("index.xml") as f:
    tree = etree.parse(f)
    root = tree.getroot()
    scope = 100
    superscripts = []
    upcoming_deletion = []
    for element in root.iter():
        if isinstance(element.tag, str):
            if element.tag == "{http://www.tei-c.org/ns/1.0}hi" and element.get("rend") == "superscript":
                if(element.text.isnumeric()):
                    element.text = re.sub(pattern, '', element.text)
                    superscripts.append(element)
                """
                Not a concern here
                if len(previous) and element.tail:
                    previous.text = previous.text + element.tail
                elif element.tail:
                    element.getparent().text = element.getparent().text + element.tail
                """
            elif element.tag == "{http://www.tei-c.org/ns/1.0}note" and element.get("type") == "footnote":
                if element.text and len(superscripts) > 0:
                    while superscripts[0].text[0] != element.text[0]:
                        print (" ---> {0}".format(etree.tostring(superscripts[0])))
                        print (" ---> {0}".format(element.text))
                        superscripts = superscripts[1:]
                if len(superscripts) > 0 and element.text and superscripts[0].text[0] == element.text[0]:
                    context = superscripts[0].getparent()
                    stored_tail = element.tail

                    copied = deepcopy(element)
                    copied.tail = superscripts[0].tail
                    context.replace(superscripts[0], copied)
                    upcoming_deletion.append(element)

                    superscripts = superscripts[1:]
            elif element.tag == "{http://www.tei-c.org/ns/1.0}note":
                print(element.text)

    for e in upcoming_deletion:
        e.getparent().remove(e)
    with open("output.xml", "wb") as ff:
        tree.write(ff, encoding="utf-8")
"""
    for element in root.findall(".//tei:hi[@rend='superscript']", {"tei": "http://www.tei-c.org/ns/1.0"}):
        if(element.text.isnumeric()):
            footnote = element.findall(".//tei:note[@type='footnote']", {"tei": "http://www.tei-c.org/ns/1.0"})
            print(ElementTree.tostring(footnote))
"""
