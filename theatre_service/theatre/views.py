from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle

from .models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import (
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    TicketSerializer,
    ReservationSerializer,
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        queryset = self.get_queryset().filter(last_name__icontains=query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.select_related('genre').prefetch_related('actors').all()
    serializer_class = PlaySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

    @action(detail=True, methods=["get"])
    def performances(self, request, pk=None):
        play = self.get_object()
        performances = play.performances.select_related('theatre_hall', 'play').all()
        page = self.paginate_queryset(performances)
        if page is not None:
            serializer = PerformanceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)

class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related('play', 'theatre_hall').all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        queryset = self.get_queryset().filter(show_time__gte=timezone.now())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('performance', 'user').all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def user_tickets(self, request):
        tickets = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related('user').prefetch_related('tickets').all()
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrAdmin]
    pagination_class = StandardResultsSetPagination
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my_reservations(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

