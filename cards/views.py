
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import django.views as views
from django.contrib.auth.mixins import LoginRequiredMixin
from cards.forms import ItemDescriptionForm, TagForm

from cards.models import Card, Item, Tag

# Create your views here.
@login_required
def index_view(request):
    cards = Card.objects.filter(user=request.user).order_by('order')
    tags_form = TagForm()
    return render(request, 'cards/index.html', {'cards': cards, 'tags_form': tags_form})

class CardListView(LoginRequiredMixin, views.View):
    def post(self, request):
        title = request.POST['newcard']
        if len(title) > 0:
            card = Card.objects.create(title=title, user=request.user)
        card.save()
        return render(request, 'cards/partials/card.html', {'card': card})

class CardView(LoginRequiredMixin, views.View):

    def get(self, request, uuid):

        card = get_object_or_404(Card, uuid=uuid, user=request.user)
        return render(request, 'cards/partials/card.html', {'card': card})

    def delete(self, request, uuid):

        card = get_object_or_404(Card, uuid=uuid, user=request.user)

        # we move the object to the last position so that the order of the other cards is updated
        Card.objects.move(card, card.get_max_order() + 1)
        card.delete()
        return HttpResponse()

class ItemListView(LoginRequiredMixin, views.View):

    def get(self, request, uuid):
        card = get_object_or_404(Card, uuid=uuid, user=request.user)
        items = card.get_items()

        if 'tag-filter-item' in request.GET.keys():
            for tag in request.GET.getlist('tag-filter-item'):
                items = items.filter(tags__uuid__contains=tag)

        return render(request, 'cards/partials/item.html', {'items': items})

    def post(self, request, uuid):
        card = get_object_or_404(Card, uuid=uuid, user=request.user)

        item_title = request.POST[f'newitem-{uuid}']
        if len(item_title) > 0:
            item = Item.objects.create(title=item_title, card=card)
            item.save()

            # we re-render the card items template, so that, in the html, we can select the last item and add it to the ui
            return render(request, 'cards/partials/item.html', {'items': card.get_items()})
        else:
            return HttpResponse()


class ItemView(LoginRequiredMixin, views.View):

    def get(self, request, uuid):
        item = get_object_or_404(Item, uuid=uuid, card__user=request.user)
        description_form = ItemDescriptionForm(None, instance=item)

        context = {'item': item, 'description_form': description_form}
        return render(request, 'cards/partials/item-details.html', context)

    def put(self, request, uuid):
        data = QueryDict(request.body)
        item = get_object_or_404(Item, uuid=uuid, card__user=request.user)

        description_form = ItemDescriptionForm(data, instance=item)
        if description_form.is_valid():
                description_form.save()
            
        return HttpResponse()

    def delete(self, request, uuid):
        item = get_object_or_404(Item, uuid=uuid, card__user=request.user)

        # we move the object to the last position so that the order of the other items is updated
        Item.objects.move(item, item.get_max_order() + 1)
        item.delete()

        return HttpResponse()


class TagListView(LoginRequiredMixin, views.View):
    
    def get(self, request):
        tags = Tag.objects.filter(user=request.user)
        return render(request, 'cards/partials/user-tags.html', {'tags': tags})

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
        response = HttpResponse()
        response['HX-Trigger-After-Settle'] = 'tag-added'
        return response

class TagView(LoginRequiredMixin, views.View):
    def delete(self, request, uuid):
        tag = get_object_or_404(Tag, uuid=uuid, user=request.user)
        if tag is not None:
            tag.delete()

        response = HttpResponse()
        response['HX-Trigger-After-Settle'] = 'tag-deleted'
        return response


@login_required
def manage_item_tags_view(request, uuid):
    item = get_object_or_404(Item, uuid=uuid, card__user=request.user)
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
def item_tags_view(request, uuid):
    item = get_object_or_404(Item, uuid=uuid, card__user=request.user)
    return render(request, 'cards/partials/item-tags.html', {'item': item})


@login_required
def moved_object_view(request):

    object_uuid = request.POST['movedItem']
    new_order = int(request.POST['order']) + 1

    if object_uuid.startswith('item-'):
        item = get_object_or_404(Item, uuid=object_uuid.replace('item-', ''), card__user=request.user)

        if request.POST['fromCard'] != request.POST['toCard']:
            Item.objects.move(item, item.get_max_order())

            item.card = get_object_or_404(Card, uuid=request.POST['toCard'].replace('parent-card-', ''), user=request.user)
            item.order = item.get_max_order() + 1
            item.save()
        
        Item.objects.move(item, new_order)

    elif object_uuid.startswith('card-'):
        card = get_object_or_404(Card, uuid=object_uuid.replace('card-', ''), user=request.user)
        Card.objects.move(card, new_order)

    return HttpResponse()

