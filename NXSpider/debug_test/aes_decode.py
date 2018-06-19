#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/5/15.
# email to LipsonChan@yahoo.com
#
import base64

from NXSpider.common.encrypt import aes_ecb, aes_ecb_decode

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(0)
unpad = lambda s: s[0:-ord(s[-1])]

aes_code = "#14ljk_!\]&0U<'("

ciphertext = "Nl7KBB481H1s6KDr+0LDleV3BNgun+wbkH1VhgrfqMPZzOZVsT3BLFqC2uS7YY09/lrsyew/bRgFclEd6cIwSf8yaE4qkrunWhZhBK3vjD32WJrHnBWhpnlUpA3YcTOyE2l8UxMYHthHFfSfhsJyxJVU9FEPNLs1RUUrVY1rXw4IunfAgYR2xZjzgDJt7pqtnJSSlrBJD8OSAiA2vrMj89KpXOSxs0dSxmwlJThnZwBgYvC+9NFwnikG+yf3We9GyTtXQGipFKgTkus+RnK/jyAEizPAO7HO5h+EgqCp1Mlddnob0oxyI0AeAhvf38ZbdnuvfvqG4XG9IhvI2Npr3J1nirpvoP5RpapGO+R42raX8fINZaS3q5nKQf8zAhjRNj8a9HHlL6sdqQfU5KaSJEyHlNeASUquFE5lsByFK9kXERkXSn1iJncZUUahRgTj6xpbVZOUCmlj8mp1VksKC/ixTXlVoSbGs8xwxuO79DkyuGeYx+K6zXUmOvlsvfAVb6Po37vhZbqZ9YEyZxPVRAH1JCPIpkJTQJA4CCJPTT+vBJ846IwwL6gjK/AIW3exkOKuKgyUb0yddP4zJixj2DRYfzUs1x+EOYBo+PYI7EgT/RQTTeYLAJwU9rbChG5Mt6IpHFxmlikMjvEgmKnnzlw0/imiqUiNFXvxEwLm6m0O/6XjmNtshdQKbROB1N5LUjt+vhxJtUsiDb2CLfDLOA=="
ciphertext = "L64FU3W4YxX3ZFTmbZ+8/W7h/5Kqax2VT/58oRU5NjAZFPGpbk27t43eUWK5m1z8cvMlvA6anlBJkkYZjrBytF6xUIqji5RKJ1g6kFzVz/lIGDPfTePng5yRmh3s77Ndg7GRhTKI+EHmY1hk5ZjJ0Q6BQ4z3zqU5O60jvv+tQI7XlsOyzC7gW/qmwCAqG4Vg1LD+PEPx+/Fj5tbgs2eAef3rWvT+Jb15HmAGq7Yz698PX9R8pRfVLUCUBFoUaJKK2O0zrblFbCEVaM4gwwiGITV2OP00qM7dYhEp5js+CInCq8C4IrncXu6V9ZBmjkyeobbi44TO9VA/oujHbF5zEDW1EVpNsillUe/zSDUXIGUWzXdYGFcz42YlJuM+VnSWL4RPI9UQUVTj30ZZPuBgmTmHmWVB8U3CKAgEV5PDiEAzyrPZ6eobHbVcmA5HsbXY0Phxvj7usONl3wOt9Yc+AaeHZyc3hzG4lVVapoXl/U2cvfVgIqVtnuJE4XM4NuUd"
ciphertext = "L64FU3W4YxX3ZFTmbZ+8/deQY+6D2ll716ETGIclcTJUqCR71zqAGY3e9XRujlth+uXXI4cnOHzmPXJ/TJUxdY5nJA95aGn5DTQPEDtkaxzlSeq5qUmAkyFZv0Z+QStPVJky2QfcU1MiYX/iVUD7SC5543s8XzFBw8XL74d8yuh8mbzaGUSMt/FMzXqV0fWQXVJexSPn18Ql8RyzN9n+lLMRsbxONXHoaum/bTgCWM5hg+4/VR1xTL465Jqb847PYODL4Uhi44BxaRz4hHmaalQ7mmw9aHiQ3v9qsrSfiQH8zKeRPNDBZLyH+E3GBt4l472tQFm0hLXa57JaskZ8aqK7wyoWkgyG7SJu8tk72hkngn99EIDE2oHy4l1iMs7iiQV2KmcPDGI1buYZoT7waSJaK9BTl7sOA86iQ1f39o5+fchTXEhl9WMyBBeS5sokCS61iuBenz5t3IGEZQ0Ci22d6mk+5joa7pefLlnOtRkSA7FZ0L7VIITat2apwn5M"
ciphertext = "wUxNl9+oaCX1+TGUoqXxPMW1W97D0rB/UWviTQG1qGf7VPc9xScpSdO78dNI29kCFN9qWTWmEEe2JvA0TgeZBdmmiikLL8RQ6zvuAfKjzTOJhL6Ff1X4hw6syUlw+wqQwRL0WQvY6ysW/OlDmqa/GHaZOirjQv580Xplu9P2wBfxW3T8HrjzPdtS05xs2Pa6JgoErDzGhmlv7ny0yYWkHqwfFtlDDlwUTAAEOXhEFI/yNE5qt4jaQABURo9ZCBoircTF92wi2BSkQHoTzDgarpOnvzmafSOR+46gt3OolILhXrtef/wPpXih9gkLrKY0"
ciphertext = "I7ZTqvekU9UjuYios3KeugpKIryhEim4OTsU7t3xaN2ZBcRHRQ0XzpsDmVa76Sh8aJ4JOmBcD37oN9sLBCkqOpoGAVROkWpNfEsYTsLz13E4Q4OIT+BBn9Acvw9CNtviGXBUyDkeec3x4RGuI6T/efUn+MntkU2ZkyyIt7VhcoV7XTFGyFx9A2UB72Tw/vn2iRXeTeS0wuAJqxJN6b9GINrizT8a+QORT7FoyPl7e4Zf8Sg4E51UnhuOGtulNc8n7MnOkbyfJSZWfHD2sHRi6g=="
plaintext = 'music:{"albumId":2084576,"alias":[],"mMusic":"{\\"fid\\":2007708232328038,\\"br\\":160000,' \
            '\\"size\\":10701396}","album":"Eternal Light","musicId":22712173,"musicName":"Refrain","mvId":0,' \
            '"duration":532000,"lMusic":"{\\"fid\\":2008807743955814,\\"br\\":96000,\\"size\\":6437585}",' \
            '"bitrate":320000,"albumPic":"http://p2.music.126.net/fNtMX44fvaGByURP0AbOZQ==/836728348761063.jpg",' \
            '"mp3DocId":1981319953261764,"artist":[["Anan Ryoko",16069]],"hMusic":"{\\"fid\\":1981319953261764,' \
            '\\"br\\":320000,\\"size\\":21359877}","albumPicDocId":836728348761063}"'
plaintext = 'music:{"musicId":28341255,"musicName":"Dancing Alone","albumId":2774171,"album":"Remove Before Flight","albumPicDocId":6025323720389239,"albumPic":"http://p1.music.126.net/w0uwPgaqDCJYYZJjzQfa7w==/6025323720389239.jpg","bitrate":320000,"mp3DocId":"69bb414114182d8e7b8a5214168bc991","duration":211200}'
plaintext = 'music:{"musicId":28341255,"musicName":"Dancing Alone",' \
            '"albumId":2774171,"album":"Remove Before Flight","albumPicDocId":6025323720389239,' \
            '"albumPic":"http://p1.music.126.net/w0uwPgaqDCJYYZJjzQfa7w==/6025323720389239.jpg",' \
            '"bitrate":320000,"mp3DocId":"69bb414114182d8e7b8a5214168bc991","duration":211200}'
plaintext = 'music:{"musicId":28341255,"musicName":"Dancing Alone",' \
            '"albumId":2774171,"album":"haha","albumPicDocId":6025323720389239,' \
            '"bitrate":320000,"mp3DocId":"69bb414114182d8e7b8a5214168bc991","duration":211200}'
# plaintext = 'music:{"musicId":28341255,"musicName":"Dancing Alone",' \
#             '"bitrate":320000}'
# plaintext = 'mv:{"title":"LATATA","mvId":5906035,"artistId":127524,' \
#             '"artistName":"Rainbow","picId":5991238859751539,"pubTime":"2013-05-17",' \
#             '"bitrate":240,"duration":258000,"briefIntro":"","detailIntro":""}'
# plaintext = 'mv:{"title":"LATATA","mvId":5906035,"artistId":14055085,' \
#             '"artistName":"(G)I-DLE","picId":109951163279867003,"pubTime":"2018-05-02",' \
#             '"bitrate":720,"duration":221000,"briefIntro":"","detailIntro":""}'

b = aes_code.encode('utf-8')
a = base64.b64decode(ciphertext)
a = aes_ecb_decode(ciphertext, aes_code)
c = aes_ecb(plaintext, aes_code)
d = c.decode()

print(d)
print(d)
