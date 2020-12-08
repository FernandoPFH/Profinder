@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
chcp 65001

set removeBootstrap="<link rel=""stylesheet"" href=""assets/bootstrap/css/bootstrap.min.css"">"
set removeUntilted="<link rel=""stylesheet"" href=""assets/css/untitled.css"">"
set removeJQuery="<script src=""assets/js/jquery.min.js""></script>"
set removeBootstrap2="<script src=""assets/bootstrap/js/bootstrap.min.js""></script>"
set removeSummernote="<script src=""http://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.12/summernote.js""></script>"
set removeLogin="<script src=""assets/js/Login.js""></script>"
set removeMyAccount="<script src=""assets/js/MyAccount.js""></script>"
set removeMyProject="<script src=""assets/js/MyProject.js""></script>"
set removeSignup="<script src=""assets/js/Signup.js""></script>"
set removeTestIfLoged="<script src=""assets/js/TestIfLoged.js""></script>"

set filesToRemove=%removeBootstrap% %removeUntilted% %removeJQuery% %removeBootstrap2% %removeSummernote% %removeLogin% %removeMyAccount% %removeMyProject% %removeSignup% %removeTestIfLoged%

set fileData=
set lineData=

FOR /F "tokens=* delims=" %%x in (.\Testes\CreateProject.html) DO (
    for %%a in (%filesToRemove%) do ( 
        set lineData=%%x:%%a=%%
    )

    set fileData=%fileData%%lineData%
)

echo %fileData%