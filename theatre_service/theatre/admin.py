from django.contrib import admin
from .models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')

@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')
    list_filter = ('genre',)
    search_fields = ('title', 'description')
    filter_horizontal = ('actors',)

@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rows', 'seats_in_row')
    search_fields = ('name',)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'play', 'theatre_hall', 'show_time')
    list_filter = ('play', 'theatre_hall')
    search_fields = ('play__title',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance', 'row', 'seat', 'user')
    list_filter = ('performance',)
    search_fields = ('user__username',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'
