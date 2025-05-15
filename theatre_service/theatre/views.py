from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation
from .serializers import (
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    TicketSerializer,
    ReservationSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        queryset = self.get_queryset().filter(last_name__icontains=query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer

    @action(detail=True, methods=["get"])
    def performances(self, request, pk=None):
        play = self.get_object()
        performances = play.performances.all()
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        queryset = self.get_queryset().filter(show_time__gte=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=False, methods=["get"])
    def user_tickets(self, request):
        tickets = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @action(detail=False, methods=["get"])
    def my_reservations(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
