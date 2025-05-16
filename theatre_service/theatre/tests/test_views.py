from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from theatre.models import Genre
from django.contrib.auth import get_user_model

User = get_user_model()

class GenreViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass1234')
        self.client.login(username='user1', password='pass1234')
        self.genre = Genre.objects.create(name='Comedy')

    def test_list_genres(self):
        url = reverse('theatre:genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Comedy')

    def test_create_genre(self):
        url = reverse('theatre:genre-list')
        data = {'name': 'Horror'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

    def test_update_genre(self):
        url = reverse('theatre:genre-detail', args=[self.genre.id])
        data = {'name': 'Romantic Comedy'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, 'Romantic Comedy')

    def test_delete_genre(self):
        url = reverse('theatre:genre-detail', args=[self.genre.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)
