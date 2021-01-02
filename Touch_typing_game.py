from essential_generators import DocumentGenerator

gen = DocumentGenerator()


class Player:
    def __init__(self, name, ID):
        self.name = name
        self.id = ID
        self.message = ''
        self.para = self.make_paragraph()
        self.is_correct = True
        self.paragraph_increases = 0

    def get_message(self, msg):
        self.message = msg

    def get_para(self, para):
        self.para = para

    def check(self):
        print('checking input')
        self.is_correct = self.para.startswith(self.message)
        if self.para == self.message:
            self.increase_paragraph(self.para)
            self.paragraph_increases += 1

    @staticmethod
    def make_paragraph():
        print('makin paragraf')
        para = gen.paragraph()
        return para

    @staticmethod
    def increase_paragraph(paragraph):
        print('adding more paragraph')
        paragraph = ' '.join([paragraph, gen.paragraph()])
        return paragraph
