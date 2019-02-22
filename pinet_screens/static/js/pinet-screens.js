function clientUpdateContent(client_id, content_id) {
    $.ajax({
        type: "POST",
        url: "/clients/update_content_ajax",
        data: {
            client_id: client_id,
            content_id: content_id
        },
        success: function (result) {
            //alert('Updated');
            //window.location.reload();
        },
        error: function (result) {
            alert('Error updating content');
            window.location.reload();
        }
    });
}


function clientUpdateLoginStatus(client_id, status) {
    $.ajax({
        type: "POST",
        url: "/clients/update_autologin_ajax",
        data: {
            client_id: client_id,
            status: status
        },
        success: function (result) {
            //alert('Updated');
            //window.location.reload();
        },
        error: function (result) {
            alert('Error updating login status');
            window.location.reload();
        }
    });
}


$(function() {
    $('.autologin-toggle').change(function() {
        //console.log($(this).prop('checked'))
        clientUpdateLoginStatus(this.attributes["data-client-id"].value, $(this).prop('checked'))
    })
  });


$(function() {

  $(".selectpicker").on("changed.bs.select", function(e, clickedIndex, newValue, oldValue) {

      clientUpdateContent(this.attributes["data-client"].value, this.value);
      console.log(this.value, clickedIndex, newValue, oldValue)
  });

});