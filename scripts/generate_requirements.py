import os

os.chdir('..')
os.system("pip freeze > requirements.txt")
