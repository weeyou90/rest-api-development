


function userIsLoggedIn(){
	console.log('checking if user is logged in');
	console.log(getCookie("token"));

	if(!!getCookie("token")){
		//for the first left nav
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


		";
	}else{
		document.getElementById("userNavRight).innerHTML = "
			<li class="nav-item active">
 				<a class="nav-link" href="{{url_for('users_authenticate')}}">Login</a>
			</li>
			<li class="nav-item active">
 				<a class="nav-link" href="{{url_for('users_register')}}">Register</a>
			</li>
		";
		

	}

}



