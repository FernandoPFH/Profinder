function sha512(str) {
  str += "i5kmHo2t";
  return crypto.subtle.digest("SHA-512", new TextEncoder("utf-8").encode(str)).then(buf => {
    return Array.prototype.map.call(new Uint8Array(buf), x=>(('00'+x.toString(16)).slice(-2))).join('');
  });
}

async function TryLogin() {
  User = {"Email":document.getElementById("Email").value,"Password":await sha512(document.getElementById("Password").value),"sessionishClientId":sessionStorage.getItem("sessionishClientId")};

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