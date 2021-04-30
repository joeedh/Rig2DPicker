import zipfile, os, sys, os.path

zfile = zipfile.ZipFile("rig2dpick.zip", mode="w")
files = os.listdir(".")

for f in files:
  if not f.endswith(".py") or f == "make_zip.py":
    continue
  
  zfile.write(f, "rig2dpick/" + f)
  

