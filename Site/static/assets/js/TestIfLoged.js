async function IsLoged(){
  return await fetch('/try_login_by_session_data/'+sessionStorage.getItem("sessionishClientId"), {
    method: 'GET',
  }).then((response) => {
    return response.json()
  }).then((data) => {
    // Work with JSON data here
    return data.Aceito
  });
}

async function Logout() {
    sessionStorage.removeItem('sessionishClientId');
    window.location.reload(false);
}

async function ChangeDocumentIfLoged(){
  if (await IsLoged()){

    User = {"sessionishClientId":sessionStorage.getItem("sessionishClientId")}
    fetch('/send_data_for_account/'+JSON.stringify(User), {
      method: 'GET',
    }).then((response) => {
      return response.json()
    }).then((data) => {
      // Work with JSON data here
      if(data.Aceito){
        let imgUrl = "/static/assets/img/Picture1-512.webp";
        if (data.Image != null) {
          imgUrl = data.Image
        }
        document.getElementsByTagName("nav")[0].getElementsByTagName("ul")[0].innerHTML = `<li class="nav-item" style="height: 67px;"><div class="dropdown show" style="width: 67px;"><a id="dropdownMenuLink" class="nav-link" href style="width: 67px;height: 67px;" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><div class="d-xl-flex flex-row align-items-xl-center" style="width: 100%;height: 100%;"><img class="PerfilPic" style="width: 100%;height: 100%;" src="${imgUrl}" /></div></a><div class="dropdown-menu" aria-labelledby="dropdownMenuLink" style="left: -85px;"><a class="dropdown-item" href="/account_data/${data.UserCode}">Minha conta</a><a class="dropdown-item" onclick="Logout()">Sair</a></div></div></li>`;
      }else{
        alert(data.Porque)
      }
    });

  }
}

$(document).ready(ChangeDocumentIfLoged())