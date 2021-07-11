$(document).ready(() => {
  fetch('/send_data_for_numberofusers/', {
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((data) => {
      // Work with JSON data here
      if (data.Aceito) {
          document.getElementById("numerodeusuarios").innerText = data.NumberOfUsers.toString() + " Usuários";
      }
  });
    
  $('#EmailInput').on('input',()=>{checarSeEmailEValido($('#EmailInput').val())});
});

function checarSeEmailEValido(email) {
    let classname = $('#EmailInput').attr('class');
    if (!(classname.includes("is-invalid") || classname.includes("is-valid"))) {
        $("#EmailInput").addClass("is-invalid");
        $("#HelpTextEmailInput").removeClass("is-valid");
    } else {
        let EMAIL_REGEX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (EMAIL_REGEX.test(String(email).toLowerCase())) {
            if (classname.includes("is-invalid")) {
                $("#EmailInput").removeClass("is-invalid");
                $("#EmailInput").addClass("is-valid");
                $("#HelpTextEmailInput").addClass("is-valid");
                document.getElementById("ContactUsButton").disabled = false;
            }
        } else {
            if (classname.includes("is-valid")) {
                $("#EmailInput").removeClass("is-valid");
                $("#EmailInput").addClass("is-invalid");
                $("#HelpTextEmailInput").removeClass("is-valid");
                document.getElementById("ContactUsButton").disabled = true;
            }
        }
    }
}