function renderNav(){
	
   	// send ajax
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
				
		    }
                    else if (result.status == false)
                    {
                      console.log("user is not logged in");
                    }

                },
                error: function(xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })



}


