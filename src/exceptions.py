class ShellError(Exception):
    '''
    Пользовательское исключение для ошибок
    '''
    def __init__(self, message: str):
        '''
        Инициализирует исключение с ошибкой


        Args:
            message(str)
        '''
        self.message = message
        super().__init__(self.message)
