# 本代码用于编译当前目录下所有py文件(包括它本身)
import os,compileall

path = os.getcwd()
compileall.compile_dir( dir = path, force = True)