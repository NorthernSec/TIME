function parseStatus(data){
  _ok = false;
  if (data['status'] != undefined){
    switch(data['status']){
      case "success":    _ok=true;break;
      default:
        setStatus("A problem occurred with the server!", "danger");
    }
  }
  return _ok;
}

function setStatus(text, status){
  $("#status-box").empty();
  $("#status-box").removeClass();
  $("#status-box").addClass("alert alert-"+status);
  $("#status-box").append(text);
}

function briefShow(text, status, icon){
  $("#status").removeClass();
  $("#status").addClass("alert alert-"+status);
  $("#status_icon").removeClass();
  $("#status_icon").addClass("glyphicon glyphicon-"+icon+"-sign");
  $("#status_message").empty();
  $("#status_message").append(text);
  $("#status").removeTemporaryClass("hidden", 3000);
}
