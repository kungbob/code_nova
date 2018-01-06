$(function () {


    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");

    var silent = false;

    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/room/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);


    editor.on("change", function( e ) {

      console.log(JSON.stringify(e))
                    // TODO, we could make things more efficient and not likely to conflict by keeping track of change IDs
                    // if( last_applied_change!=e && !just_cleared_buffer ) {
                    //     collaborator.change( JSON.stringify(e) ) ;
                    //
                    //
                    // }
                    // just_cleared_buffer = false ;
                    if (silent)
                    {
                      console.log("silent")

                    }
                    else {

                      socket.send(JSON.stringify({
                          "command": "editor_send",  // determines which handler will be used (see chat/routing.py)
                          "room": 1,
                          "change" : JSON.stringify(e)
                      }));

                    }

                }, false );



    // Helpful debugging
    socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };

    socket.onmessage = function (message) {
        // Decode the JSON
        console.log("Got websocket message " + message.data);
        var data = JSON.parse(message.data);
        // Handle errors
        if (data.error) {
            alert(data.error);
            return;
        }

        if(data.message)
        {
          console.log("i hv recieve something");
          var delta = JSON.parse(data.message) ;
          console.log("delta",delta);

          if (data.user_id == "{{request.user.id}}")
          {
            console.log("my own change");
          }

          silent = true;
          editor.getSession().getDocument().applyDeltas([delta]) ;
          silent = false;



        }


        // Handle joining

    };

    $('#join_room_button').on('click', function() {
         /* your code here */

         var test_message = "something test message";

         socket.send(JSON.stringify({
             "command": "join_room",  // determines which handler will be used (see chat/routing.py)
             "room": 1
         }));
    });

    $('#leave_room_button').on('click', function() {
         /* your code here */

         var test_message = "something test message";

         socket.send(JSON.stringify({
             "command": "leave_room",  // determines which handler will be used (see chat/routing.py)
             "room": 1
         }));
    });

    // Says if we joined a room or not by if there's a div for it
    function inRoom(roomId) {
        return $("#room-" + roomId).length > 0;
    };

    // Room join/leave
    $("li.room-link").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            // Leave room
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",  // determines which handler will be used (see chat/routing.py)
                "room": roomId
            }));
        } else {
            // Join room
            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    });
});
