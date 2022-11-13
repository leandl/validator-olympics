from os import path, mkdir
import shutil
import json
import sys

from entities.config import Config
from entities.generator_file.generator_javascript_file import GeneratorJavascriptFile
from entities.generator_file.generator_python_file import GeneratorPythonFile
from entities.generator_file.generator_php_file import GeneratorPHPFile

questions = []
if not path.isfile(Config.file["JSON-DATA"]):
  print("Não foi encotrado o arquivo data.json")
  sys.exit(0)
  

with open(Config.file["JSON-DATA"]) as file:
  questions = json.load(file)

generator_file = GeneratorPHPFile(Config.path["TEMPLATES"])

if path.isdir(Config.path["EXAM"]):
  print("removendo arquivos antigos...")
  shutil.rmtree(Config.path["EXAM"])


print("criando a pasta exam...")
mkdir(Config.path["EXAM"])

for index, question in enumerate(questions):
  name_file, content_file = generator_file.generate(index + 1, question)
  path_file_question = path.join(Config.path["EXAM"], name_file)


  with open(path_file_question, "w") as file:
    file.write(content_file)
  