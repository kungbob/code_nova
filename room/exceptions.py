import json

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """


    def __init__(self, message):

            # Call the base class constructor with the parameters it needs
        super(ClientError, self).__init__(message)

        # Now for your custom code...
        self.message = message
        # self.error_message = error_message

    def send_to(self, channel):
        channel.send({
            "text": json.dumps({
                "error": self.message,
            }),
        })
