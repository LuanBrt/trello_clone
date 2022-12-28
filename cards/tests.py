from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from cards.models import Card, Item

# Create your tests here.

class ItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.card1 = Card.objects.create(user=self.user, title='card1')
        self.card2 = Card.objects.create(user=self.user, title='card2')


    def test_item_order(self):

        item1 = Item.objects.create(card=self.card1, title='item1')
        item2 = Item.objects.create(card=self.card1, title='item2')

        self.assertEqual(item2.order, 2)
        self.assertEqual(item1.order, 1)

    def test_item_movement(self):

        item1 = Item.objects.create(card=self.card1, title='item1')
        item2 = Item.objects.create(card=self.card1, title='item2')

        Item.objects.move(item2, 1)

        item1 = Item.objects.get(id=item1.id)
        item2 = Item.objects.get(id=item2.id)

        self.assertEqual(item2.order, 1)
        self.assertTrue(item1.order > item2.order)

class ItemViewTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.c.post(reverse('accounts:login'), {'username': 'testuser', 'password': '12345'})

        self.card1 = Card.objects.create(user=self.user, title='card1')
        self.card2 = Card.objects.create(user=self.user, title='card2')

        self.item1 = Item.objects.create(card=self.card1, title='item1')
        self.item2 = Item.objects.create(card=self.card1, title='item2')

    
    def test_between_cards_movement(self):
        self.c.post(reverse('cards:moved-object'), {'fromCard': f'parent-card-{self.card1.uuid}',
                                                    'toCard': f'parent-card-{self.card2.uuid}',
                                                    'order': '0',
                                                    'movedItem': f'item-{self.item1.uuid}'})
        item1 = Item.objects.get(id=self.item1.id)
        item2 = Item.objects.get(id=self.item2.id)
        self.assertTrue(item1.order == 1)
        self.assertTrue(item2.order == 1)

class CardModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_card_creation(self):
        card1 = Card.objects.create(user=self.user, title='card1')
        card2 = Card.objects.create(user=self.user, title='card2')

        self.assertTrue(card2.order > card1.order)