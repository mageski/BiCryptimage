from ..ImageStegano.imagedecode import ImageDecode
from ..cryptpack.cryptograService import CryptograService
from ..saveService.Externalservice import SaveReadService
from PIL import Image
import numpy


class VideoDecode:
    def __init__(self, listImage):
        self._list = []
        for i in listImage:
            self._list.append(ImageDecode(None, i))
        try:
            self._x, self._y, self._z = self._list[0]._tabImage.shape
        except:
            self._x, self._y = self._list[0]._tabImage.shape
            self._z = 1
        self.__message = []
        self.__finalMess = []

    def extract(self, password, location):
        finish = 0
        encodedBinLong = self._list[0].transformInfo()
        if self._list[0].getType() == "Text":
            long = self._list[0].getLong()
            self.getHidenMess(long)
            return self.extractText(password, location, self._list[0].getType())
        elif self._list[0].getType() == "ImgT" or self._list[0].getType() == "ImgC" or self._list[0].getType() == "ImgL":
            return self.extractImg(password, location, self._list[0].getType(), encodedBinLong)
        elif self._list[0].getType() == "Utft" or self._list[0].getType() == "Isot":
            long = self._list[0].getLong()
            self.getHidenMess(long)
            return self.extractOther(password, location, self._list[0].getType())
        else:
            return "dont have recognized hidden element"
    def extractImg(self, password, location, types, encodedBinLong):
        encodebin2 = self._list[0].getEncode()
        encodedLong = self._list[0].transInfoEncode(encodedBinLong)
        decodedMess = CryptograService.deBinEncode(encodebin2)
        decodedMess.insert(0, encodedLong)
        print(decodedMess)
        try:
            long = CryptograService.decrypt(decodedMess, password)
        except:
            return "password invalid"
        self._list[0].setImgHiddenLong(long)
        shape = self._list[0].takeShape()
        long = self._list[0].getLong()
        self.getHidenMess(long)
        binima = CryptograService.trasnformMess(
            self.__finalMess,types)
        location += ".png"
        if types == "ImgL":
            shape.pop()
        print(shape)
        newIma = CryptograService.reconstructSneak(
            binima, shape, location)
        return 0
    def extractText(self, password, location, types):
        binMess = CryptograService.trasnformMess(self.__finalMess, types)
        encodebin2 = self._list[0].getEncode()
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
        return 0
    def extractOther(self, password, location, types):

        mess = CryptograService.trasnformMess(self.__finalMess, types)
        encodebin2 = self._list[0].getEncode()
        decodedMess = CryptograService.deBinEncode(encodebin2)
        decodedMess.insert(0, mess)
        try:
            message = CryptograService.decrypt(decodedMess, password)
        except:
            return "password invalid"
        location += self._list[0].getExtension()
        try:
            if self._list[0].getType() == "Utft":
                SaveReadService.saveOther(
                    message.encode("UTF-8"), location)
            else:
                SaveReadService.saveOther(
                    message.encode("ISO-8859-1"), location)
        except:
            return "rental error"
        return 0
    def reorganise(self, messUnit):
        counter = 0
        temp = []
        final = []
        for i in messUnit:
            if counter >= 8:
                final.append(temp)
                temp = []
                counter = 0
            temp.append(i)
            counter += 1
        return final
    def getHidenMess(self, long):
        finish = 0
        for i in self._list:
            i.transformBin()
            finish, encryptMess = i.decrypte(long, finish, False)
            self.__message += encryptMess
            print("decriptage en cours ", finish, "/", long * 8)
            if finish == 0:
                break
        messUnit = []
        for i in self.__message:
            messUnit += i
        self.__finalMess = self.reorganise(messUnit)
