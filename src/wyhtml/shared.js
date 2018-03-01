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
}

function login(logindata) {
	$.ajax({
		url: 'http://localhost:8080/users/authenticate', // url where to submit the request
		type : "POST", // type of action POST || GET
		dataType : 'json', // data type
		data : logindata,
		contentType: "application/json",
		success : function(data) {

		    console.log(data.status);
		    if (data.status == true)
		    {
			setCookie("token", data.result.token)
			console.log("cookie"+getCookie("token"))			
		    	window.location= "/";
		    }
		    else
		    {
		       alert("Wrong user/pw combination");
		    }

		},
		error: function(xhr, resp, text) {
		    console.log(xhr, resp, text);
		}
	});
}

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
