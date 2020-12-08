var ProjectCode; 
$(document).ready(() => {
    ProjectCode = document.getElementById("ProjectCode").innerHTML;
    
    Data = {"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"ProjectCode":ProjectCode,"Titulo":-1,"Area":-1,"UserCode":-1,"Publicado":-1}
    
    fetch('/send_data_for_projects/'+JSON.stringify(Data), {
        method: 'GET',
    }).then((response) => {
        return response.json();
    }).then((data) => {
        // Work with JSON data here
        if (data.Aceito) {
            if (data.Projetos[0].IsYourCode) {
                document.getElementById("Titulo").innerHTML = data.Projetos[0].Titulo;
                if (data.Projetos[0].Image != null) {
                    document.getElementById("ItemPreview").src = data.Projetos[0].Image;
                }

                for (let i = 0; i<data.Projetos[0].Areas.length;i++) {
                    document.getElementById('Areas').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center AreaEscolhida" style="padding-right: 5px;"><p>${data.Projetos[0].Areas[i]}</p></div>`;
                }
            
                for (let i = 0; i<data.Projetos[0].Users.length; i++) {
                    document.getElementById('Membros').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido ${data.Projetos[0].Users[i][1]}" data-toggle="tooltip" title="UserCode: ${data.Projetos[0].Users[i][2]}" style="padding-right: 5px;"><div><p>${data.Projetos[0].Users[i][0]}</p></div></div>`;
                }
                
                document.getElementById("ProjectDesc").innerHTML = data.Projetos[0].Descr;
            } else {
                if (data.Projetos[0].Publicado) {
                    let editButton = document.getElementById("EditButton");
                    editButton.parentNode.removeChild(editButton);
                    document.getElementById("TituloOfProject").style.margin = "46px 0px 20px 27px";
                    document.getElementById("Titulo").innerHTML = data.Projetos[0].Titulo;
                    if (data.Projetos[0].Image != null) {
                        document.getElementById("ItemPreview").src = data.Projetos[0].Image;
                    }

                    for (let i = 0; i<data.Projetos[0].Areas.length;i++) {
                        document.getElementById('Areas').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center AreaEscolhida"><p>${data.Projetos[0].Areas[i]}</p></div>`;
                    }

                    for (let i = 0; i<data.Projetos[0].Users.length; i++) {
                        document.getElementById('Membros').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido ${data.Projetos[0].Users[i][1]}" data-toggle="tooltip" title="UserCode: ${data.Projetos[0].Users[i][2]}"><div><p>${data.Projetos[0].Users[i][0]}</p></div></div>`;
                    }
                    document.getElementById("ProjectDesc").innerHTML = data.Projetos[0].Descr;
                } else {
                    document.getElementById("ProjectHoleDiv").innerHTML = "<strong style=\"color: rgb(0,0,0);font-size: 100px;\">404 Not Found</strong>"
                }
            }
        } else {
            document.getElementById("ProjectHoleDiv").innerHTML = "<strong style=\"color: rgb(0,0,0);font-size: 100px;\">404 Not Found</strong>"
        }
    });
});

function EditProject() {
    location.href="/create_project/"+ProjectCode;
}