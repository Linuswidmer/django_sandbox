# models.py
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_waiting = models.BooleanField(default=False)
    num_wins = models.IntegerField(default=0)
    num_losses = models.IntegerField(default=0)
    time_played = models.IntegerField(default=0)

    def __str__(self):
        return self.name