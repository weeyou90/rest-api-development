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


                    if (data.status == true)
                    {
                        // redirect to the index page

                      alert("User successfully logged in!");
                      window.location= "./index.html";
                    }
                    else if (data.status == false)
                    {
                         // have some issues, need to fix
                      alert("Username or password is wrong!");
                      window.location= "./login.html";
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
        });
});