# autopep8: off
import argparse
import MainShortcuts as ms
import os
import requests
import signal
import subprocess
import sys
from . import __version__,__version_tuple__
from flask import Response
from hashlib import sha256
from random import *
from time import sleep
from threading import Thread
from typing import Union
http_codes={}
for k,v in requests.codes.__dict__.items():
  if not v in http_codes:
    http_codes[v]=k
services={}
class service:
  def __init__(self,path:str,password:str=None):
    self.closed=False
    self.enabled=False
    self.pid=None
    self.process=None
    if path=="admin":
      self.path=None
      self.name="admin"
    else:
      self.path=os.path.abspath(path)
      self.name=os.path.basename(self.path)
      if password==None:
        self.password=randbytes(16).hex()
      else:
        self.password=password
      try:
        self.read()
      except:
        self.close()
  def read(self,**kw):
    kw["path"]=self.path
    self.data=ms.json.read(**kw)
  def write(self,**kw):
    if not "mode" in kw:
      kw["mode"]="p"
    kw["data"]=self.data
    kw["path"]=self.path
    return ms.json.write(**kw)
  def reload(self):
    try:
      self.read()
    except:
      self.close()
  def close(self,kill:bool=False):
    while self.process:
      if kill:
        self.kill()
      else:
        self.stop()
        sleep(10)
        self.kill()
    for k in dir(self):
      if not k.startswith("__"):
        try:
          delattr(self,k)
        except:
          pass
    self.closed=True
  def enable(self,*,threaded=False):
    if self.process:
      return
    if not threaded:
      return Thread(target=self.enable,kwargs={"threaded":True}).start()
    self.enabled=True
    self.start(threaded=True)
    self.code=self.process.wait()
    self.process=None
    self.pid=None
    if not self.enabled:
      return
    if self["restart"]=="always":
      return self(threaded=True)
    if self["restart"]=="on_error":
      if self.code!=0:
        return self(threaded=True)
    self.enabled=False
  def disable(self):
    if self.enabled:
      self.enabled=False
      self.stop()
  def __call__(self,*args,**kw):
    return self.enable(*args,**kw)
  def __getitem__(self,k):
    return self.data.get(k)
  def __setitem__(self,k,v):
    self.data[k]=v
  def __hasitem__(self,k):
    return k in self.data
  def start(self,threaded=False,**kw):
    if self.process:
      return
    if not threaded:
      return Thread(target=self.start,kwargs={"threaded":True}).start()
    kw["args"]=self.data["args"]
    kw["stderr"]=subprocess.DEVNULL
    kw["stdin"]=subprocess.DEVNULL
    kw["stdout"]=subprocess.DEVNULL
    if self["cwd"]:
      kw["cwd"]=os.path.abspath(self.data["cwd"]).replace("\\","/")
    if self["env"]:
      if self["clean_env"]:
        kw["env"]={}
      else:
        kw["env"]=os.environ.copy()
      kw["env"].update(self["env"])
    if self["user"]:
      if hasattr(os,"setreuid"):
        kw["user"]=self["user"]
    if self["group"]:
      if hasattr(os,"setregid"):
        kw["group"]=self["group"]
    if self["extra_groups"]:
      if hasattr(os,"setgroups"):
        kw["extra_groups"]=self["extra_groups"]
    self.process=subprocess.Popen(**kw)
    self.pid=self.process.pid
    if self["data_path"]:
      ms.json.write(self["data_path"],self.to_dict())
  def restart(self,kill=False):
    while self.process:
      if kill:
        self.kill()
      else:
        self.stop()
    self.start()
  def send_signal(self,sig:int):
    if self.process:
      self.process.send_signal(sig)
  def stop(self):
    self.send_signal(signal.SIGINT)
  def kill(self):
    self.send_signal(signal.SIGKILL)
  def to_dict(self)->dict:
    return {"name":self.name,"path":self.path,"pid":self.pid,"password":self.password,"data":self.data}
  def to_json(self,**kw)->str:
    return ms.json.encode(self.to_dict(),**kw)
def cfg_load(path:str=os.path.expanduser("~/.config/MainServiceManager/cfg.json"))->ms.cfg:
  cfg=ms.cfg(path,type="json")
  cfg.default={
    "host":"127.0.0.1",
    "password":"",
    "port":8960,
    "services_dir":os.path.dirname(cfg.path).replace("\\","/")+"/services",
    }
  cfg.dload()
  ms.dir.create(cfg["services_dir"])
  ms.dir.create(os.path.dirname(cfg.path))
  if not ms.path.exists(cfg.path):
    print("Created a config file with default settings",file=sys.stderr)
    cfg.save()
  return cfg
def cfg_save(cfg:ms.cfg)->str:
  dont_save=[]
  d={}
  for i in dont_save:
    d[i]=cfg.data.pop(i)
  cfg.save()
  for i in dont_save:
    cfg[i]=d[i]
  return cfg.path
def get_args(**kw)->argparse.Namespace:
  kw["description"]=f"MainServiceManager {__version__}"
  kw["epilog"]="Creator: MainPlay_TG\nContact: https://t.me/MainPlay_TG\nMade in Russia"
  kw["formatter_class"]=argparse.RawTextHelpFormatter
  kw["prog"]="MSVC-server"
  argp=argparse.ArgumentParser(**kw)
  argp.add_argument("-v","--version",
    action="store_true",
    help="print the version and exit",
    )
  argp.add_argument("-c","--config",
    default=None,
    help="config file",
    )
  return argp.parse_args()
def auth_header(user:str,password:str="")->str:
  if type(user)==service:
    password=user.password
    user=user.name
  return "Basic "+":".join([user,sha256(password.encode("utf-8")).hexdigest()])
def auth(cfg,request)->Union[bool,list]:
  if "Authorization" in request.headers:
    if request.headers["Authorization"]==auth_header("admin",cfg["password"]):
      return "admin"
    for k,v in services.items():
      if request.headers["Authorization"]==auth_header(v):
        return v.name
  else:
    return False
def access(user:str,svc:Union[str,service])->bool:
  if user=="admin":
    return True
  if type(svc)==service:
    svc=svc.name
  return user==svc
def make_r(data:dict={},code:int=200,status:str=None,**kw)->Response:
  if status==None:
    if code in http_codes:
      status=http_codes[code]
  d={
    "code":code,
    "data":data,
    "server":{"name":"MainServiceManager","version":__version_tuple__},
    "status":status,
    }
  kw["status"]=code
  kw["content_type"]="application/json"
  kw["response"]=ms.json.encode(d)
  r=Response(**kw)
  # r.headers["Content-Type"]="application/json; charset=utf-8"
  return r
def check_port(cfg:ms.cfg):
  try:
    if cfg["host"]=="0.0.0.0":
      host="127.0.0.1"
    else:
      host=cfg["host"]
    port=cfg["port"]
    requests.request("GET",f"http://{host}:{port}/admin/status")
    raise OSError("It was not possible to launch the server at {host}:{port}".format(host=cfg["host"],port=cfg["port"]))
  except requests.exceptions.ConnectionError:
    return True
