var AreasEscolhidasparaBuscar = [];

$(document).ready(() => {
  fetch('/send_data_for_projectssideinfos/', {
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((data) => {
      // Work with JSON data here
      if (data.Aceito) {
          let i;
          let innerText = "";
          for (i = 0; i < data.Areas.length; i++) {
              innerText += `<li class="list-group-item d-xl-flex justify-content-xl-start align-items-xl-center sidebar-item"><input type="checkbox" style="margin-left: -11px;" onclick="ADACheckBoxClick(this)"/><label class="d-xl-flex sidebar-item-text" style="margin-top: 7px;margin-left: 4px;">${data.Areas[i]}</label></li>`
          }
          document.getElementById("ADA-List").innerHTML = innerText;
      }
  });
  
  let SearchPreDone = sessionStorage.getItem("searchbarvalue");

  if (SearchPreDone) {
    document.getElementById("SearchBar").value = SearchPreDone;

    sessionStorage.removeItem("searchbarvalue");

    SearchForProjects();
  }
});

function ACheckBoxClick(SelfElement) {
  let AListElements = Array.prototype.slice.call(SelfElement.parentElement.parentElement.getElementsByTagName("li"));

  let index = AListElements.indexOf(SelfElement.parentElement);
  if (index > -1) {
    AListElements.splice(index, 1);
  }

  if (AListElements[0].getElementsByTagName('input')[0].checked) {
    index = Array.prototype.slice.call(SelfElement.parentElement.parentElement.getElementsByTagName("li")).indexOf(AListElements[0]);
    if (index > -1) {
      SelfElement.parentElement.parentElement.getElementsByTagName("li").item(index).getElementsByTagName("input")[0].checked = false;
    }
  }
}

function ADACheckBoxClick(SelfElement) {
  if (SelfElement.checked) {
    AreasEscolhidasparaBuscar.push(SelfElement.parentElement.getElementsByTagName("label")[0].innerText);
  } else {
    let index = AreasEscolhidasparaBuscar.indexOf(SelfElement.parentElement.getElementsByTagName("label")[0].innerText);
    if (index > -1) {
      AreasEscolhidasparaBuscar.splice(index, 1);
    }
  }
}

function SearchForProjects () {
  let SpecificTypeToSearch = "";

  if (document.getElementById("A-List").getElementsByTagName('li').item(0).getElementsByTagName('input').checked) {
    SpecificTypeToSearch = "prof";
  } else if (document.getElementById("A-List").getElementsByTagName('li').item(1).getElementsByTagName('input').checked) {
    SpecificTypeToSearch = "aluno";
  }

  Data = {"Titulo":document.getElementById("SearchBar").value,"Tipo":SpecificTypeToSearch,"Areas":AreasEscolhidasparaBuscar}

  fetch('/search_for_projects/'+JSON.stringify(Data), {
    method: 'GET',
  }).then((response) => {
    return response.json();
  }).then((data) => {
    // Work with JSON data here
    if (data.Aceito) {
        console.log(data);
        let ListOfProjectsElement = document.getElementById("ProjectsList");
        ListOfProjectsElement.innerHTML = "";
        for (let i = 0; i<data.Projetos.length; i++) {
          let ProjetoElement = `<a href="/project/${data.Projetos[i]}" style="text-decoration: none;"><div class="d-xl-flex flex-row justify-content-xl-start align-items-xl-start ProjectItem" style="background: #f7ccb4;border-width: 1px;border-style: solid;"><img class="ProjectItem" style="width: 180px;height: 180px;background: #ffffff;" src="${data.Projetos[i].Image}" /><div class="d-xl-flex flex-column justify-content-xl-center align-items-xl-start"> <div class="d-xl-flex justify-content-xl-center align-items-xl-start ProjectItem-div" style="margin-left: -1px;"><strong>${data.Projetos[i].Titulo}<br /></strong></div><div class="d-flex flex-wrap ProjectItem-div" style="padding-top: 4px;"><p class="d-flex ProjectItem-div" style="width: 56px;height: 27px;margin-bottom: -6px;margin-top: -5px;">Areas:</p>`;
          for (let j = 0; j<data.Projetos[i].Areas.length; j++) {
            ProjetoElement += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center AreaEscolhida" style="padding-right: 5px;"><p><strong>${data.Projetos[i].Areas[j]}</strong></p></div>`;
          }
          ProjetoElement += `</div><div class="d-flex flex-wrap ProjectItem-div" style="padding-top: 4px;"><p class="d-flex ProjectItem-div" style="width: 86px;height: 27px;margin-bottom: -6px;margin-top: -5px;">Membros:</p>`;
          for (let j = 0; j<data.Projetos[i].Membros.length; j++) {
            ProjetoElement += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido ${data.Projetos[i].Membros[j][1]}" data-toggle="tooltip" title="UserCode: ${data.Projetos[i].Membros[j][2]}"><div><p>${data.Projetos[i].Membros[j][0]}</p></div></div>`;
          }
          ProjetoElement += `</div></div></div></a>`;
          ListOfProjectsElement.innerHTML += ProjetoElement;
        }
    } else {
      let ListOfProjectsElement = document.getElementById("ProjectsList");
      ListOfProjectsElement.innerHTML = "";
      alert("Nenhum projeto encontrado!!!");
    }
});
}