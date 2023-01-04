from django.urls import path

from cards.views import add_card_view, add_item_view, add_tag_view, card_items_view, card_view, delete_card_view, delete_item_view, delete_tag_view, item_details_view, item_tags_view, manage_item_tags_view, moved_object_view, user_tags_view

app_name = 'cards'
urlpatterns = [
    path('card/<str:uuid>', card_view, name='card'),
    path('delete/card/<str:uuid>', delete_card_view, name='delete-card'),
    path('add/card/', add_card_view, name='add-card'),

    path('card/<str:uuid>/items', card_items_view, name='card-items'),


    path('tags/', user_tags_view, name='user-tags'),
    path('add/tag/', add_tag_view, name='add-tag'),
    path('delete/tag/<str:uuid>', delete_tag_view, name='delete-tag'),


    path('item/<str:uuid>/tags/', item_tags_view, name='item-tags'),
    path('item/<str:uuid>/tags/update', manage_item_tags_view, name='update-item-tags'),
    
    path('item/<str:uuid>/details/', item_details_view, name='item-details'),
    path('delete/item/<str:uuid>', delete_item_view, name='delete-item'),
    path('add/item/<str:card_uuid>', add_item_view, name='add-item'),
    
    path('moved/', moved_object_view, name='moved-object')
]