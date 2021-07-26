from .saveService.Externalservice import SaveReadService
from .mainWrite import WriteMessage


class TextMessage():

    @classmethod
    def encrypt(cls, message, password, imageIn, location, container):
        try:
            testmess = SaveReadService.takeText(message)
        except:
            return "error text file not recognized"
        err = WriteMessage.encrypt(testmess, password, imageIn, location, container)
        return err
