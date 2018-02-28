function renderNav(){
	
   	$.ajax({
                url: 'http://localhost:8080/users', // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : '{token:"' +getCookie("token") + '"}',
                contentType: "application/json",
                success : function(result) {

                    console.log(result.status);


                    if (result.status == true)
                    {
                        console.log("user is logged in");
			document.getElementById("userNavLeft").innerHTML = '';
				
		    }
                    else if (result.status == false)
                    {
                      console.log("user is not logged in");
			document.getElementById("userNavRight").innerHTML = '';
			
		

	
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })



}


/*

 if (result.status == true)
                    {
                        console.log("user is logged in");
			document.getElementById("userNavLeft").innerHTML = "
				      <li class="nav-item active">
					<a class="nav-link" href="./newEntry.html">New Entry</a>
				      </li>
				";


				document.getElementById("userNavRight).innerHTML = "

				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
				  		Hi 
				</a>
				<div class="dropdown-menu" aria-labelledby="navbarDropdown">
				  <a class="dropdown-item" href="./profile.html">Profile</a>     
				  <div class="dropdown-divider"></div>
				  <a class="dropdown-item" href="./logout">Logout</a>
				</div>
			      </li>
				
		    }
                    else if (result.status == false)
                    {
                      console.log("user is not logged in");
			document.getElementById("userNavRight).innerHTML = "
			<li class="nav-item active">
 				<a class="nav-link" href="{{url_for('users_authenticate')}}">Login</a>
			</li>
			<li class="nav-item active">
 				<a class="nav-link" href="{{url_for('users_register')}}">Register</a>
			</li>
		";
		

	
                    }


*/



