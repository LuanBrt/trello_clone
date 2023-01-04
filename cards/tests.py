
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from cards.models import Card, Item, Tag

# Create your tests here.

class ItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.card1 = Card.objects.create(user=self.user, title='card1')
        self.card2 = Card.objects.create(user=self.user, title='card2')


    def test_item_order(self):

        # testing if the creation of items will assign them correct orders
        item1 = Item.objects.create(card=self.card1, title='item1')
        item2 = Item.objects.create(card=self.card1, title='item2')

        self.assertEqual(item2.order, 2)
        self.assertEqual(item1.order, 1)

    def test_item_movement(self):

        # testing if the movement of items will assign them correct orders
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

        # testing if the post requests trigger the correct change of orders
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

class TagViewTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.c.post(reverse('accounts:login'), {'username': 'testuser', 'password': '12345'})

        self.tag1 = Tag.objects.create(name='tag1', color='#FFFFFF', user=self.user)
        self.tag2 = Tag.objects.create(name='tag2', color='#FFFFFF', user=self.user)
        self.card = Card.objects.create(title='card', user=self.user)
        self.item = Item.objects.create(title='item 1', card=self.card)

    def test_tag_attaching(self):
        # testing the view for managing an item tag's list
        self.c.post(reverse('cards:update-item-tags', kwargs={'uuid': self.item.uuid}), {'tag-update-item': [str(self.tag1.uuid)]})
        self.assertTrue(self.tag1 in self.item.tags.all())
        self.assertTrue(self.tag2 not in self.item.tags.all())

        self.c.post(reverse('cards:update-item-tags', kwargs={'uuid': self.item.uuid}), {'tag-update-item': [str(self.tag2.uuid)]})
        self.assertTrue(self.tag2 in self.item.tags.all())
        self.assertTrue(self.tag1 not in self.item.tags.all())

        