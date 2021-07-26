from PIL import Image
import numpy


class SneakImage():

    def __init__(self, image):
        self.image = Image.open(image)
        if(self.image).mode == "P":
            self.image = Image.open(image).convert("L")
        self._binImage = []
        self._tabImage = numpy.asarray(self.image).astype('uint8')
        self.__bin = []

    def getNumArray(self):
        try:
            x, y, z = self._tabImage.shape
        except:
            x, y = self._tabImage.shape
            z = 1
        tempTabImage = numpy.reshape(self._tabImage, (x * y * z))
        strTemp = " ".join(map(str, tempTabImage))
        return strTemp

    def getShapBin(self):
        binShape = []
        shape = self._tabImage.shape
        for i in shape:
            temp = format(i, '016b')
            binShape.append(temp)
        print(shape)
        return(binShape)

    def getType(self):
        shape = self._tabImage.shape
        try:
            if shape[2] == 3:
                return("ImgC")
                print("ok")
            elif shape[2] == 4:
                return("ImgT")
        except:
            return("ImgL")

    def getBinima(self):
        try:
            x, y, z = self._tabImage.shape
        except:
            x, y = self._tabImage.shape
            z = 1
        tempTabImage = numpy.reshape(self._tabImage, (x * y * z))
        for i in range(len(tempTabImage)):
            temp = format(tempTabImage[i], '08b')
            self._binImage.append(temp)
        print("la longeure du image est de : ", len(self._binImage))
        return self._binImage
