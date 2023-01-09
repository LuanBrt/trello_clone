from django.urls import path

# from cards.views import add_card_view, add_item_view, add_tag_view, card_items_view, card_view, delete_card_view, delete_item_view, delete_tag_view, item_details_view, item_tags_view, manage_item_tags_view, moved_object_view, user_tags_view
from cards.views import CardListView, CardView, ItemListView, ItemView, TagListView, TagView, item_tags_view, manage_item_tags_view, moved_object_view


app_name = 'cards'
urlpatterns = [
    path('cards/', CardListView.as_view(), name='card-list'),
    path('card/<str:uuid>', CardView.as_view(), name='card'),

    path('card/<str:uuid>/items', ItemListView.as_view(), name='items-list'),
    path('item/<str:uuid>', ItemView.as_view(), name='item'),

    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tag/<str:uuid>', TagView.as_view(), name='tag'),


    path('item/<str:uuid>/tags/', item_tags_view, name='item-tags'),
    path('item/<str:uuid>/tags/update', manage_item_tags_view, name='update-item-tags'),
    path('moved/', moved_object_view, name='moved-object')
]