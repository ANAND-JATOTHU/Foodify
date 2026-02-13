from django.apps import AppConfig


class PaymentSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment_system'
    verbose_name = 'Payment System'

    def ready(self):
        """Import signals when app is ready"""
        import payment_system.signals
