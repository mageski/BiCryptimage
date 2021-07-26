from .imageparent import ImageParent


class ImageCode(ImageParent):

    def __init__(self, image, listim=[]):
        ImageParent.__init__(self, image, listim)

    def addElement(self, info, newElement, place=0):
        pointer = 0
        pointer2 = 4
        counter = 0
        counter2 = place
        nbrstr = []
        print(len(newElement))
        print("nbr element max for each frame  :", len(self._binImage)*4)
        print(counter2)
        if counter2 == 0:
            for i in range(len(info)):
                self._binImage[i][3] = str(info[i])
        while counter2 < (len(newElement)):
            if pointer >= len(self._binImage):
                print(pointer2)
                pointer2 += 1
                pointer = 0
            try:
                self._binImage[pointer][pointer2] = str(newElement[counter2])
                nbrstr.append(str(newElement[counter2]))
            except:
                print("value : ",len(nbrstr))
                return counter2
            counter2 += 1
            pointer += 1
            counter += 1
        return 0
