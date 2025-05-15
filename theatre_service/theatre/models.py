from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="plays")
    actors = models.ManyToManyField(Actor, related_name="plays")

    def __str__(self):
        return self.title

class TheatreHall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} at {self.show_time}"

class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("performance", "row", "seat")

    def __str__(self):
        return f"Ticket for {self.performance} - Row {self.row}, Seat {self.seat}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    tickets = models.ManyToManyField(Ticket, related_name="reservations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation #{self.pk} by {self.user.username}"
