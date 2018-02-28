// add function for msg box
function closeAlertBox(){
    alertBox = document.getElementById("alertBox");
    alertClose = document.getElementById("alertClose");
    alertBox.parentNode.removeChild(alertBox);
    alertClose.parentNode.removeChild(alertClose);
};

window.alert = function(msg){
    var id = "alertBox", alertBox, closeId = "alertClose", alertClose;
    alertBox = document.createElement("div");
    document.body.appendChild(alertBox);
    alertBox.id = id;
    alertBox.innerHTML = msg;
    alertClose = document.createElement("div");
    alertClose.id = id;
    document.body.appendChild(alertClose);
    alertClose.onclick = closeAlertBox;
};

$(document).ready(function(){
         // click on button submit
        $("#submit").on('click', function(e){

          e.preventDefault();
          e.returnValue = false;

          if(document.getElementById("password").value != document.getElementById("password_confirm").value)
          {
            alert("Password doesn't match");
            return;
          }
          else if (document.getElementById("username").value == "" || document.getElementById("fullname").value == "" || document.getElementById("age").value == "" || document.getElementById("password").value == "")
          {
            alert("Please fill up all the fields");
            return;
          }

          var usernameVar = document.getElementById("username").value
          var passwordVar = document.getElementById("password").value
          var fullnameVar = document.getElementById("fullname").value
          var ageVar = document.getElementById("age").value
          var formData = `{\"username\": "${usernameVar}",\"password\": "${passwordVar}",\"fullname\": "${fullnameVar}",\"age\": ${ageVar}}`;

        //  var formData = JSON.stringify($("#formAuthenticate").serializeArray());


            // send ajax
            $.ajax({
                url: 'http://localhost:8080/users/register', // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : formData,
                contentType: "application/json",
                success : function(data) {

                    console.log(data.status);
                    if (data.status == true)
                    {
                        // redirect to the login page

                      alert("User successfully registered!");
                      window.location= "./login.html";
                    }
                    else
                    {
                      
                       alert("User name already exists!);
                       console.log(data.error)
		      //window.location= "./login.html";
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
        });
});


