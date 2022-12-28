from django.db import models, transaction
from django.db.models import F, Max


class OrderManager(models.Manager):

    def move(self, obj, new_order):
        """Moves object to new position"""

        qs = obj.get_owner_objects()

        with transaction.atomic():
            if obj.order > int(new_order):
                qs.filter(order__lt=obj.order,
                order__gte=new_order,
                ).exclude(pk=obj.pk
                ).update(order=F('order') + 1)
            else:
                qs.filter(order__lte=new_order,
                order__gt=obj.order
                ).exclude(pk=obj.pk
                ).update(order=F('order') - 1)
        
            obj.order = new_order 
            obj.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with transaction.atomic():
            results = instance.get_owner_objects().aggregate(
                Max('order')
            )

            current_order = results['order__max']
            if current_order is None:
                current_order = 0

            value = current_order + 1
            instance.order = value
            instance.save()

            return instance