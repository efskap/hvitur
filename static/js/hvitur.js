
 $('#upload-btn').click(function() {
           event.preventDefault();
document.getElementById("chooser").click();
 });



 function sub(obj){
      event.preventDefault();
    var file = obj.value;
     if(file == "") return;
    var fileName = file.split("\\");
    $("#upload-btn").html( fileName[fileName.length-1]);
  var ajax_load = "<img class='spinner center' src='static/bx_loader.gif' alt='loading...' />";

       $('#result').html(ajax_load); // loading spinny

        var form_data = new FormData($('#uploadform')[0]);
        $.ajax({
            type: 'POST',
            url: '/do',
            data: form_data,
            contentType: false,  // dont try to parse this, jquery
            processData: false,  // dunno what this does
            dataType: 'text',    // yeah we want a string
                success: function (data) {
        $('#result').html("<img class='output' src='" + data + "'/>");
    }
        }).done(function (data, textStatus, jqXHR) {
            console.log(data);
            console.log(textStatus);
            console.log(jqXHR);
            console.log('Success!');
        }).fail(function (data) {
            console.log('error!');
        });

  }

