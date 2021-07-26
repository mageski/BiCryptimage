from cryptpack.CryptograService import CryptograService
from sneakmessage import SneakMessage

message = input ("message :" )
mdp = input("password : ")
cryptoMess = CryptograService.encrypt(message, mdp)
mesg = SneakMessage(cryptoMess)
info = mesg.setInfo()
element = mesg.getbin()
messEncode = mesg.setmessEncode()
print(messEncode[2])
messEncode = "".join(messEncode)
temp = ""
counter = 0
counterstr = 0
temp2 = []
code = ""
for pointer in messEncode:
    temp += pointer
    counter += 1
    if counter >= 8 :
        temp = int(temp,2)
        charc = chr(temp)
        code += charc
        counterstr += 1
        temp = ''
        counter = 0
    if counterstr >= 24:
        temp2.append(code)
        code = ''
        counterstr = 0
print("temp2 :",temp2)
