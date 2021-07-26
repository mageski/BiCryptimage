
from .saveService.Externalservice import SaveReadService
from .cryptpack.cryptograService import CryptograService
from .HiddenMessage.sneakmessage import SneakMessage
from videoStegano.videoCode import VideoCode


class VidOther:
    @classmethod
    def encrypt(cls, message, password, imageIn, location):
        try:
            encodedMessage, extension = SaveReadService.takeOther(message)
        except:
            return "can't open hidden file"
        try:
            decodeMessage, type = CryptograService.deBinDecode(encodedMessage)
        except:
            return "error during hidden file decode"
        testmess = CryptograService.encrypt(decodeMessage, password)
        try:
            mesg = SneakMessage(testmess[0], "Text")
        except:
            return "transformation into text error"
        mesg.setbin()
        mesg.setType(type)
        extBin = mesg.extensionBin(extension)
        longExt = mesg.longExtBin(extension)
        encode = [testmess[1], testmess[2], testmess[3]]
        encodebin = CryptograService.binEncode(encode)
        info = mesg.getInfo()
        info = info[0] + info[1] + info[2] + info[3] + info[4]
        info = mesg.addEncode(info, encodebin)
        element = mesg.getbin()
        info += longExt + extBin
        try:
            x, fps = SaveReadService.TakeVide(imageIn, True)
        except:
            return "error during video read"
        try:
            vid = VideoCode(x, fps)
        except:
            return "error during video trasform"
        try:
            vid.addElement(info, element)
        except:
            return "error during message input"
        try:
            vid.reConstVid(fps, location)
        except:
            return"rental error"
        return 0
