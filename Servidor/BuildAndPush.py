from os import path,system
from subprocess import check_output

check_output("RemoveImages.bat",shell=True)

username = "fernandopfh"
version ="1.0.0"

filecontent = ""

nextlinehastitle = False

with open(path.join(path.dirname(path.realpath(__file__)),"testes-docker-compose.yml"), "r") as file:
    for line in file:

        if "build:" in line:
            imagePath = line.replace("build: ","").replace("\t","").replace("./","").replace("\\","/").strip() + '/'

            dockerfilepath = path.join(path.realpath(__file__).replace("\\BuildAndPush.py","").replace("\\","/"),imagePath.replace('./',''))

            system(f'docker build --tag {username}/{tagname}:{version} "{dockerfilepath}/"')

            system(f"docker push {username}/{tagname}:{version}")

            line = f"{' '*4}image: {username}/{tagname}:{version}\n"

        tagname = line.replace('\t','').replace(':','').strip()

        filecontent += line

with open("docker-compose.yml","w") as file:
    file.write(filecontent)
