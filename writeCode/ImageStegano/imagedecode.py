from .imageparent import ImageParent


class ImageDecode(ImageParent):
    def __init__(self, image, listim=[]):
        ImageParent.__init__(self, image, listim)
        self._type = ""
        self._hiddenLong = 0
        self._message = []
        self._info = ""
        self._encode = []
        self._extension = ""

    def getExtension(self):
        return self._extension

    def __takeOtherInfo(self):
        self.__takeInfo()
        pointer = 668
        temp = ""
        counter = 1
        counter1 = 0
        while pointer < 676:
            temp += self._binImage[pointer][3]
            pointer += 1
        nbrExt = int(temp, 2)
        pointer = 676
        temp = ""
        print(nbrExt)
        while counter1 < nbrExt:
            temp += self._binImage[pointer][3]
            if counter == 8:
                temp = int(temp, 2)
                charc = chr(temp)
                self._extension += charc
                temp = ""
                counter1 += 1
                counter = 0
            pointer += 1
            counter += 1
        print(self._extension)

    def __takeInfo(self):
        for i in range(92):
            self._info += self._binImage[i][3]
        pointer = 92
        while pointer < 668:
            self._encode.append(self._binImage[pointer][3])
            pointer += 1

    def __takeImageInfo(self):
        for i in range(732):
            self._info += self._binImage[i][3]
        pointer = 732
        while pointer < 1308:
            self._encode.append(self._binImage[pointer][3])
            pointer += 1

    def getEncode(self):
        return self._encode

    def transformInfo(self):
        self.transformBin()
        type = ""
        temp = ""
        for i in range(28):
            temp += self._binImage[i][3]
            if (i + 1) % 7 == 0:
                print(temp)
                temp = int(temp, 2)
                charc = chr(temp)
                type += charc
                temp = ""
        self._type = type
        temp = ""

        if type == "Text":
            self.__takeInfo()
        elif type == "ImgT" or type == "ImgC" or type == "ImgL":
            print("Bontype")
            self.__takeImageInfo()
        elif type == "Utft" or type == "Isot":
            self.__takeOtherInfo()
        else:
            pass
        pointer = 28
        while pointer < len(self._info):
            temp += self._info[pointer]
            pointer += 1
        if type == "Text" or type == "Utft" or type == "Isot":
            long = int(temp, 2)
            self._hiddenLong = long
            return long
        else:
            return temp

    def getType(self):
        return self._type

    def getLong(self):
        return self._hiddenLong

    def decrypte(self, long, countersave=0, separation=True):
        pointer = 4
        pointer2 = 0
        counter = 0
        countertest = countersave
        temp = []
        nbr = long * 8
        print("nombre d'element a extraire", nbr)
        while  countertest <= nbr :
            if separation and counter >= 8:
                self._message.append(temp)
                temp = []
                counter = 0
            if pointer2 >= len(self._binImage):
                pointer2 = 0
                pointer += 1
            try:
                temp.append(self._binImage[pointer2][pointer])
                countertest += 1
            except :
                self._message.append(temp)
                return countertest, self._message
            pointer2 += 1
            counter += 1
        if not separation:
            self._message.append(temp)
        return 0, self._message

    def takeShape(self):
        pointer = len(self._info) + len(self._encode)
        shape = []
        temp = ""
        counter = 0
        while pointer <= len(self._info) + len(self._encode) + 48:
            if counter >= 16:
                print(len(temp))
                temp = int(temp, 2)
                shape.append(temp)
                counter = 0
                temp = ""
            temp += self._binImage[pointer][3]
            counter += 1
            pointer += 1
        return shape

    def setImgHiddenLong(self, longBin):
        self._hiddenLong = int(longBin, 2)

    def transInfoEncode(self, longBin):
        counter = 0
        EncodedBinLong = []
        EncodedLong = ""
        temp = []
        counter = 0
        for i in longBin:
            temp.append(i)
            counter += 1
            if counter >= 8:
                EncodedBinLong.append(temp)
                temp = []
                counter = 0

        print(counter)
        print(len(EncodedBinLong))
        for i in EncodedBinLong:
            temp = "".join(i)
            temp = int(temp, 2)
            charc = chr(temp)
            EncodedLong += charc
        return EncodedLong
