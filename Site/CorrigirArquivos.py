from os import path, listdir, rename, remove
from shutil import move, rmtree

#Esvaziar a pasta de backup
pastaBackup = path.join(path.dirname(path.realpath(__file__)),"Backup")
arquivosEmBackup = [path.join(pastaBackup, nome) for nome in listdir(pastaBackup) if path.isfile(path.join(pastaBackup, nome))]

if len(arquivosEmBackup) > 0:
    for arquivoEmBackup in arquivosEmBackup:
        remove(arquivoEmBackup)

pastaEmBackup = path.join(path.join(path.dirname(path.realpath(__file__)),"Backup"),"assets")
if(path.exists(pastaEmBackup)):
    rmtree(pastaEmBackup)

#Mover arquivos atuais
pastaTemplatesAtuais = path.join(path.dirname(path.realpath(__file__)),"templates")
templatesAtuaisPath = [path.join(pastaTemplatesAtuais, nome) for nome in listdir(pastaTemplatesAtuais) if path.isfile(path.join(pastaTemplatesAtuais, nome))]

for templateAtualPath in templatesAtuaisPath:
    rename(templateAtualPath,templateAtualPath.replace("\\templates\\","\\Backup\\"))

pastaAssetsAtual = path.join(path.join(path.dirname(path.realpath(__file__)),"static"),"assets")
if(path.exists(pastaAssetsAtual)):
    move(pastaAssetsAtual,pastaAssetsAtual.replace("\\static\\","\\Backup\\"))

#Editar novos arquivos
linhasASeremRetiradas = [
    b'<link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">',
    b'<link rel="stylesheet" href="assets/css/untitled.css">',
    b'<script src="assets/js/EditProject.js"></script>',
    b'<script src="http://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.12/summernote.js"></script>'
    b'<script src="assets/js/jquery.min.js"></script>',
    b'<script src="assets/bootstrap/js/bootstrap.min.js"></script>',
    b'<script src="assets/js/Login.js"></script>',
    b'<script src="assets/js/MyAccount.js"></script>',
    b'<script src="assets/js/Project.js"></script>',
    b'<script src="assets/js/Projects.js"></script>',
    b'<script src="assets/js/Signup.js"></script>',
    b'<script src="assets/js/TestIfLoged.js"></script>',
    b'<script src="assets/js/SearchBar.js"></script>'
]

linhasASeremSubstituidas = [
    [b'assets/img/',b'/static/assets/img/']
]

pastaTestes = path.join(path.dirname(path.realpath(__file__)),"Testes")
arquivosNovosPath = [path.join(pastaTestes, nome) for nome in listdir(pastaTestes) if path.isfile(path.join(pastaTestes, nome))]

for arquivoNovoPath in arquivosNovosPath:
    with open(arquivoNovoPath, "rb+") as file:
        linhasLidas = file.readlines()
        conteudoDoArquivo = b""

        for linhaLida in linhasLidas:
            for linhaASerRetirada in linhasASeremRetiradas:
                if linhaASerRetirada in linhaLida:
                    linhaLida = linhaLida.replace(linhaASerRetirada,b"")

            for linhaASerSubstituida in linhasASeremSubstituidas:
                if linhaASerSubstituida[0] in linhaLida:
                    linhaLida = linhaLida.replace(linhaASerSubstituida[0],linhaASerSubstituida[1])

            conteudoDoArquivo += linhaLida

        file.seek(0)
        file.write(conteudoDoArquivo)
        file.truncate()

#Mover arquivos novos
for arquivoNovoPath in arquivosNovosPath:
    rename(arquivoNovoPath,arquivoNovoPath.replace("\\Testes\\","\\templates\\"))

pastaAssetsAtual = path.join(path.join(path.dirname(path.realpath(__file__)),"Testes"),"assets")
move(pastaAssetsAtual,pastaAssetsAtual.replace("\\Testes\\","\\static\\"))