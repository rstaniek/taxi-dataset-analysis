import abc
from abc import abstractmethod, ABCMeta

#Sth like an interface IDK LOL
class Executable(metaclass=ABCMeta):

    @abstractmethod
    def run(self, args):
        raise NotImplementedError('user must define this method manually')
