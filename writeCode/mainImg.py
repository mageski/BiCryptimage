from .cryptpack.cryptograService import CryptograService
from .hiddenimage.sneakImage import SneakImage
from .HiddenMessage.sneakmessage import SneakMessage
from .ImageStegano.imagecode import ImageCode
from .videoStegano.videoCode import VideoCode
from .saveService.Externalservice import SaveReadService


class ImageMessage:
    @classmethod
    def encrypt(cls, message, password, imageIn, location, container):
        try:
            ima = SneakImage(message)
        except:
            return "error hidden picture"
        imaray = ima.getNumArray()
        imType = ima.getType()
        binshape = ima.getShapBin()
        binIma = ima.getBinima()
        try:
            mesg = SneakMessage(binIma, "Bina")
        except:
            return "error during hidden image transformation"
        mesg.setbin()
        mesg.setType(imType)
        info = mesg.getInfo()
        encodedIma = CryptograService.encrypt(info[4], password)
        long = CryptograService.longEncodeBin(encodedIma[0])
        long = "".join(long)
        info = info[0] + info[1] + info[2] + info[3] + long
        encode = [encodedIma[1], encodedIma[2], encodedIma[3]]
        encodebin = CryptograService.binEncode(encode)
        encodebin += binshape
        info = mesg.addEncode(info, encodebin)
        element = mesg.getbin()
        if container == "image":
            try:
                codedIm = ImageCode(imageIn)
            except:
                return "main picture error"
            codedIm.transformBin()
            err = codedIm.addElement(info, element)
            if err != 0:
                return "message is too big for the picture"
            location += ".png"
            try:
                reconst = codedIm.reConstruct(location)
            except:
                return"rental error"
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
