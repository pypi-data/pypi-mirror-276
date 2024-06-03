class testing():
    test = 'test'
    test__ = 'testing'

    def __init__(self):
        test = 'test'
        testing = 'testing'
        self.test = 'test'
        self.testing = 'testing'

    def __hello__(self):
        response = f'{self.test} {self.testing}'

        return response 

    @classmethod
    def hello_class(cls):
        output = f'{cls.test} {cls.test__}'
        status_code = 0
        print(output)

        return status_code

    @staticmethod
    def hello_static(cls):
        response = f'{cls.test} {cls.test__}'

        return response

    @classmethod
    def retrive_testing(cls):
        test = cls.hello_static(cls)

        return test