from abc import abstractmethod
from measure import names


class Method(object):
    @staticmethod
    @abstractmethod
    def init(options: tuple):
        pass

    @staticmethod
    @abstractmethod
    def step(snap: dict):
        pass

    @staticmethod
    @abstractmethod
    def finalize():
        pass


class PrintAtEndMethod(Method):
    my_options = []
    output = ""

    @staticmethod
    def init(options: list):
        PrintAtEndMethod.my_options = options
        # PrintMethod.output += "time"
        for option in PrintAtEndMethod.my_options:
            PrintAtEndMethod.output += "\t" + names[option]
        PrintAtEndMethod.output += "\n"

    @staticmethod
    def step(snap: dict):
        # PrintMethod.output += str(snap["time"])
        for option in PrintAtEndMethod.my_options:
            PrintAtEndMethod.output += "\t" + str(snap[option])
        PrintAtEndMethod.output += "\n"

    @staticmethod
    def finalize():
        print(PrintAtEndMethod.output)


class PrintInTimeMethod(Method):
    my_options = []

    @staticmethod
    def init(options: list):
        output = ""
        PrintInTimeMethod.my_options = options
        # PrintMethod.output += "time"
        for option in PrintInTimeMethod.my_options:
            output += "\t" + names[option]
        output += "\n"
        print(output)

    @staticmethod
    def step(snap: dict):
        output = ""
        # PrintMethod.output += str(snap["time"])
        for option in PrintInTimeMethod.my_options:
            output += "\t" + str(snap[option])
        output += "\n"
        print(output)

    @staticmethod
    def finalize():
        pass


class CsvMethod(Method):
    @staticmethod
    def init(options: tuple):
        pass

    @staticmethod
    def step(snap: dict):
        pass

    @staticmethod
    def finalize():
        pass
