$(function() {
    $('select').click(function() {
        // var user = $('#txtBrand').val();
        // var pass = $('#txtModel').val();
        $.ajax({
            url: '/handler1',
            data: $('#receiptForm').serialize(),
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