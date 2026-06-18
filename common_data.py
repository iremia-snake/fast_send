from os import path, remove, listdir

class CommonTextHandler:
    """
    Организует хранение глобального текста и резервирование в файл
    """

    edit_id = 0
    path = ""
    text = ""

    def __init__(self, text_file_path):
        self.path = text_file_path

    def write(self, text, reserve = True):
        """
        Записывает ноовый текст, резервирует в файл, если не указан параметр
        """
        if self.text != text:
            self.text = text
            self.edit_id += 1

            if not reserve:
                return None
            try:
                with open(self.path, 'w', encoding='utf-8') as file:
                    text = text.replace('\r\n', '\n').replace('\r', '\n')
                    file.write(text)
                return None
            except Exception as e:
                return e
    
    def get_text(self):
        return self.text

    def read_file(self):
        """
        Читает текст из файла
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                self.text = file.read()
                return self.text
        except Exception as e:
            return e
        

class CommonFilesHandler:
    """
    Организует сохранение и чтение общих файлов
    """

    directory_path = ""
    edit_id = 0

    

    def __init__(self, directory):
        self.directory_path = directory


    def get_list_files(self):
        return [f for f in listdir(self.directory_path) if path.isfile(path.join(self.directory_path, f))]

    
    def add(self, file):
        def unique_name(filename):
            base_name = filename
            for i in range(1, 100):
                fullpath = path.join(self.directory_path, filename)
                if path.exists(fullpath):
                    name = path.basename(base_name).split('.')[0]
                    ext = path.basename(base_name).split('.')[-1]
                    filename = name + f'({i}).' + ext
                else:
                    return filename
                 
        try:           
            file.save(path.join(self.directory_path, unique_name(file.filename)))
            self.edit_id += 1
            return None
        except Exception as e:
            print(e)
            return e


    def remove_file(self, filename):
        file_path = path.join(self.directory_path, filename)
        try:
            remove(file_path)
            self.edit_id += 1
            return None
        except Exception as e:
            return e