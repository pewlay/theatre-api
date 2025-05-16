from rest_framework import serializers
from .models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Ticket,
    Reservation
)

class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(help_text="Назва жанру театральної вистави")

    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(help_text="Ім'я актора")
    last_name = serializers.CharField(help_text="Прізвище актора")

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class PlaySerializer(serializers.ModelSerializer):
    title = serializers.CharField(help_text="Назва вистави")
    description = serializers.CharField(help_text="Опис вистави")
    genre = GenreSerializer(read_only=True, help_text="Жанр вистави")
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source='genre',
        write_only=True,
        help_text="ID жанру вистави"
    )
    actors = ActorSerializer(many=True, read_only=True, help_text="Список акторів")
    actor_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all(),
        source='actors',
        write_only=True,
        help_text="Список ID акторів"
    )

    class Meta:
        model = Play
        fields = ['id', 'title', 'description', 'genre', 'genre_id', 'actors', 'actor_ids']


class TheatreHallSerializer(serializers.ModelSerializer):
    name = serializers.CharField(help_text="Назва театральної зали")
    rows = serializers.IntegerField(help_text="Кількість рядів у залі")
    seats_in_row = serializers.IntegerField(help_text="Кількість місць у ряді")

    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True, help_text="Вистава")
    play_id = serializers.PrimaryKeyRelatedField(
        queryset=Play.objects.all(),
        source="play",
        write_only=True,
        help_text="ID вистави"
    )
    theatre_hall = TheatreHallSerializer(read_only=True, help_text="Театральна зала")
    theatre_hall_id = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all(),
        source="theatre_hall",
        write_only=True,
        help_text="ID театральної зали"
    )
    show_time = serializers.DateTimeField(help_text="Дата та час показу")

    class Meta:
        model = Performance
        fields = ["id", "play", "play_id", "theatre_hall", "theatre_hall_id", "show_time"]


class TicketSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(read_only=True, help_text="Показ вистави")
    performance_id = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all(),
        source="performance",
        write_only=True,
        help_text="ID показу вистави"
    )
    row = serializers.IntegerField(help_text="Ряд місця")
    seat = serializers.IntegerField(help_text="Номер місця в ряді")

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "performance_id"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, help_text="Список квитків у броні")
    ticket_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ticket.objects.all(),
        source="tickets",
        write_only=True,
        help_text="Список ID квитків для бронювання"
    )
    created_at = serializers.DateTimeField(help_text="Дата та час створення броні")

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "ticket_ids", "created_at")
