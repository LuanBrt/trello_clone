
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cards.forms import ItemDescriptionForm, TagForm

from cards.models import Card, Item, Tag

# Create your views here.
@login_required
def index_view(request):
    cards = Card.objects.filter(user=request.user).order_by('order')
    tags_form = TagForm()
    return render(request, 'cards/index.html', {'cards': cards, 'tags_form': tags_form})

@login_required
def card_view(request, uuid):
    card = Card.objects.get(uuid=uuid, user=request.user)
    return render(request, 'cards/partials/card.html', {'card': card})

@login_required
def user_tags_view(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'cards/partials/user-tags.html', {'tags': tags})

@login_required
def add_tag_view(request):
    form = TagForm(request.POST)
    if form.is_valid():
        tag = form.save(commit=False)
        tag.user = request.user
        tag.save()
    response = HttpResponse()
    response['HX-Trigger-After-Settle'] = 'tag-added'
    return response

@login_required
def manage_item_tags_view(request, uuid):
    item = Item.objects.get(uuid=uuid, card__user=request.user)
    selected_tags = request.POST.getlist('tag-update-item')
    all_tags = request.user.tag.all()

    for tag in all_tags:
        if str(tag.uuid) in selected_tags and tag not in item.tags.all():
            item.tags.add(tag)

        elif str(tag.uuid) not in selected_tags and tag in item.tags.all():
            item.tags.remove(tag)

    response = HttpResponse()
    response['HX-Trigger-After-Settle'] = f'item-{item.uuid}-tags-update'
    return response

@login_required
def delete_tag_view(request, uuid):
    tag = Tag.objects.get(user=request.user, uuid=uuid)
    if tag is not None:
        tag.delete()

    response = HttpResponse()
    response['HX-Trigger-After-Settle'] = 'tag-deleted'
    return response

@login_required
def card_items_view(request, uuid):
    card = Card.objects.get(uuid=uuid, user=request.user)
    items = card.get_items()
    if 'tag-filter-item' in request.GET.keys():

        for tag in request.GET.getlist('tag-filter-item'):

            items = items.filter(tags__uuid__contains=tag)
    return render(request, 'cards/partials/item.html', {'items': items})

@login_required
def item_details_view(request, uuid):
    
    item = Item.objects.get(uuid=uuid, card__user=request.user)
    description_form = ItemDescriptionForm(request.POST or None, instance=item)

    if request.POST:
        if description_form.is_valid():
            description_form.save()
        
        return HttpResponse()


    context = {'item': item, 'description_form': description_form}
    return render(request, 'cards/partials/item-details.html', context)

@login_required
def item_tags_view(request, uuid):
    item = Item.objects.get(uuid=uuid, card__user=request.user)
    return render(request, 'cards/partials/item-tags.html', {'item': item})

@login_required
def add_item_view(request, card_uuid):
    card = Card.objects.get(uuid=card_uuid, user=request.user)
    item_title = request.POST[f'newitem-{card_uuid}']
    if len(item_title) > 0:
        item = Item.objects.create(title=item_title, card=card)
        item.save()

        # we re-render the card items template, so that, in the html, we can select the last item and add it to the ui
        return render(request, 'cards/partials/item.html', {'items': card.get_items()})
    else:
        return HttpResponse()

@login_required
def add_card_view(request):
    card = Card.objects.create(title=request.POST['newcard'], user=request.user)
    card.save()
    return render(request, 'cards/partials/card.html', {'card': card})

@login_required
def delete_card_view(request, uuid):
    card = Card.objects.get(uuid=uuid, user=request.user)

    if card is not None:
        card.delete()

    return HttpResponse()

@login_required
def delete_item_view(request, uuid):
    item = Item.objects.get(uuid=uuid, card__user=request.user)

    if item is not None:
        item.delete()

    return HttpResponse()

@login_required
def moved_object_view(request):

    object_uuid = request.POST['movedItem']
    new_order = int(request.POST['order']) + 1

    if object_uuid.startswith('item-'):
        item = Item.objects.get(uuid=object_uuid.replace('item-', ''))

        if request.POST['fromCard'] != request.POST['toCard']:
            Item.objects.move(item, item.card.get_max_order())

            item.card = Card.objects.get(uuid=request.POST['toCard'].replace('parent-card-', ''), user=request.user)
            item.order = item.card.get_max_order() + 1
            item.save()
        
        Item.objects.move(item, new_order)

    elif object_uuid.startswith('card-'):
        card = Card.objects.get(uuid=object_uuid.replace('card-', ''), user=request.user)
        Card.objects.move(card, new_order)

    return HttpResponse()