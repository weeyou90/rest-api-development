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
                    else if (data.status == false)
                    {
                         // have some issues, need to fix
                      alert("Error");
                      window.location= "./register.html";
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
        });
});


