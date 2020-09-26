from django.db import models


class Message(models.Model):
    sender = models.CharField('Sender', max_length=128)
    receiver = models.CharField('Receiver', max_length=128)
    message = models.CharField('Message', max_length=4096)
    subject = models.CharField('Subject', max_length=512)
    creation_date = models.DateTimeField('Sent on')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
