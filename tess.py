import tempfile
import subprocess
from PIL import Image
class tess:
    def __init__(self,img,tessdir=""):
        self.tessdir=tessdir
        self.img=img
        self.lang=[]
        self.addconf=False
        self.mode=False
        self.result=""
        if tessdir=="":
            self.find_exec()
        else:
            self.tessdir=tessdir
        self.tessdir+="\\"
        self.init_workdir()
        self.prepare_img()
    
    def prepare_img(self):
        self.imgdir=self.workdir+"img.bmp"
        self.img.save(self.imgdir)

    def init_workdir(self):
        self.temp=tempfile.TemporaryDirectory("","tessocr-")
        self.workdir=self.temp.name+'\\'

    def find_exec(self):
        f=open("path.txt",mode='r')
        cur=f.readline()
        while self.tessdir=="" and cur!="":
            try:
                cur=cur[0:cur.index('\n')]
                f1=open(cur+"\\tesseract.exe",mode='rb')
                f1.close()
            except:
                cur=f.readline()
                continue
            self.tessdir=cur
        if self.tessdir=="":
            raise RuntimeError("Cannot find tess executable!")
        f.close()
    
    def add_language(self,lang):
        self.lang.append(lang)
    
    def set_chars(self,charset):
        self.addconf=True
        self.confpath=self.workdir+"tessconf"
        chars="tessedit_char_whitelist "+charset
        try:
            wconf=open(self.confpath,mode='w')
            wconf.write(chars)
            wconf.write("\n")
        finally:
            wconf.close()
    
    def set_mode(self,mode):
        self.mode=True
        if mode=="word":
            self.modenum="8 "
        elif mode=="line":
            self.modenum="7 "

    def call(self,cmd):
        print(cmd)
        self.process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE
            )
        self.result=self.process.stdout.read()
    
    def getresult(self):
        try:
            self.result=self.result.decode('utf8')
        finally:
            return self.result
    
    def parse_cmd(self):
        self.cmd='"'+self.tessdir+"tesseract.exe"+'" '
        self.cmd+=self.imgdir
        self.cmd+=" stdout "
        if self.lang.count!=0:
            self.cmd+=" -l "
            for lang in self.lang:
                self.cmd+=lang
                self.cmd+="+"
            self.cmd=self.cmd[0:-1]+" "
        if self.mode:
            self.cmd+="--psm "
            self.cmd+=self.modenum
        if self.addconf:
            self.cmd+=self.confpath

    def exec_tess(self):
        self.parse_cmd()
        self.call(self.cmd)