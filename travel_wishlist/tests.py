from django.test import TestCase
from django.urls import reverse

from .models import Place


class TestHomePage(TestCase):
    
    def test_home_page_shows_empty_list_for_empty_database(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')


class TestWishList(TestCase):

    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


class TestPlacesVisitedNoPlaces(TestCase):

    def test_visited_places_list_contains_no_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet.')


class TestPlacesVisitedOnlyVisited(TestCase):

    fixtures = ['test_places']

    def test_only_visited_places_displayed_in_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')


class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places)) # check only one place
        tokyo_from_response = response_places[0]

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_database, tokyo_from_response)


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    # Switched from the videos, I changed the render template to visited.html
    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')

        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)


    def test_non_existent_place(self):
        visit_nonexistent_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_nonexistent_place_url, follow=True)
        self.assertEqual(404, response.status_code)
        