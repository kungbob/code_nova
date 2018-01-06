from channels import route
from .consumers import ws_connect, ws_receive, ws_disconnect,ask_advice,chat_send,chat_load,join_room,leave_room, editor_send,editor_load, editor_save,editor_save_run,search_helper


# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We could path match here if we wanted.
websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ws_connect),
    # route("websocket.connect", ws_connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", ws_disconnect),
]

# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("room.receive", join_room, command="^join_room$"),
    route("room.receive", leave_room, command="^leave_room$"),

    route("room.receive", editor_send, command="^editor_send$"),
    route("room.receive", editor_save_run, command="^editor_save_run$"),
    route("room.receive", editor_save, command="^editor_save$"),
    route("room.receive", editor_load, command="^editor_load$"),

    route("room.receive", chat_send, command="^chat_send$"),
    route("room.receive", chat_load, command="^chat_load$"),

    route("room.receive", search_helper, command="^search_helper$"),
    route("room.receive", ask_advice, command="^ask_advice$"),
]
