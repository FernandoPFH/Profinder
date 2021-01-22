var publicado = 0;
var possibilidadesDeAreas = [];
var escolhidasDeAreas = [];
var possibilidadesDeMembros = [];
var escolhidasDeMembros = [];

$(document).ready(async function() { $('#summernote').summernote({
  tabsize: 2,
  height: $('#summernote').height() - 53,
  width: "90%"
  });

  window.onclick = function(event) {
    var modal = document.getElementById("myModal");
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  var $body = $('body');
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.attributeName === "class") {
        if ($(mutation.target).prop(mutation.attributeName).includes("modal-open")) {
          let modalbg = document.getElementsByClassName("modal-backdrop show")[0];
          modalbg.parentElement.removeChild(modalbg);
          $('#summernote').next().prepend(modalbg);
        }
      }
    });
  });
  observer.observe($body[0], {
    attributes: true
  });

  document.getElementById('Area').addEventListener('input', () => {
      document.getElementById('criarnovaarea').value = document.getElementById('Area').value + " ";
  });
  
  document.getElementById('Area').addEventListener('change', () => {
  
      let value = document.getElementById('Area').value;
  
      if (value[value.length-1] == " ")
          value = value.substring(0, value.length - 1);
  
      escolhidasDeAreas.push(value);
  
      let index = possibilidadesDeAreas.indexOf(value);
  
      if (index > -1) {
          possibilidadesDeAreas.splice(index, 1);
      }
  
      document.getElementById('Areas').innerHTML = document.getElementById('Areas').innerHTML.replace(`<option value="${value}"></option>`);
      document.getElementById('AreasEscolhidas').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center AreaEscolhida"><p>${value}</p><a class="d-flex" href="#" onclick="removeArea(this)">X</a></div>`
      
      document.getElementById('Area').value = "";
      document.getElementById('criarnovaarea').value = "";
  });

  document.getElementById('Membro').addEventListener('change', () => {

      let code = document.getElementById('Membro').value.replace("UserCode: ","");
      let item;
      for (let i = 0;i<possibilidadesDeMembros.length;i++) {
        if (possibilidadesDeMembros[i].indexOf(code) > -1) {
          item = possibilidadesDeMembros[i];
          possibilidadesDeMembros.splice(i,1);
        }
      }

      escolhidasDeMembros.push(item);

      document.getElementById('Membros').innerHTML = document.getElementById('Membros').innerHTML.replace(`<option value="UserCode: ${item[2]}">${item[0]}</option>`);
      document.getElementById('MembrosEscolhidos').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido ${item[1]}" data-toggle="tooltip" title="UserCode: ${item[2]}"><div><p>${item[0]}</p></div><a class="d-flex" href="#" onclick="removeMembro(this)">X</a></div>`

      document.getElementById('Membro').value = "";
  });

  await fetch('/send_data_for_projectssideinfos/', {
        method: 'GET',
      }).then((response) => {
        return response.json();
      }).then((data) => {
        // Work with JSON data here
        if (data.Aceito) {
            possibilidadesDeAreas = data.Areas;
        }
    });

  await fetch('/send_data_for_userssideinfos/', {
        method: 'GET',
      }).then((response) => {
        return response.json();
      }).then((data) => {
        // Work with JSON data here
        if (data.Aceito) {
          possibilidadesDeMembros = data.Users;
        }
    });

    let selfUserCode;

    let Dados = {"sessionishClientId":sessionStorage.getItem("sessionishClientId")}

    await fetch('/send_data_for_account/'+JSON.stringify(Dados), {
          method: 'GET',
        }).then((response) => {
          return response.json();
        }).then((data) => {
          // Work with JSON data here
          if (data.Aceito) {
            selfUserCode = data.UserCode;
          }
      });

  if (ProjectCode != "new") {
      document.getElementById("Title").innerHTML = "Editar Projeto";

      Data = {"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"ProjectCode":ProjectCode,"Titulo":-1,"Area":-1,"UserCode":-1,"Publicado":-1}

      fetch('/send_data_for_projects/'+JSON.stringify(Data), {
        method: 'GET',
      }).then((response) => {
        return response.json();
      }).then((data) => {
        // Work with JSON data here
        if (data.Projetos[0].IsYourCode) {
            document.getElementById("Titulo").value = data.Projetos[0].Titulo;
            $('#summernote').summernote('code',data.Projetos[0].Descr);
            publicado = data.Projetos[0].Publicado;

            if (data.Projetos[0].Image != null) {
              document.getElementById("ItemPreview").src = data.Projetos[0].Image;
              document.getElementById("ChangeItemPreview").src = data.Projetos[0].Image;
            }
            
            for (let i = 0; i<data.Projetos[0].Areas.length;i++) {
                let index = possibilidadesDeAreas.indexOf(data.Projetos[0].Areas[i]);
                if (index > -1) {
                  possibilidadesDeAreas.splice(index, 1);
                }
            }
            escolhidasDeAreas = data.Projetos[0].Areas;
            
            for (let i = 0; i<escolhidasDeAreas.length;i++) {
                document.getElementById('AreasEscolhidas').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center AreaEscolhida"><p>${escolhidasDeAreas[i]}</p><a class="d-flex" href="#" onclick="removeArea(this)">X</a></div>`;
            }
            
            for (let i = 0; i<data.Projetos[0].Users.length;i++) {
              for (let j = 0; j<possibilidadesDeMembros.length;j++) {
                let index = possibilidadesDeMembros[j].indexOf(data.Projetos[0].Users[i][2]);
                if (index > -1) {
                  possibilidadesDeMembros.splice(j, 1);
                }
              }
            }

            document.getElementById('MembrosEscolhidos').innerHTML = `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido selfuser" data-toggle="tooltip" title="UserCode: ${selfUserCode}"><div><p>Você</p></div></div>`

            escolhidasDeMembros = data.Projetos[0].Users;
            
            for (let i = 0; i<escolhidasDeMembros.length; i++) {
                let index = escolhidasDeMembros[i].indexOf(selfUserCode);
                if (index == -1) {
                  document.getElementById('MembrosEscolhidos').innerHTML += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido ${escolhidasDeMembros[i][1]}" data-toggle="tooltip" title="UserCode: ${escolhidasDeMembros[i][2]}"><div><p>${escolhidasDeMembros[i][0]}</p></div><a class="d-flex" href="#" onclick="removeMembro(this)">X</a></div>`;
                }
              }

            document.getElementById("PublishButton").innerText = (publicado) ? "Ocultar" : "Publicar";
        } else {
            document.getElementById("ProjectHoleDiv").innerHTML = "<strong style=\"color: rgb(0,0,0);font-size: 56px;\">Para editar esse projeto entre com uma conta que esteja vinculada nesse projeto!!!</strong>";
        }
    }).then(()=> {
      let options = "";
      for (let i = 0; i < possibilidadesDeAreas.length; i++) {
          options += `<option value="${possibilidadesDeAreas[i]}"></option>`;
      }
      options += `<option id="criarnovaarea" value="">Criar Nova Area</option>`;
      document.getElementById('Areas').innerHTML = options;
      
      options = "";
      for (let i = 0; i < possibilidadesDeMembros.length; i++) {
        options += `<option value="UserCode: ${possibilidadesDeMembros[i][2]}">${possibilidadesDeMembros[i][0]}</option>`;
      }
      document.getElementById('Membros').innerHTML = options;
    });
  } else {
    let options = "";
    for (let i = 0; i < possibilidadesDeAreas.length; i++) {
        options += `<option value="${possibilidadesDeAreas[i]}"></option>`;
    }
    options += `<option id="criarnovaarea" value="">Criar Nova Area</option>`;
    document.getElementById('Areas').innerHTML = options;

    for (let i = 0; i < possibilidadesDeMembros.length; i++) {
      let index = possibilidadesDeMembros[i].indexOf(selfUserCode);
      if (index > -1) {
        escolhidasDeMembros.push(possibilidadesDeMembros[i])
        possibilidadesDeMembros.splice(i, 1);
      }
    }

    document.getElementById('MembrosEscolhidos').innerHTML = `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido selfuser" data-toggle="tooltip" title="UserCode: ${selfUserCode}"><div><p>Você</p></div></div>`
      
    options = "";
    for (let i = 0; i < possibilidadesDeMembros.length; i++) {
      options += `<option value="UserCode: ${possibilidadesDeMembros[i][2]}">${possibilidadesDeMembros[i][0]}</option>`;
    }
    document.getElementById('Membros').innerHTML = options;
  }
});

function removeMembro(element) {
    let code = element.parentElement.getAttribute("title").replace("UserCode: ","");
    let item;
    for (let i = 0;i<escolhidasDeMembros.length;i++) {
      if (escolhidasDeMembros[i].indexOf(code) > -1) {
        item = escolhidasDeMembros[i];
        escolhidasDeMembros.splice(i,1);
      }
    }

    possibilidadesDeMembros.push(item);
    let options = "";
    for (let i = 0; i < possibilidadesDeMembros.length; i++) {
        options += `<option value="UserCode: ${possibilidadesDeMembros[i][2]}">${possibilidadesDeMembros[i][0]}</option>`;
    }
    document.getElementById('Membros').innerHTML = options;

    element.parentElement.parentElement.removeChild(element.parentElement);
}

function removeArea(element) {
    let nome = element.parentElement.getElementsByTagName('p')[0].innerText;
    possibilidadesDeAreas.push(nome);
    let options = "";
    for (let i = 0; i < possibilidadesDeAreas.length; i++) {
        options += `<option value="${possibilidadesDeAreas[i]}"></option>`;
    }
    options += `<option id="criarnovaarea" value="">Criar Nova Area</option>`;
    document.getElementById('Areas').innerHTML = options;

    let index = escolhidasDeAreas.indexOf(nome);

    if (index > -1) {
        escolhidasDeAreas.splice(index, 1);
    }

    element.parentElement.parentElement.removeChild(element.parentElement);
}

function saveCode() {
    var markupStr = $('#summernote').summernote('code');

    markupStr = markupStr.replaceAll('"',"'").replaceAll("/"," !@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@! ");
    
    var tituloStr = document.getElementById("Titulo").value;
    
    var areasList = escolhidasDeAreas;

    var usersList = [];

    for (let i = 0;i<escolhidasDeMembros.length;i++) {
      usersList.push(escolhidasDeMembros[i][2]);
    }

    if (ProjectCode != "new") {
        if (tituloStr.length > 0 && areasList.length > 0 && usersList.length > 0) {
            Data = {"createMethod":0,"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"Titulo":tituloStr,"Areas":areasList,"Users":usersList,"Desc":encodeURIComponent(markupStr),"Publicado":publicado,"ProjectCode":ProjectCode}

            fetch('/send_data_for_projects/'+JSON.stringify(Data), {
              method: 'POST',
            }).then((response) => {
              return response.json();
            }).then((data) => {
              // Work with JSON data here
                if (data.Aceito) {
                  alert("Projeto salvo!!!");
                } else {
                  alert("Algo Deu Errado");
                }
            });
          } else if (tituloStr.length == 0) {
              alert("Coloque um titulo");
          } else if (areasList.length == 0) {
              alert("Adicione uma área");
          } else if (markupStr.length == 0){
              alert("Escreva algo");
          }
    } else {
        if (tituloStr.length > 0 && areasList.length > 0 && usersList.length > 0) {
            Data = {"createMethod":1,"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"Titulo":tituloStr,"Areas":areasList,"Users":usersList,"Desc":encodeURIComponent(markupStr),"Publicado":publicado}
            
            fetch('/send_data_for_projects/'+JSON.stringify(Data), {
                method: 'POST',
              }).then((response) => {
                return response.json();
              }).then((data) => {
                // Work with JSON data here
                if (data.Aceito) {
                  ProjectCode = data.ProjectCode;
                  alert("Projeto salvo!!!");
                } else {
                  alert("Algo Deu Errado");
                }
              });
        } else if (tituloStr.length == 0) {
            alert("Coloque um titulo");
        } else if (areasList.length == 0) {
            alert("Adicione uma área");
        } else if (markupStr.length == 0){
            alert("Escreva algo");
        }
    }
}

function publishCode() {
    var markupStr = $('#summernote').summernote('code');

    markupStr = markupStr.replaceAll('"',"'").replaceAll("/"," !@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@! ");
    
    var tituloStr = document.getElementById("Titulo").value;
    
    var areasList = escolhidasDeAreas;

    var usersList = [];

    for (let i = 0;i<escolhidasDeMembros.length;i++) {
      usersList.push(escolhidasDeMembros[i][2]);
    }

    if (ProjectCode != "new") {
        if (tituloStr.length > 0 && areasList.length > 0 && markupStr.length > 0) {
            Data = {"createMethod":0,"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"Titulo":tituloStr,"Areas":areasList,"Users":usersList,"Desc":encodeURIComponent(markupStr),"Publicado":(publicado)?0:1,"ProjectCode":ProjectCode}

            fetch('/send_data_for_projects/'+JSON.stringify(Data), {
              method: 'POST',
            }).then((response) => {
              return response.json();
            }).then((data) => {
              // Work with JSON data here
              if (data.Aceito) {
                publicado = (publicado)?0:1;
                document.getElementById("PublishButton").innerText = (publicado) ? "Ocultar" : "Publicar";
                alert("Projeto publicado!!!");
              }else {
                alert("Algo Deu Errado");
              }
            });
        } else if (tituloStr.length == 0) {
            alert("Coloque um titulo");
        } else if (areasList.length == 0) {
            alert("Adicione uma área");
        } else if (markupStr.length == 0){
            alert("Escreva algo");
        }
    }else {
        if (tituloStr.length > 0 && areaStr.length > 0 && markupStr.length > 0) {
            Data = {"createMethod":1,"sessionishClientId":sessionStorage.getItem("sessionishClientId"),"Titulo":tituloStr,"Areas":areasList,"Desc":encodeURIComponent(markupStr),"Publicado":(publicado)?0:1}
            
            fetch('/send_data_for_projects/'+JSON.stringify(Data), {
                method: 'POST',
              }).then((response) => {
                return response.json();
              }).then((data) => {
                // Work with JSON data here
                if (data.Aceito) {
                  ProjectCode = data.ProjectCode;
                  publicado = (publicado)?0:1;
                  document.getElementById("PublishButton").innerText = (publicado) ? "Ocultar" : "Publicar";
                  alert("Projeto publicado!!!");
                } else {
                  alert("Algo Deu Errado");
                }
              });
        } else if (tituloStr.length == 0) {
            alert("Coloque um titulo");
        } else if (areasList.length == 0) {
            alert("Adicione uma área");
        } else if (markupStr.length == 0){
            alert("Escreva algo");
        }
  }
}

function ChangeImagePopUp() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

function ChangeImageData() {
    if (ProjectCode != "new") {
      const PORT = 5100;
      var file = document.getElementById('FileToGet').files[0];
      var fileReader = new FileReader();
      fileReader.readAsDataURL(file)
      fileReader.onload = () => {
          var arrayBuffer = fileReader.result;
  
          var socket = io.connect(`http://${IP}:${PORT}`);
  
          socket.on('Response', (data)=>{
            data.sessionishClientId = sessionStorage.getItem("sessionishClientId");
            data.updateProjectImage = 1;
            data.ProjectCode = ProjectCode;
              fetch('/update_image_account_data/'+JSON.stringify(data), {
                  method: 'POST',
              }).then((response) => {
                  return response.json();
              }).then((dataresponse) => {
                  // Work with JSON data here
                  if(dataresponse.Aceito){
                      alert("Foto Mudadas");
                      window.location.href = `/create_project/${ProjectCode}`;
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
    } else {
      alert("Salve o projeto primeiro");
    }
}

function CloseImagePopUp() {
    document.getElementById("myModal").style.display = "none";
}