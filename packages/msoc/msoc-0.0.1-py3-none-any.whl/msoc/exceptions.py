class LoadedEngineNotFoundError(KeyError):
    def __init__(self, name):
        super().__init__("Движок не был найден в загруженных: " + name)


class EnginePathNotFoundError(FileNotFoundError):
    def __init__(self, path):
        super().__init__("Не удалось импортировать движок: " + path)