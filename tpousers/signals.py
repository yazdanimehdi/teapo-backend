from django.db.models.signals import post_save
import channels.layers
from asgiref.sync import async_to_sync
from tpousers.models import OrderPendingPayment


def transaction_ws(sender, instance, **kwargs):
    if instance.order_speaking is not None:
        user = instance.order_speaking.user
    elif instance.order_writing is not None:
        user = instance.order_writing.user
    else:
        user = None

    if user is not None:
        message = instance.status
        layer = channels.layers.get_channel_layer()
        async_to_sync(layer.group_send)('user' + str(user.id), {
            'type': 'events.transaction',
            'content': message
        })


post_save.connect(transaction_ws, sender=OrderPendingPayment, dispatch_uid="transaction_post_save")
