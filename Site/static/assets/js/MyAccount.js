var UserCode;
$(document).ready(() => {
    UserCode = document.getElementById("UserCode").innerHTML;

    window.onclick = function(event) {
      var modal = document.getElementById("myModal");
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
    
    Data = {"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"UserCode":UserCode}
    
    fetch('/send_data_for_account/'+JSON.stringify(Data), {
      method: 'GET',
    }).then((response) => {
      return response.json()
    }).then((data) => {
        if (data.IsYourCode) {
            document.getElementById("Email").value = data.Email
            document.getElementById("Password").value = data.Password
            document.getElementById("Name").value = data.Name
              if (data.Image != null) {
                document.getElementById("ItemPreview").src = data.Image;
                document.getElementById("ChangeItemPreview").src = data.Image;
              }

              Data = {"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"Titulo":-1,"Area":-1,"ProjectCode":-1,"Publicado":-1}

            fetch('/send_data_for_projects/'+JSON.stringify(Data), {
              method: 'GET',
            }).then((response) => {
              return response.json()
            }).then((data) => {
                if (data.Aceito) {
                    var table = document.getElementById("myProjectsTable");

                    let i;
                    for (i = 0; i < data.Projetos.length; i++) {
                        let dataForRow = data.Projetos[i];
                        let row = table.insertRow(-1);

                        let cell1 = row.insertCell(0);
                        let cell2 = row.insertCell(1);

                        cell1.innerHTML = `<a href="/project/${dataForRow.ProjectCode}">${dataForRow.Titulo}</a>`;
                        if (dataForRow.Publicado) {
                            cell2.innerHTML = `<input type='checkbox' checked/>`
                        } else {
                            cell2.innerHTML = `<input type='checkbox' />`
                        }
                    }

                    document.getElementById("semNenhumProjeto").remove();

                    document.getElementById("MyProjectsContainer").innerHTML += `<div class="d-xl-flex flex-row justify-content-xl-center align-items-xl-center"><p style="color: rgb(0,0,0);margin-bottom: 0px;">Criar Novo Projeto</p><button class="btn btn-primary d-xl-flex justify-content-xl-center align-items-xl-center" type="button" style="height: 24px;width: 24px;margin-left: 7px;" onclick="window.location.href = '/create_project/new'">+</button></div>`
                }
            });
        } else {
            let changeButton = document.getElementById("ChangeButton");
            changeButton.parentNode.removeChild(changeButton);
            let myModal = document.getElementById("myModal");
            myModal.parentNode.removeChild(myModal);
            let myOverlay = document.getElementsByClassName("overlay").item(0);
            myOverlay.parentNode.removeChild(myOverlay);
            
            let emailParent = document.getElementById("Email").parentNode;
            emailParent.removeChild(document.getElementById("Email"));
            emailParent.innerHTML = emailParent.innerHTML + `<p id=\"Email\" style=\"width: 232px;margin-left: 50px;color: rgb(0,0,0);\">${data.Email}</p>`;
            
            let passwordParent = document.getElementById("Password").parentNode;
            passwordParent.parentNode.removeChild(passwordParent);
            
            let nameParent = document.getElementById("Name").parentNode;
            nameParent.removeChild(document.getElementById("Name"));
            nameParent.innerHTML = nameParent.innerHTML + `<p id=\"Name\" style=\"width: 232px;margin-left: 50px;color: rgb(0,0,0);\">${data.Name}</p>`;
            
            if (data.Image != null) {
              document.getElementById("ItemPreview").src = data.Image;
            }
            
            let tableCellPublicado = document.getElementById("Publicado");
            tableCellPublicado.parentNode.removeChild(tableCellPublicado);
            
            document.getElementById("noProjectsParagraph").innerHTML = "Ainda não há nenhum projecto";
            let noProjectsLink = document.getElementById("noProjectsLink");
            noProjectsLink.parentNode.removeChild(noProjectsLink);
            
            Data = {"UserCode":UserCode,"Titulo":-1,"Area":-1,"ProjectCode":-1,"Publicado":1}
          
            fetch('/send_data_for_projects/'+JSON.stringify(Data), {
              method: 'GET',
            }).then((response) => {
              return response.json()
            }).then((data) => {
                if (data.Aceito) {
                    var table = document.getElementById("myProjectsTable");

                    let i;
                    for (i = 0; i < data.Projetos.length; i++) {
                        let dataForRow = data.Projetos[i];
                        let row = table.insertRow(-1);

                        let cell1 = row.insertCell(0);
                        let cell2 = row.insertCell(1);
                        let cell3 = row.insertCell(2);

                        cell1.innerHTML = dataForRow.Titulo;
                        cell2.innerHTML = dataForRow.Area;
                        cell3.innerHTML = `<a href="/project/${dataForRow.ProjectCode}">Click Aqui</a>`
                    }

                    document.getElementById("semNenhumProjeto").remove();

                }
            });
        }
    });
});

function ChangeAccountData() {
  User = {"Email":document.getElementById("Email").value,"Password":document.getElementById("Password").value,"Name":document.getElementById("Name").value,"Type":"prof","sessionishClientId":sessionStorage.getItem("sessionishClientId")};

  fetch('/send_data_for_account/'+JSON.stringify(User), {
    method: 'POST',
  }).then((response) => {
    return response.json()
  }).then((data) => {
    // Work with JSON data here
    if(data.Aceito){
      alert("Infos Mudadas")
      location.reload()
    }else{
      alert(data.Porque)
    }
  });
}

function ChangeImagePopUp() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

function ChangeImageData() {
    const IP = "127.0.0.1";
    const PORT = 5100;
    var file = document.getElementById('FileToGet').files[0];
    var fileReader = new FileReader();
    fileReader.readAsDataURL(file)
    fileReader.onload = () => {
        var arrayBuffer = fileReader.result;

        var socket = io.connect(`http://${IP}:${PORT}`);

        socket.on('Response', (data)=>{
          data.sessionishClientId = sessionStorage.getItem("sessionishClientId");
          data.updateProjectImage = 0;
            fetch('/update_image_account_data/'+JSON.stringify(data), {
                method: 'POST',
            }).then((response) => {
                return response.json();
            }).then((dataresponse) => {
                // Work with JSON data here
                if(dataresponse.Aceito){
                    alert("Foto Mudadas");
                    location.reload()
                }else{
                    alert(dataresponse.Porque);
                    
                    var info = {
                        filename :  data.filename 
                    };
                    
                    socket.emit("ImageDelete",info);
                }
            });
        });

        var ImageSendData = {
            filename: file.name,
            filedata: arrayBuffer
        }

        socket.emit('ImageSend', ImageSendData);
    }
}

function CloseImagePopUp() {
    document.getElementById("myModal").style.display = "none";
}