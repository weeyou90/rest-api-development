function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie = c_name + "=" + c_value;
}

function getCookie(c_name) {
    var i, x, y, ARRcookies = document.cookie.split(";");
    for (i = 0; i < ARRcookies.length; i++) {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == c_name) {
            return unescape(y);
        }
    }
};

function userIsLoggedIn(){
	
	// send ajax
            $.ajax({
                url: 'http://localhost:8080/users', // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : JSON.stringify({token:getCookie("token")}),
                contentType: "application/json",
                success : function(result) {
		
                    if (result.status == true)

                    {
                        console.log("user is logged in");
                        // $("#user").html(result.result.name);
document.getElementById("userNavRight").innerHTML = '<a id="user_info" href="./profile.html">Profile</a> | <a id="user_expire" href="./logout.html">Logout</a>';
document.getElementById("userNavLeft").innerHTML = '<a href="./privateDiary.html">Read My Diary Entries</a> | <a href="./createPost.html">Create Entries</a>';
				
		    }
                    else if (result.status == false)
                    {
                      console.log("user is not logged in");
			document.getElementById("userNavRight").innerHTML = '<a href="./login.html">Login</a> | <a href="./signup.html">Register</a>';
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })


}



$(document).ready(function(){
	
	$("#user_expire").on('click', function(e){
		token = getCookie("token")
		tokendata = JSON.stringify({token:token})
		console.log("logout"+token)
		e.preventDefault();
		e.returnValue = false;
		// send ajax
            $.ajax({
                url: 'http://localhost:8080/users/expire', // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : tokendata,
                contentType: "application/json",
                success : function(data) {

                    console.log(data);

                    if (data.status == true)
                    {
                        // redirect to the index page
                      alert("Successfully logged out");
                      window.location.href= "index.html";
                    }
                    else if (data.status == false)
                    {
                         // have some issues, need to fix
                      alert("Already logged out");
                      window.location.href = "index.html";
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
	});


         // click on login button
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
                success : function(result) {

                    console.log(result.status);


                    if (result.status == true)
                    {
			
                        setCookie("token", result.result.token)                      
                        alert("cookie"+getCookie("token"))
                        alert("Login Successful!")
                        $(location).attr('href', 'http://localhost/index.html')
        
        }
                    else if (result.status == false)
                    {
                      alert("Login Failed!");
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
        });
});

function getuser() {
	token = getCookie("token")
	tokendata = JSON.stringify({token:token})
	$.ajax({
		url: 'http://localhost:8080/users', // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : tokendata,
		contentType: "application/json",
		success : function(data) {
		    if (data.status == true)
		    {		
		    	return data.result
		    }
		    else
		    {
		  
		       return false
		    }

		},
		error: function(xhr, resp, text) {
		    console.log(xhr, resp, text);
		}
	});

}

