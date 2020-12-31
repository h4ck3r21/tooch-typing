$(function() {
    var socket = io.connect(
        'http://' + document.domain + ':' + location.port);
    socket.on( 'connect', function() {
      socket.emit( 'my event', {message: 'User Connected'})
      var form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input.message' ).val()
        socket.emit( 'my event', {
          message : user_input
        })
        $( 'input.message' ).val( '' ).focus()
      })
    });
    socket.on( 'my response', function( msg ) {
        console.log( msg )
        console.log( msg.message )
        if(msg.data !== 'undefined' ) {
            $( 'h3' ).remove()
            console.log("Appending " + msg.data )
            $( 'div.message_holder' ).append( '<div>'+msg.message +'</div>' )
        }
    });
});