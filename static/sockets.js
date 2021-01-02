$(function(){
    var socket = io.connect('/', {transports: ['websocket']});
    let userID = $( '#userID').html()
    document.addEventListener('keypress', logKey);
    function logKey(e) {
      let user_input = $( 'input.message' ).val()
      console.log('sending keypress')
      socket.emit('keypress', {input: user_input, userID:userID})
    }

    socket.on( 'connect', function() {
      let username = $( '#username').html()
      let userID = $( '#userID').html()
      socket.emit( 'connecting', {username: username, userID: userID})
      console.log('user connected')
      var form = $( 'form' ).on( 'submit', function( e ) {
          e.preventDefault()
        })
    })

    socket.on('log', function(msg) {
      $( '#log' ).append( '<div>'+ msg + '</div>' )
    })

    socket.on( 'user disconnect', function() {
      console.log('sending user disconnect message')
      socket.emit('online', userID)
    });

    socket.on('error', function(id){
        console.log('error')
        if (id == userID) {
            $('#your-para').addClass('error');
        }
    })

    socket.on('fix', function(id){
        console.log('correct keypress')
        if (id == userID) {
            $('#your-para').removeClass('error');
        }
    })
});
