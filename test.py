from tess import Tess
from PIL import Image
#im=Image.open("test.png")
p = Tess()
p.load_img("test.png")
p.add_language("eng")
p.set_mode("line")
p.set_chars("abcdefg")
p.exec_tess()
print(p.getresult())
