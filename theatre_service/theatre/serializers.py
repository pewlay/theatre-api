from rest_framework import serializers
from models import (Genre,
                    Actor,
                    Play,
                    TheatreHall,
                    Performance,
                    Ticket,
                    Reservation
                    )

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class PlaySerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True
    )
    actors = ActorSerializer(many=True, read_only=True)
    actor_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all(), source='actors', write_only=True
    )

    class Meta:
        model = Play
        fields = ['id', 'title', 'description', 'genre', 'genre_id', 'actors', 'actor_ids']


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True)
    play_id = serializers.PrimaryKeyRelatedField(
        queryset=Play.objects.all(), source="play", write_only=True
    )
    theatre_hall = TheatreHallSerializer(read_only=True)
    theatre_hall_id = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all(), source="theatre_hall", write_only=True
    )

    class Meta:
        model = Performance
        fields = ["id", "play", "play_id", "theatre_hall", "theatre_hall_id", "show_time"]


class TicketSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(read_only=True)
    performance_id = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all(), source="performance", write_only=True
    )

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "performance_id"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    ticket_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ticket.objects.all(), source="tickets", write_only=True
    )

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "ticket_ids", "created_at")