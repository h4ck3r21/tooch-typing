$(function() {
    var socket = io.connect('/');
    socket.on( 'connect', function() {
      let username = $( '#username').html()
      socket.emit( 'my event', {message: '*Connected*', username: username})
      console.log('user connected')
      var form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input.message' ).val()

        socket.emit( 'my event', {
          username : username,
          message : user_input
        })
        $( 'input.message' ).val( '' ).focus()
      })
      socket.on('disconnect', function() {
        console.log('user disconnected')
      })
    });
    socket.on( 'user disconnect', function() {
      console.log('sending user disconnect message')
      $( 'div.message_holder' ).append( '<div>'+ 'User Disconnected'+ '</div>' )
    })
    socket.on( 'my response', function( msg ) {
        console.log( msg )
        console.log( msg.message )
        if(msg.message) {
            $( '#error-message' ).hide()
            console.log("Appending " + msg.data )
            $( 'div.message_holder' ).append( '<div>'+ msg.username + ':&nbsp;' + msg.message +'</div>' )
        } else {
            $( '#error-message' ).show()
            $( '#error-message' ).html("No message given!!")
        }
    });
});