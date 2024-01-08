import subprocess
import os
import shutil
subprocess.run(["pip", "install", "django"])
subprocess.run(["pip", "install", "bs4"])
subprocess.run(["pip", "install", "requests"])
subprocess.run(["python","-m","pip","install", "daphne"])
subprocess.run(["python", "manage.py", "makemigrations"])
subprocess.run(["python", "manage.py", "migrate"])

curUsr = os.path.expanduser('~')
pathToDesktop = curUsr + '\\Desktop\\pharmacy.pyw'

f = open("main.pyw", "w")
f.write("import subprocess\n")
f.write("import webbrowser\n")
f.write('webbrowser.open_new("http://localhost:8000/")\n')
f.write('subprocess.run(["daphne","medical.asgi:application"])')
f.close()

f = open('Pharmacy.pyw', "w")
f.write("import subprocess\n")
f.write('subprocess.run(["python","{}"])'.format((str(os.getcwd())+"\\main.pyw")))
base_dir = str(os.getcwd()) + '\\Pharmacy.pyw'
shutil.copy(base_dir,pathToDesktop)
