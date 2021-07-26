from .cryptpack.cryptograService import CryptograService
from .mainWrite import WriteMessage
from .saveService.Externalservice import SaveReadService


class OtherMessage:
    @classmethod
    def encrypt(cls, message, password, imageIn, location, container):
        try:
            encodedMessage, extension = SaveReadService.takeOther(message)
        except:
            return "can't open hidden file "
        try:
            decodeMessage, type = CryptograService.deBinDecode(encodedMessage)
        except:
            return "error during hidden file decode"
        err = WriteMessage.encrypt(
            decodeMessage, password, imageIn, location, container, type, extension)
        return err
