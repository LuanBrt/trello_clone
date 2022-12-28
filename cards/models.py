import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings

from cards.order_manager import OrderManager

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    

    class Meta:
        abstract = True
        

class Card(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    objects = OrderManager()
    order = models.IntegerField(default=1)

    def get_items(self):
        return self.items.all().order_by('order')

    def get_max_order(self):
        if self.items.all().exists():
            return self.items.aggregate(models.Max('order'))['order__max']
        else:
            return 0

    def get_owner_objects(self):
        return Card.objects.filter(user=self.user)


class Item(BaseModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    objects = OrderManager()
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    content = models.TextField(null=True)

    def get_owner_objects(self):
        return self.card.get_items()




    