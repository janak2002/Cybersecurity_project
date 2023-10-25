from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

#
salt = b'\xa6\n\x14\xc8l\x124\xb2\xa6\xcd\xf1\x7f\x95 \xe9d\x7fN1H\\\xd8\r\xad\x1e\xfd\xbc\xaf\x85\xcf\xc28'
password='mydoglili'

key=PBKDF2(password,salt,32)
message = b"j.klaric@student.utwente.nl"
print(key)
cipher = AES.new(key,AES.MODE_CBC)
ciphered_data=cipher.encrypt(pad(message,AES.block_size))

with open ('encrypted.bin','wb') as f:
    f.write(cipher.iv)
    #f.write(b'\n')
    f.write(ciphered_data)

with open ('encrypted.bin','rb') as f:
    iv=f.read(16)
    decrypt_data=f.read()

cipher=AES.new(key,AES.MODE_CBC,iv=iv)
original=unpad(cipher.decrypt(decrypt_data),AES.block_size)

print(original)