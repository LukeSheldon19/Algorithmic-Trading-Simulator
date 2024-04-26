import uuid

from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    activities = models.TextField()

    def __str__(self):
        return "<Profile id={} first_name={} last_name={}>".format(
            self.id, self.first_name, self.last_name
        )

    @property
    def latest_status(self):
        return self.status_set.order_by("-date_time").first()


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    date_time = models.DateTimeField()
    profile = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return f"<Status from={self.profile_id} at={self.date_time}>"


class Poke(models.Model):
    poker = models.ForeignKey(
        Profile, null=False, on_delete=models.CASCADE, related_name="poke_poker"
    )
    pokee = models.ForeignKey(
        Profile, null=False, on_delete=models.CASCADE, related_name="poke_pokee"
    )
    date_time = models.DateTimeField()

    def __str__(self):
        return f"<Poke from={self.poker_id} to={self.pokee_id} at={self.date_time}>"
