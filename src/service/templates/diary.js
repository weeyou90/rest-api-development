
var API_ENDPOINT = "http://localhost:8080"

function ajax_get(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            console.log('responseText:' + xmlhttp.responseText);
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch(err) {
                console.log(err.message + " in " + xmlhttp.responseText);
                return;
            }
            callback(data);
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

ajax_get(API_ENDPOINT + '/diary', function(data) {
	getPublicPosts(data);
});



function getPublicPosts(){
	
	var posts = data;
	posts.forEach(function(post) {
  		document.getElementById("publicPosts").innerHTML = "
			<div class="card" style="width: 100%;">
		  <div class="card-body">
		    <h5 class="card-title">{{post.title}}</h5>
		    <h6 class="card-subtitle mb-2 text-muted">By:{{post.author}}<br>On:{{post.publish_date}}</h6>
		    <p class="card-text">{{post.text}}</p>
		    <a href="#" class="card-link" data-toggle="modal" data-target={{"#" + post.id|string()}}>Read more</a>
		  </div>
		</div>
		
<div class="modal fade" id="{{post.id}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">{{post.title}}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
	<p>Published by:{{post.author}}, On:{{post.publish_date}}</p>
       <p>{{post.text}}</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<br>

		";
	});
		

}


function getPrivatePosts(username){

	var posts = [];
	posts.forEach(function(posts){
			document.getElementById("privatePosts").innerHTML = "
		
		<div class="card" style="width: 100%;">
		  <div class="card-body">
		    <h5 class="card-title">{{user_post.title}}</h5>
		    <h6 class="card-subtitle mb-2 text-muted">By:{{user_post.author}}<br> On:{{user_post.publish_date}}
			<form method="POST">
				<button type="button" class="btn btn-default btn-sm" style="float:right; position:relative; margin-left:5px;">
					<span class="fa fa-trash"></span>
				</button>
			</form>
			{%if user_post.public==0 %}
			<form method="POST">
				<button type="button" class="btn btn-default btn-sm" style="float:right; position:relative">
					<span class="fa fa-eye" ></span>
				</button>
			</form>
			{% else %}
			<form method="POST">
				<button type="button" class="btn btn-default btn-sm" style="float:right;position:relative">
					<span class="fa fa-eye-slash"></span>
				</button>
			</form>
			{%endif%}
			
			</h6>
		
		    <p class="card-text">{{user_post.text}}</p>
		    <a href="#" class="card-link flush-left" data-toggle="modal" data-target={{"#" + user_post.id|string()}}>Read more</a>				    	
		  </div>
		</div>
		
		<div class="modal fade" id="{{user_post.id}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
		  <div class="modal-dialog" role="document">
		    <div class="modal-content">
		      <div class="modal-header">
			<h5 class="modal-title" id="exampleModalLabel">{{user_post.title}}</h5>
			<button type="button" class="close" data-dismiss="modal" aria-label="Close">
			  <span aria-hidden="true">&times;</span>
			</button>
		      </div>
		      <div class="modal-body">
			<p>Published by:{{user_post.author}}, On:{{user_post.publish_date}}</p>
		       <p>{{user_post.text}}</p>
		      </div>
		      <div class="modal-footer">
			<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
		      </div>
		    </div>
		  </div>
		</div>
		<br>

	";

	});	

	

}
