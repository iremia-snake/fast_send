class DataFile:
    def __init__(self, path):
        self.path = path


    def write(self, text):
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                text = text.replace('\r\n', '\n').replace('\r', '\n')
                file.write(text)
            return 0
        except Exception as e:
            return e


    def read(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                text = file.read()
                return text
        except Exception as e:
            return e