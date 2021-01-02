$(function() {
    var socket = io.connect('/', {transports: ['websocket']});
    socket.on( 'connect', function() {
      let username = $( '#username').html()
      socket.emit( 'my event', {message: '*Connected*', username: username})
      socket.emit( 'connecting', username)
      console.log('user connected')
      var form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input.message' ).val()
        $("input.message").value += "\n";

    socket.on( 'reload online users', function( users ) {
      $( '#online' ).empty()
      users.forEach(function (user, index){
        console.log(user + 'connected')
        $( '#online' ).append( '<div>'+ user + ':&nbsp; online</div>' )
      })
    })

    socket.on( 'user disconnect', function() {
      let username = $( '#username').html()
      console.log('sending user disconnect message')
      $( '#message_holder' ).append( '<div>'+ 'User Disconnected'+ '</div>' )
      socket.emit('online', username)
    });

    socket.on( 'my response', function( msg ) {
        console.log( msg )
        console.log( msg.message )
        if(msg.message) {
            $( '#error-message' ).hide()
            console.log("Appending " + msg.data )
            $( '#message_holder' ).append( '<div>'+ msg.username + ':&nbsp;' + msg.message +'</div>' )
        } else {
            $( '#error-message' ).show()
            $( '#error-message' ).html("No message given!!")
        }
    });
});
