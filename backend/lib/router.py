import inspect


def url(path):
    def wrapper(func):
        return func
    return wrapper


class Router:
    def __init__(self):
        self.pathes = {}

    def collect_pathes(self, cls, decorator_name='url'):
        sourcelines = inspect.getsourcelines(cls)[0]

        for i, line in enumerate(sourcelines):
            line = line.strip()

            if line.split('(')[0].strip() == f'@{decorator_name}':
                name = ''

                for shift in range(1, 10):
                    nextLine = sourcelines[i+shift]
                    splited_line = nextLine.split('def')

                    if len(splited_line) > 1:
                        name = splited_line[1].split('(')[0].strip()

                        break

                self.pathes[sourcelines[i].split('\'')[1]] = name

    def get_method(self, path):
        return self.pathes[path]
