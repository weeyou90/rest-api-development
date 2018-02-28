// add function for msg box
// function closeAlertBox(){
//     alertBox = document.getElementById("alertBox");
//     alertClose = document.getElementById("alertClose");
//     alertBox.parentNode.removeChild(alertBox);
//     alertClose.parentNode.removeChild(alertClose);
// };

// window.alert = function(msg){
//     var id = "alertBox", alertBox, closeId = "alertClose", alertClose;
//     alertBox = document.createElement("div");
//     document.body.appendChild(alertBox);
//     alertBox.id = id;
//     alertBox.innerHTML = msg;
//     alertClose = document.createElement("div");
//     alertClose.id = id;
//     document.body.appendChild(alertClose);
//     alertClose.onclick = closeAlertBox;
// };

$(document).ready(function(){
         // click on button submit
        $("#login").on('click', function(e){

          e.preventDefault();
          e.returnValue = false;

          if (document.getElementById("username").value == "" || document.getElementById("password").value == "")
          {
            alert("Please fill up all the fields");
            return;
          }

          var usernameVar = document.getElementById("username").value
          var passwordVar = document.getElementById("password").value
          var formData = `{\"username\": "${usernameVar}",\"password\": "${passwordVar}"}`;

        //  var formData = JSON.stringify($("#formAuthenticate").serializeArray());


            // send ajax
            $.ajax({
                url: 'http://localhost:8080/users/authenticate', // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : formData,
                contentType: "application/json",
                success : function(data) {

                    console.log(data.status);
                    token = data.result;

                    if (data.status == true)
                    {
                        // redirect to the index page

                      alert("User successfully logged in!");
                      window.location.href= `index.html?${token}`;
                    }
                    else if (data.status == false)
                    {
                         // have some issues, need to fix
                      alert("Username or password is wrong!");
                      window.location= "login.html";
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
        });
});

