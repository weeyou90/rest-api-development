API_Endpoint = "http://localhost:8080"

function retrieveAllPublicEntries(){
    return $.ajax({
        url: API_Endpoint +"/diary",
        type: 'GET',
        dataType: 'json', 
        success: function(res) {
            console.log(res);
            alert(res);
        }
 });
}

function retrieveEntriesOfAuthenticatedUser(payload){
	$.ajax({
        url: API_Endpoint+"/diary",
        type: 'POST',
        dataType: 'json',
        data: payload
        success: function(res) {
            console.log(res);
            alert(res);
        }
 });
}

function createNewDiaryEntry(payload){
	$.ajax({
        url: API_Endpoint + "/create",
        type: 'POST',
        dataType: 'json', 
        data: payload
        success: function(res) {
            console.log(res);
            alert(res);
        }
 });
}

function deleteExistingDiaryEntry(){
	$.ajax({
        url: API_Endpoint+ "/diary/delete",
        type: 'POST',
        dataType: 'json', 
        data: payload
        success: function(res) {
            console.log(res);
            alert(res);
        }
 });
}


function adjustDiaryEntryPermissions(payload){
	$.ajax({
        url: API_Endpoint+"/diary/permission",
        type: 'POST',
        dataType: 'json', 
        data: payload
        success: function(res) {
            console.log(res);
            alert(res);
        }
 });
}
