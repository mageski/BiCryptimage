from .cryptpack.cryptograService import CryptograService
from .ImageStegano.imagedecode import ImageDecode
from .saveService.Externalservice import SaveReadService


class DecriptImage:
    @classmethod
    def decrypt(cls, imageIn, password, location):
        try:
            img = ImageDecode(imageIn)
        except:
            return "main picture error"
        encodedBinLong = img.transformInfo()
        print(img.getType())
        if img.getType() == "Text":
            long = img.getLong()
            finish, encryptMess = img.decrypte(long)
            binMess = CryptograService.trasnformMess(
                encryptMess, img.getType())
            encodebin2 = img.getEncode()
            decodedMess = CryptograService.deBinEncode(encodebin2)
            decodedMess.insert(0, binMess)
            try:
                message = CryptograService.decrypt(decodedMess, password)
            except:
                return "password invalid"
            location += ".txt"
            try:
                SaveReadService.saveText(message, location)
            except:
                return "rental error"
        elif img.getType() == "ImgT" or img.getType() == "ImgC" or img.getType() == "ImgL":
            encodebin2 = img.getEncode()
            encodedLong = img.transInfoEncode(encodedBinLong)
            decodedMess = CryptograService.deBinEncode(encodebin2)
            decodedMess.insert(0, encodedLong)
            print(decodedMess)
            try:
                long = CryptograService.decrypt(decodedMess, password)
            except:
                return "password invalid"
            img.setImgHiddenLong(long)
            shape = img.takeShape()
            long = img.getLong()
            finish, binImaReconst = img.decrypte(long)
            binima = CryptograService.trasnformMess(
                binImaReconst, img.getType())
            location += ".png"
            if img.getType() == "ImgL":
                shape.pop()
            print(shape)
            newIma = CryptograService.reconstructSneak(
                binima, shape, location)
        elif img.getType() == "Utft" or img.getType() == "Isot":
            long = img.getLong()
            finish, encryptMess = img.decrypte(long)
            messBin = CryptograService.trasnformMess(
                encryptMess, img.getType())
            encodebin2 = img.getEncode()
            decodedMess = CryptograService.deBinEncode(encodebin2)
            decodedMess.insert(0, messBin)
            try:
                message = CryptograService.decrypt(decodedMess, password)
            except:
                return "password invalid"
            location += img.getExtension()
            try:
                if img.getType() == "Utft":
                    SaveReadService.saveOther(
                        message.encode("UTF-8"), location)
                else:
                    SaveReadService.saveOther(
                        message.encode("ISO-8859-1"), location)
            except:
                return "encodage error"
        else:
            return "no element hide find"
        return 0
