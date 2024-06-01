import re

import pandas as pd
from lxml import etree as ET

XML_ERROR = """
 IPC Scheme File Loading Problem
 Please download the ipc_xml scheme file from:
 https://www.wipo.int/ipc/itos4ipc/ITSupport_and_download_area/20240101/MasterFiles/index.html
 and set the corrected file address in ipc_xml
 """


class IpcParser:
    global XML_ERROR

    def __init__(
        self, ipc_xml="", ns="{http://www.wipo.int/classifications/ipc/masterfiles}"
    ):
        if not ipc_xml:
            raise Exception(XML_ERROR)
        self.file_name = ipc_xml
        self.default_ns = ns

    def __load_ipc_xml__(self):
        # Load the XML file
        try:
            tree = ET.parse(self.file_name)
            self.root = tree.getroot()
        except:
            raise Exception(XML_ERROR)

    def __clean_text__(self, text):
        return text.strip().replace("\n", "").replace("\t", "")

    def get_human_readable_ipc(self, code: str) -> str:
        code_len = len(code)
        ending_zeros = r"0+$"

        section_code = code[0]
        class_code = code[1:3] if code_len >= 3 else ""
        sub_class_code = code[3] if code_len >= 4 else ""
        main_group_code = " " + str(int(code[6:8])) + "/" if code_len >= 8 else ""
        sub_group_code = ""

        if code_len >= 9:
            sub_group = re.sub(pattern=ending_zeros, repl="", string=code[8:])
            sub_group_code = sub_group if sub_group else "00"

        return "".join(
            [section_code, class_code, sub_class_code, main_group_code, sub_group_code]
        )

    def extract_symbol_and_parent(self, elem, ns):
        # Get the symbol for the current element
        symbol = elem.attrib.get("symbol", "")
        kind = elem.attrib.get("kind", "")

        description_elems_title = elem.find(f".//{ns}textBody/{ns}title")

        description_elems = description_elems_title.findall(f"{ns}titlePart")
        full_desc = []

        for t in description_elems:
            short_desc = "".join(list(t.find(f"{ns}text").itertext()))
            ref_desc = t.find(f"{ns}entryReference")

            ref_symbol = ""
            if ref_desc is not None:
                for ref_elem in ref_desc.iter():
                    if ref_elem.attrib.get("ref"):
                        ref_symbol = " " + self.get_human_readable_ipc(
                            ref_elem.attrib["ref"]
                        )
                        break

                ref_desc = f' ({self.__clean_text__("".join(list(ref_desc.itertext())))}{ref_symbol})'
            else:
                ref_desc = ""

            short_desc += ref_desc
            full_desc.append(self.__clean_text__(short_desc))
        full_desc = "".join(full_desc)

        # Get the parent symbol by traversing up the hierarchy
        parent_symbols = [
            parent.attrib.get("symbol", "")
            for parent in elem.iterancestors()
            if parent.attrib.get("symbol")
        ]
        # Reverse the order to get the correct parent hierarchy

        human_symbol = self.get_human_readable_ipc(symbol)
        human_parent = [self.get_human_readable_ipc(p) for p in parent_symbols[::-1]]
        materialized_parent = " >> ".join(human_parent)
        return human_symbol, full_desc, human_parent, materialized_parent, kind

    def get_dataframe(self):
        df = []
        self.__load_ipc_xml__()
        # Iterate through each element and extract symbol, title and parent
        for elem in self.root.findall(f".//{self.default_ns}ipcEntry"):
            # exclude index and notes
            if elem.attrib["kind"] in ["i", "n"]:
                continue

            symbol, text_content, parent, materialized_path, kind = (
                self.extract_symbol_and_parent(elem, self.default_ns)
            )
            if symbol:
                df.append(
                    {
                        "code": symbol,
                        "description": text_content,
                        "parent": parent,
                        "materialized_path": materialized_path,
                        "kind": kind,
                    }
                )
        return pd.DataFrame(df)
