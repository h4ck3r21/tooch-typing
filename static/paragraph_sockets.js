$(function(){
    var socket = io.connect('/', {transports: ['websocket']});
    let userID = $( '#userid').html()
    socket.on('paragraph', function(paragraph){
            $( '#paragraph' ).html(paragraph.para)
            $('#para-correct').html(paragraph.cor)
            $( '#errors').html(paragraph.errors)
        })
    socket.on('error', function(id){
            if (id == userID) {
                $('body').addClass('error');
            }
    })

    socket.on('fix', function(userid){
        if (userid == userID) {
            $('body').removeClass('error');
        }
    });
});