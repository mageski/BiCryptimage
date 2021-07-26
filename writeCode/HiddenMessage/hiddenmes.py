import abc


class HiddenMes(abc.ABC):

    @abc.abstractmethod
    def setbin(self):
        pass

    @abc.abstractmethod
    def getbin(self):
        return "".join(self._bin)
