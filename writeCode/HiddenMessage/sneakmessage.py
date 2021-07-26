from .hiddenmes import HiddenMes


class SneakMessage(HiddenMes):
    def __init__(self, message, typeMes):
        self._message = message
        self._type = typeMes
        self._bin = []
        self._messEncodeBin = []

    def setbin(self):
        if self._type == "Text":
            for bit in self._message:
                self._bin.append(format(ord(bit), '08b'))
        elif self._type == "Bina":
            self._bin = self._message
        else:
            print("erreur de message ou message non pris en charge")

    def getbin(self):
        return super().getbin()

    def setType(self, imType):
        self._type = imType

    def getInfo(self):
        binary = bytearray(self._type, "utf8")
        long = len(self._bin)
        long = bin(long)[2:]
        bin64 = 64 * ['0']
        del bin64[64 - len(long):64]
        information = []
        pointer = 0
        for bit in binary:
            information.append(bin(bit)[2:])
        while pointer < len(long):
            bin64.append(long[pointer])
            pointer += 1
        bin64 = "".join(bin64)
        information.append(bin64)
        return information

    def addEncode(self, info, encode):
        for i in encode:
            info += i
        return info

    def extensionBin(self, ext):
        extBin = ""
        for bit in ext:
            extBin += (format(ord(bit), '08b'))
        return extBin

    def longExtBin(self, ext):
        return format(len(ext), '08b')
