from .ImageStegano.imagecode import ImageCode
from .HiddenMessage.sneakmessage import SneakMessage
from .cryptpack.cryptograService import CryptograService
from .videoStegano.videoCode import VideoCode
from .saveService.Externalservice import SaveReadService



class WriteMessage:
    @classmethod
    def encrypt(cls, message, password, imageIn, location, container, type = None, extension=None):
        try:
            testmess = CryptograService.encrypt(message, password)
        except:
            return "message is incorrectly formatted"

        mesg = SneakMessage(testmess[0], "Text")
        mesg.setbin()
        if type != None:
            mesg.setType(type)
            extBin = mesg.extensionBin(extension)
            longExt = mesg.longExtBin(extension)
        encode = [testmess[1], testmess[2], testmess[3]]
        encodebin = CryptograService.binEncode(encode)
        info = mesg.getInfo()
        info = info[0] + info[1] + info[2] + info[3] + info[4]
        info = mesg.addEncode(info, encodebin)
        element = mesg.getbin()
        if type != None:
            info += longExt + extBin
        if container == "image":
            ima = ImageCode(imageIn)
            ima.transformBin()
            err = ima.addElement(info, element)
            if err != 0 :
                return "message is too big for the picture"
            try:
                reconst = ima.reConstruct(location + ".png")
            except:
                return "rental error"
        elif container == "video":
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
