$(function() {
    console.log('Poke Script loaded');
    
    $('.select-pokemon').submit(function(e) {
        e.preventDefault();
        
        var form = $(this);
        console.log($(location).attr('href') + form.attr('action'))
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize()
        }).done(function(result) {
            console.log(result);
        }).error(function(err) {
            console.log("ERROR:",err);
        })
    });
})