function getUserInformation(){

	
	document.getElementById("profile").innerHTML = "
		<div class="container">
			<div class="card card-outline-primary mb-3">
			  <div class="card-block">
			    <blockquote class="card-blockquote">
			<ul class="list-group list-group-flush">
			  <li class="list-group-item">Full Name    : {{users.fullname}}</li>
			  <li class="list-group-item">User Name    : {{users.name}}</li>
			  <li class="list-group-item">Age          : {{users.age}}</li>
			</ul>
			    </blockquote>
			  </div>
			</div>
		</div>


	";
}
