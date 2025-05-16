from django.test import TestCase
from django.contrib.auth import get_user_model
from theatre.models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation
from datetime import datetime, timedelta

User = get_user_model()

class TheatreModelsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.genre = Genre.objects.create(name='Drama')
        self.actor = Actor.objects.create(first_name='John', last_name='Doe')
        self.play = Play.objects.create(title='Hamlet', description='A tragedy', genre=self.genre)
        self.play.actors.add(self.actor)
        self.hall = TheatreHall.objects.create(name='Main Hall', rows=10, seats_in_row=20)
        self.performance = Performance.objects.create(play=self.play, theatre_hall=self.hall, show_time=datetime.now() + timedelta(days=1))
        self.ticket = Ticket.objects.create(performance=self.performance, row=1, seat=1, user=self.user)
        self.reservation = Reservation.objects.create(user=self.user)
        self.reservation.tickets.add(self.ticket)

    def test_genre_str(self):
        self.assertEqual(str(self.genre), 'Drama')

    def test_actor_str(self):
        self.assertEqual(str(self.actor), 'John Doe')

    def test_play_str(self):
        self.assertEqual(str(self.play), 'Hamlet')

    def test_hall_str(self):
        self.assertEqual(str(self.hall), 'Main Hall')

    def test_performance_str(self):
        self.assertIn('Hamlet', str(self.performance))

    def test_ticket_str(self):
        self.assertIn('Row 1', str(self.ticket))

    def test_reservation_str(self):
        self.assertIn('testuser', str(self.reservation))
