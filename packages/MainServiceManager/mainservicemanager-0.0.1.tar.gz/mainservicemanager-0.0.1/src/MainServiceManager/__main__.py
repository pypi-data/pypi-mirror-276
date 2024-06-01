# autopep8: off
import os
import sys
import subprocess
__dir__=os.path.dirname(__file__)
def server_start():
  p=subprocess.Popen([sys.executable,__dir__+"/server.py"])
  try:
    return p.wait()
  except:
    pass