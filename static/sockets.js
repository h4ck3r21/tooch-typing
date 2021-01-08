$(function(){
    var socket = io.connect('/', {transports: ['websocket']});
    let userID = $( '#userID').html()
    var Ids = []
    $( "#message-box" ).keydown(function() {
      setTimeout(() => {
           let user_input = $( 'input.message' ).val()
           console.log('sending keypress')
           socket.emit('keypress', {input: user_input, userID:userID})
      }, 100);
    });

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
      Ids = []
      $( "#enemy-paragraphs").empty()
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

    socket.on('connection', function(enemy_id){
        console.log('connecting')
        if (userID == enemy_id.id) {
            var i;
            for (i = 0; i < enemy_id.len; i++) {
              console.log(enemy_id.i)
              Ids.push(enemy_id[i])
              $( "#enemy-paragraphs").append('<iframe src="/paragraph/'+
               enemy_id[i] +
               '" title="your paragraph" class="enemy-para"></iframe>');
            };
        }
    })

    socket.on('new user', function(id){
        console.log('new user: ' + id)
        console.log('checking if ' + id + 'is not equal to ' + userID)
        console.log(id != userID)
        if (id != userID && !(id in Ids)) {
            Ids.push(id)
            console.log('adding enemy paragraph')
            $( "#enemy-paragraphs").append('<iframe src="/paragraph/'+ id +'" title="your paragraph" class="enemy-para"></iframe>');
        }
    })
});
