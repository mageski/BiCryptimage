from ..ImageStegano.imagecode import ImageCode
from PIL import Image
import numpy
import cv2
from vidgear.gears import WriteGear
import subprocess as sp

class VideoCode:
    def __init__(self, listImage, fps):
        self._fps = fps
        self._list = []
        for i in listImage:
            self._list.append(ImageCode(None, i))
        try:
            self._x, self._y, self._z = self._list[0]._tabImage.shape
        except:
            self._x, self._y = self._list[0]._tabImage.shape
            self._z = 1
        print(self._z)
        self._change = None

    def addElement(self, info, element):
        counter = 0
        finish = 0
        print("hideen long = ", len(element))
        for i in self._list:
            i.transformBin()
            finish = i.addElement(info, element, finish)
            print("encours = ", finish, "/", len(element))
            i._tabImage = self.reConstruct(i, counter)
            print("modified frame = ", counter)
            counter += 1
            if finish == 0:
                break

    def reConstruct(self, image, place):
        newImage = []
        for i in range(len(image._binImage)):
            newImageElement = "".join(image._binImage[i])
            val = int(newImageElement, 2)
            newImage.append(val)
        if self._z == 1:
            newImage = numpy.reshape(
                newImage, (self._x, self._y)).astype("uint8")
        else:
            newImage = numpy.reshape(
                newImage, (self._x, self._y, self._z)).astype("uint8")
        return newImage

    def reConstVid(self, fps, location):
        video = cv2.VideoWriter(location + ".avi", cv2.VideoWriter_fourcc(
            *'HFYU'), fps, (self._y, self._x))
        counter = 0
        for i in self._list:
            video.write(i._tabImage)
        video.release()
