from essential_generators import DocumentGenerator

gen = DocumentGenerator()


class Player:
    def __init__(self, name, ID):
        self.name = name
        self.id = ID
        self.message = ''
        self.para = self.make_paragraph()
        self.char = 0
        self.is_correct = True
        self.remaining_char = self.para

    def get_message(self, msg):
        self.message = msg

    def get_para(self, para):
        self.para = para

    def check(self):
        print('checking input')
        self.is_correct = self.para.startswith(self.message)
        if self.is_correct:
            self.remaining_char = self.para.split(self.message, 1)[1]
            print(self.char)
            self.char = len(self.message)
        print(f'checking if {self.para}\n is equal to {self.message}')
        print(self.message == self.para)
        if self.remaining_char == '':
            self.increase_paragraph(self.para)

    @staticmethod
    def make_paragraph():
        print('makin paragraf')
        para = gen.paragraph()
        return para

    def increase_paragraph(self, paragraph):
        print('adding more paragraph')
        self.para = ' '.join([paragraph, gen.paragraph()])
