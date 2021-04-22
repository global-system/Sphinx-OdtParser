from docutils.parsers.rst import Parser as RstParser
from pathlib import Path
import os.path
from panflute import *


class Filter:
    def __init__(self):
        self.is_code_block_open = False
        self.block_body = []

    def get_text(self,elem: Element,doc) -> str:
        text = []

        def action(child_elem, doc):
            if isinstance(child_elem, Str):
                text.append(child_elem.text)
            elif isinstance(child_elem, Space):
                text.append(" ")
            elif isinstance(child_elem, LineBreak):
                text.append("\n")
            elif isinstance(child_elem, SoftBreak):
                text.append("\n")

        elem.walk(action, doc)
        return "".join(text)

    def prepare(self, doc):
        pass

    def end_code_block(self):
        #remove end tag
        code_text = self.block_body[0:-1]
        cb = CodeBlock("".join(code_text), classes=[""])
        self.is_code_block_open = False
        self.block_body = []
        return cb

    def action(self, elem, doc):
        if isinstance(elem, Image):
            i: Image = elem
            (_,file_name) = os.path.split(i.url)
            i.url = "build/Pictures/" + file_name
            return None
        elif isinstance(elem, Para):
            text = self.get_text(elem, doc)
            if text == """```""":
                if self.is_code_block_open:
                    return self.end_code_block()
                else:
                    self.is_code_block_open = True
                    return []
            if self.is_code_block_open:
                self.block_body.append("\n")
                return []
        if self.is_code_block_open:
            if isinstance(elem, Str):
                self.block_body.append(elem.text)
            elif isinstance(elem, Space):
                self.block_body.append(" ")

    def finalize(self, doc: Doc):
        if self.is_code_block_open:
            cb = self.end_code_block()
            doc.content.append(Para(Emph(Str("Error, there is an unclosed code block:"))))
            doc.content.append(cb)
        pass

    @staticmethod
    def filter(input_file_name: str, output_file_name: str):
        filter = Filter()

        def action(elem, doc):
            return filter.action(elem, doc)

        def prepare(doc):
            return filter.prepare(doc)

        def finalize(doc):
            return filter.finalize(doc)

        with open(output_file_name, mode='w', encoding='utf-8') as output:
            with open(input_file_name, encoding='utf-8') as input:
                run_filters([action], prepare=prepare, finalize=finalize, input_stream=input, output_stream=output,
                            doc=None)


class OdtParser(RstParser):
    supported = ['bodt']

    def parse(self, inputstring, document):
        path = document.current_source
        (dir_name,full_file_name) = os.path.split(path)
        file_name = full_file_name.split('.')[0]
        os.path.join(dir_name,'build',file_name + ".json")
        run_pandoc(args=['-o', os.path.join(dir_name,'build',file_name + ".json"),
                         '--extract-media',  os.path.join(dir_name,'build'),
                         os.path.join(dir_name,file_name + ".odt")
                         ]
                   )
        Filter.filter(
            os.path.join(dir_name,'build',file_name + ".json"),
            os.path.join(dir_name,'build',file_name + "_s1.json")
                      )

        run_pandoc(args=[
                        '-t', 'rst',
                        '-o', os.path.join(dir_name,'build',file_name + ".tmp"),
                         os.path.join(dir_name,'build',file_name + "_s1.json")
                         ]
                   )
        text = Path(os.path.join(dir_name,'build',file_name + ".tmp")).read_text(encoding="UTF-8")
        document.settings.env.note_dependency(os.path.join(dir_name,file_name + ".odt"))
        super().parse(text, document)
