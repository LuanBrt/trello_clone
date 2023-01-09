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
    
    def get_items(self):
        return self.items.all().order_by('order')

    def __str__(self):
        return f'{self.title}-({self.order})'

    objects = OrderManager()
    order = models.IntegerField(default=1)
    def get_owner_objects(self):
        return Card.objects.filter(user=self.user)

    def get_max_order(self):
        if self.get_owner_objects().exists():
            return self.get_owner_objects().aggregate(models.Max('order'))['order__max']
        else:
            return 0


class Tag(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tag')
    name = models.CharField(max_length=90)
    color = models.CharField(max_length=30)

class Item(BaseModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    description = models.CharField(null=True, max_length=400)
    due_date = models.DateField(null=True)
    tags = models.ManyToManyField(Tag)

    objects = OrderManager()
    order = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.title}-({self.order})'

    def get_owner_objects(self):
        return self.card.get_items()

    
    def get_max_order(self):
        if self.get_owner_objects().exists():
            return self.get_owner_objects().aggregate(models.Max('order'))['order__max']
        else:
            return 0






    