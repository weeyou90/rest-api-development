$(document).ready(function(){
	var token = window.location.search.substring(1);

	 $("#user_info").click(function() {
      window.location.href = `profile.html?${token}`;
    });


	$("#user_expire").on('click', function(e){
		var formData = `{\"token\": "${token}"}`;

		e.preventDefault();
		e.returnValue = false;
		// send ajax
            $.ajax({
                url: 'http://localhost:8080/users/expire', // url where to submit the request
                type : "POST", // type of action POST || GET
                dataType : 'json', // data type
                data : formData,
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

});
