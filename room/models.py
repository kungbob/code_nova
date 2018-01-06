from django.db import models
from channels import Group
import json
from student.models import Student
from exercise.models import Exercise
# Create your models here.

class Room(models.Model):

    exercise = models.ForeignKey(Exercise,unique=False,
    on_delete=models.CASCADE,)
    owner = models.ForeignKey(Student, unique=False,
    related_name="room_owner_set", on_delete=models.CASCADE,)
    code = models.TextField(default="",blank=True)
    particpant = models.ManyToManyField(Student,related_name="room_participant_set")
    author = models.ManyToManyField(Student,related_name="room_author_set")
    chat_history = models.TextField(default='{"chat_history":[]}')
    require_help = models.BooleanField(default=False)

    def __str__(self):
        return "room-"+ str(self.id)



    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user):
    # def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        # final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}
        final_msg = {'room': str(self.id), 'message': message, 'user_id': user.id}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )

    def broadcast(self,message):
        self.websocket_group.send(
            {"text": json.dumps(message)}
        )
