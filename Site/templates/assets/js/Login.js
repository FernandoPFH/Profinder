function TryLogin() {
  User = {"Email":document.getElementById("Email").value,"Password":document.getElementById("Password").value,"sessionishClientId":sessionStorage.getItem("sessionishClientId")};

  fetch('/send_data_for_login/'+JSON.stringify(User), {
    method: 'GET',
  }).then((response) => {
    return response.json();
  }).then((data) => {
    // Work with JSON data here
    if(data.Aceito){
      sessionStorage.setItem("sessionishClientId",data.sessionishClientId)
      window.location.href = "/account_data/"+data.Code;
    }else{
      alert(data.Porque);
    }
  });
}