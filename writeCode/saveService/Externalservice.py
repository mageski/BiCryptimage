from vidgear.gears import VideoGear
import cv2

class SaveReadService:
    @classmethod
    def saveText(cls, text, file):
        with open(file, "w+", encoding="utf-8") as fichier:
            fichier.write(text)

    @classmethod
    def saveOther(cls, text, file):
        with open(file, "wb") as fichier:
            fichier.write(text)

    @classmethod
    def takeText(cls, file):
        text = ""
        with open(file, 'r', encoding="utf-8") as fichier:
            for line in fichier.readlines():
                text += line.strip() + '\n'
        return text

    @classmethod
    def takeOther(cls, file):
        f = []
        extension = ""
        with open(file, 'r+b') as fichier:
            for i in reversed(fichier.name):
                extension += i
                if i == ".":
                    break
            for line in fichier.readlines():
                f.append(line)
        return [f, extension[::-1]]

    @classmethod
    def TakeVide(cls, ficher, conversion):
        x = []
        cap = VideoGear(source=ficher).start()
        fps = cap.framerate
        print(fps)
        count = 0
        while True:
            frame = cap.read()
            if frame is None:
                break
            x.append(frame)
        cap.stop()
        return x, fps
