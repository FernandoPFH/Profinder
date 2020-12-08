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
        document.getElementsByClassName("nav navbar-nav ml-auto")[0].innerHTML = `<li class="nav-item" style="height: 67px;"><a class="nav-link" href="/account_data/${data.UserCode}" style="height: 67px;width: 67px;"><div class="d-xl-flex flex-row align-items-xl-center" style="height: 100%;width: 100%;"><img class="PerfilPic" src="${imgUrl}" style="height: 100%;width: 100%;" /></div></a></li>`;
      }else{
        alert(data.Porque)
      }
    });

  }
}

$(document).ready(ChangeDocumentIfLoged())