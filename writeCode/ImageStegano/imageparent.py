from PIL import Image
import numpy


class ImageParent():
    def __init__(self, image, listim=[]):
        if  listim == []:
            self.image = Image.open(image)
            if(self.image).mode == "P":
                self.image = Image.open(image).convert("L")
            self._binImage = []
            self._tabImage = []
        else:
            self.image = None
            self._binImage = []
            self._tabImage = listim
    def _transformTab(self):
        if self.image != None:
            self._tabImage = numpy.asarray(self.image).astype('uint8')
        else:
            pass
    def transformBin(self):
        self._transformTab()
        self._binImage = []
        try:
            x, y, z = self._tabImage.shape
        except:
            x, y = self._tabImage.shape
            z = 1
        tempTabImage = numpy.reshape(self._tabImage, (x * y * z))
        for i in range(len(tempTabImage)):
            temp = format(tempTabImage[i], '08b')
            temp = list(temp.strip())
            self._binImage.append(temp)

    def reConstruct(self, location):
        newImage = []
        for i in range(len(self._binImage)):
            newImageElement = "".join(self._binImage[i])
            val = int(newImageElement, 2)
            newImage.append(val)
        try:
            x, y, z = self._tabImage.shape
        except:
            x, y = self._tabImage.shape
            z = 1
        if z == 1:
            newImage = numpy.reshape(newImage, (x, y))
        else:
            newImage = numpy.reshape(newImage, (x, y, z))
        print("c est ici :", (self._tabImage == newImage).all())
        if z == 4:
            Image.fromarray((newImage).astype('uint8'), 'RGBA').save(location)
        elif z == 3:
            Image.fromarray((newImage).astype('uint8'), 'RGB').save(location)
        else:
            Image.fromarray((newImage).astype('uint8'), 'L').save(location)
        return newImage
