from tess import tess
from PIL import Image
im=Image.open("test.png")
p=tess(im)
p.add_language("eng")
p.set_mode("line")
p.exec_tess()
print(p.getresult())