from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cards.models import Card, Item

# Create your views here.
@login_required
def index_view(request):
    cards = Card.objects.filter(user=request.user).order_by('order')
    return render(request, 'cards/index.html', {'cards': cards})

@login_required
def card_view(request, uuid):
    card = Card.objects.get(uuid=uuid, user=request.user)
    return render(request, 'cards/partials/card.html', {'card': card})

@login_required
def item_view(request, uuid):
    item = Item.objects.get(uuid=uuid, card__user=request.user)
    return render(request, 'cards/partials/item.html', {'item': item})

@login_required
def add_item_view(request, card_uuid):
    card = Card.objects.get(uuid=card_uuid, user=request.user)
    item_title = request.POST[f'newitem-{card_uuid}']
    if len(item_title) > 0:
        item = Item.objects.create(title=item_title, card=card)
        item.save()

        return render(request, 'cards/partials/item.html', {'item': item})
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
    item = Item.objects.get(uuid=uuid, user=request.user)

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