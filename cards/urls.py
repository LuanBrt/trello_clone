from django.urls import path

from cards.views import add_card_view, add_item_view, card_view, delete_card_view, delete_item_view, moved_object_view, item_view

app_name = 'cards'
urlpatterns = [
    path('card/<str:uuid>', card_view, name='card'),
    path('delete/card/<str:uuid>', delete_card_view, name='delete-card'),
    path('add/card/', add_card_view, name='add-card'),

    path('item/<str:uuid>', item_view, name='item'),
    path('delete/item/<str:uuid>', delete_item_view, name='delete-item'),
    path('add/item/<str:card_uuid>', add_item_view, name='add-item'),
    
    path('moved/', moved_object_view, name='moved-object')
]