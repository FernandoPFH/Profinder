var AreasEscolhidasparaBuscar = [];

const CorSelecionado = "#1144dd"
const CorNaoSelecionado = "#061545"

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
              innerText += `<a class="d-flex flex-row align-items-center sidebar-item" onclick="ADACheckBoxClick(this)"><input type="checkbox" /><p style="color: rgb(0,0,0);margin-bottom: 0px;font-size: 18px;">${data.Areas[i]}></a>`
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

function SelecionarAreaAtual(SelfElement) {
    if (SelfElement.getElementsByTagName("p")[0].style.backgroundColor != CorSelecionado) {
        SelfElement.getElementsByTagName("p")[0].style.backgroundColor = CorSelecionado;
        if (SelfElement.nextSibling) {
            SelfElement.nextSibling.getElementsByTagName("p")[0].style.backgroundColor = CorNaoSelecionado;
            document.getElementById("list-aluno").getElementsByTagName("a")[0].disabled = true;
            document.getElementById("list-professor").getElementsByTagName("a")[0].disabled = true;
            document.getElementById("list-aluno").getElementsByTagName("a")[1].disabled = false;
            document.getElementById("list-professor").getElementsByTagName("a")[1].disabled = false;
        } else {
            SelfElement.previousSibling.getElementsByTagName("p")[0].style.backgroundColor = CorNaoSelecionado;
            document.getElementById("list-aluno").getElementsByTagName("a")[1].disabled = true;
            document.getElementById("list-professor").getElementsByTagName("a")[1].disabled = true;
            document.getElementById("list-aluno").getElementsByTagName("a")[0].disabled = false;
            document.getElementById("list-professor").getElementsByTagName("a")[0].disabled = false;
        }
    }
}

function ACheckBoxClick(SelfElement) {
  let AListElements = Array.prototype.slice.call(SelfElement.parentElement.getElementsByTagName("a"));

  let index = AListElements.indexOf(SelfElement);
  if (index > -1) {
    AListElements.splice(index, 1);
  }

  if (AListElements[0].getElementsByTagName('input')[0].checked) {
    index = Array.prototype.slice.call(SelfElement.parentElement.getElementsByTagName("a")).indexOf(AListElements[0]);
    if (index > -1) {
      SelfElement.parentElement.getElementsByTagName("a").item(index).getElementsByTagName("input")[0].checked = false;
    }
  }
    
  SelfElement.getElementsByTagName('input')[0].checked = !SelfElement.getElementsByTagName('input')[0].checked;
}

function ADACheckBoxClick(SelfElement) {
  if (!SelfElement.getElementsByTagName("input")[0].checked) {
    AreasEscolhidasparaBuscar.push(SelfElement.getElementsByTagName("p")[0].innerText);
  } else {
    let index = AreasEscolhidasparaBuscar.indexOf(SelfElement.getElementsByTagName("p")[0].innerText);
    if (index > -1) {
      AreasEscolhidasparaBuscar.splice(index, 1);
    }
  }
    
  SelfElement.getElementsByTagName("input")[0].checked = !SelfElement.getElementsByTagName("input")[0].checked;
}

function SearchForProjects () {
  let SpecificTypeToSearch = "";

  if (document.getElementById("A-List").getElementsByTagName('a').item(0).getElementsByTagName('input').item(0).checked) {
    SpecificTypeToSearch = "prof";
  } else if (document.getElementById("A-List").getElementsByTagName('a').item(1).getElementsByTagName('input').item(0).checked) {
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
        let ListOfProjectsElement = document.getElementById("ProjectsList");
        ListOfProjectsElement.innerHTML = "";
        for (let i = 0; i<data.Projetos.length; i++) {
          let ProjetoElement = `<a href="/project/${data.Projetos[i]}" class="SearchItem"><div class="d-flex flex-row align-items-start ProjectItem"><img class="ProjectItem special" src="${data.Projetos[i].Image}" /><div class="d-flex flex-column justify-content-center align-items-start" style="width: 100%;"><div class="d-xl-flex justify-content-xl-center align-items-xl-start ProjectItem-div" style="margin-left: -1px;"><strong>${data.Projetos[i].Titulo}<br /></strong></div><div class="d-flex flex-wrap ProjectItem-div" style="padding-top: 4px;"><p class="d-flex ProjectItem-div" style="width: 56px;height: 27px;margin-bottom: -6px;margin-top: -5px;">Areas:</p> </div><div class="d-flex flex-wrap ProjectItem-div" style="padding-top: 4px;"><p class="d-flex ProjectItem-div" style="width: 86px;height: 27px;margin-bottom: -6px;margin-top: -5px;">Membros:</p></div></div></div></a>`;
          for (let j = 0; j<data.Projetos[i].Areas.length; j++) {
            ProjetoElement += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center AreaEscolhida" style="padding-right: 5px;"><p><strong>${data.Projetos[i].Areas[j]}</strong></p></div>`;
          }
          ProjetoElement += `</div><div class="d-flex flex-wrap ProjectItem-div" style="padding-top: 4px;"><p class="d-flex ProjectItem-div" style="width: 86px;height: 27px;margin-bottom: -6px;margin-top: -5px;">Membros:</p>`;
          for (let j = 0; j<data.Projetos[i].Membros.length; j++) {
            ProjetoElement += `<div class="d-xl-flex justify-content-xl-start align-items-xl-center MembroEscolhido ${data.Projetos[i].Membros[j][1]}" data-toggle="tooltip" title="UserCode: ${data.Projetos[i].Membros[j][2]}"><div><p>${data.Projetos[i].Membros[j][0]}</p></div></div>`;
          }
          ProjetoElement += `</div></div></div></a>`;
          ListOfProjectsElement.innerHTML += ProjetoElement;
          CloseImagePopUp()
        }
    } else {
      let ListOfProjectsElement = document.getElementById("ProjectsList");
      ListOfProjectsElement.innerHTML = "";
      alert(data.Porque);
    }
});
}

function ChangeImagePopUp() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

function CloseImagePopUp() {
    document.getElementById("myModal").style.display = "none";
}