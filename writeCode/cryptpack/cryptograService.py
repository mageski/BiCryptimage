from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import numpy
from PIL import Image


class CryptograService:
    @classmethod
    def encrypt(cls, plain_text: str, password: str):
        salt = get_random_bytes(AES.block_size)
        private_key = hashlib.scrypt(
            password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
        cipher_config = AES.new(private_key, AES.MODE_GCM)
        cipher_text, tag = cipher_config.encrypt_and_digest(
            bytes(plain_text, 'utf-8'))
        return [
            b64encode(cipher_text).decode('utf-8'),
            b64encode(salt).decode('utf-8'),
            b64encode(cipher_config.nonce).decode('utf-8'),
            b64encode(tag).decode('utf-8')
        ]

    @classmethod
    def decrypt(cls, enc_dict: list, password: str):
        print(password)
        salt = b64decode(enc_dict[1])
        cipher_text = b64decode(enc_dict[0])
        nonce = b64decode(enc_dict[2])
        tag = b64decode(enc_dict[3])
        private_key = hashlib.scrypt(
            password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)
        return decrypted.decode("utf-8")

    @classmethod
    def deBinEncode(cls, listEncode: list):
        temp = ""
        counter = 0
        counterstr = 0
        temp2 = []
        code = ""
        for pointer in listEncode:
            temp += pointer
            counter += 1
            if counter >= 8:
                temp = int(temp, 2)
                charc = chr(temp)
                code += charc
                counterstr += 1
                temp = ''
                counter = 0
            if counterstr >= 24:
                temp2.append(code)
                code = ''
                counterstr = 0
        return temp2

    @classmethod
    def binEncode(cls, listEncode: list):
        temp = []
        binValue = []
        for bits in range(len(listEncode)):
            binary = bytearray(listEncode[bits], "utf8")
            print("setencde mess:", binary)
            for bit in binary:
                temp.append(format(bit, '08b'))
            binValue.append(temp)
            temp = []
        binValue = binValue[0] + binValue[1] + binValue[2]
        return binValue

    @classmethod
    def reconstructSneak(cls, image: list, shape: list, location):
        if len(shape) == 2:
            newImage = numpy.reshape(image, (shape[0], shape[1]))
            imgSneak = Image.fromarray(
                (newImage).astype('uint8'), 'L').save(location)
            return imgSneak
        else:
            newImage = numpy.reshape(image, (shape[0], shape[1], shape[2]))
        if shape[2] == 4:
            imgSneak = Image.fromarray(
                (newImage).astype('uint8'), 'RGBA').save(location)
        elif shape[2] == 3:
            imgSneak = Image.fromarray(
                (newImage).astype('uint8'), 'RGB').save(location)
        else:
            imgSneak = Image.fromarray(
                (newImage).astype('uint8')).save(location)
        return imgSneak

    @classmethod
    def longEncodeBin(cls, longBin):
        temp = []
        print(longBin)
        for bit in longBin:
            temp.append(format(ord(bit), '08b'))
        return temp

    @classmethod
    def deBinDecode(cls, bytesText: list):
        try:
            decodedText = ""
            for i in bytesText:
                decodedText += i.decode('UTF-8')
            type = "Utft"
        except:
            decodedText = ""
            for i in bytesText:
                decodedText += i.decode('ISO-8859-1')
            type = 'Isot'
        return [decodedText, type]

    @classmethod
    def trasnformMess(cls, message, type):
        print(type)
        if type == "Text" or type == "Utft" or type == "Isot":
            messagedec = ""
            print("longeur = ", len(message))
            for i in range(len(message)):
                temp = "".join(message[i])
                temp = int(temp, 2)
                charc = chr(temp)
                messagedec += charc
        else:
            messagedec = []
            for i in range(len(message)):
                temp = "".join(message[i])
                temp = int(temp, 2)
                messagedec.append(temp)
        return messagedec
