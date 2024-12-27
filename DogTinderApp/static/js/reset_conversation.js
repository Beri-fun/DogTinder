
function reset_conversation(){
    let get_url = $(this).attr('data-url');
    $.ajax({
        url: get_url,
        type: 'GET',
        success: function() {
            console.log('Success');
            location.reload(); 
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

$(document).ready(function() {

    $('#reset_conversation').click(function() {
        reset_conversation()
    });

});