$(function(){
    var socket = io.connect('/', {transports: ['websocket']});
    let userID = $( '#userid').html()
    socket.on('paragraph', function(paragraph){
            $( '#paragraph' ).html(paragraph)
        })
    socket.on('error', function(id){
            if (id == userID) {
                $('body').addClass('error');
            }
    })

    socket.on('fix', function(id){
        if (id == userID) {
            $('body').removeClass('error');
        }
    });
});