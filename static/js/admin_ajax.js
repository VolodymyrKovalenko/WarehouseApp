$(function() {
    $('button.acceptButton').click(function() {
        // var user = $('#txtBrand').val();
        // var pass = $('#txtModel').val();
        $.ajax({
            url: '/handler2',
            data: $('#app_id').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});