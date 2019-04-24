from random import randint
from constance import config

from django.conf import settings
from django.core.mail import send_mail
from django.db import models, IntegrityError, transaction
from django.template.loader import render_to_string
from django.utils import timezone

from subscription_manager.subscription.models import Subscription

from .managers import PaymentManager


class Payment(models.Model):
    period = models.OneToOneField(
        to='subscription.Period',
        on_delete=models.CASCADE,
        verbose_name='Abo'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Betrag in CHF'
    )
    method = models.CharField(
        max_length=20,
        choices=(
            ('invoice', 'Rechnung'),
            ('twint', 'Twint')
        ),
        default='invoice',
        verbose_name='Zahlungsmethode'
    )
    code = models.CharField(
        max_length=12,
        unique=True
    )
    due_on = models.DateField(
        verbose_name='Zahlbar bis'
    )
    paid_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Bezahlter Betrag'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Bezahlt am'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Erstellt am'
    )

    objects = PaymentManager()

    class Meta:
        verbose_name = 'Zahlung'
        verbose_name_plural = 'Zahlungen'

    def __str__(self):
        return 'Zahlung für Abo {} von {}'.format(self.period.subscription.id, self.period.subscription.user.full_name)

    def is_paid(self):
        """
        Returns true if the paid at datetime is set.
        """
        return self.paid_at is not None
    is_paid.boolean = True

    def is_renewal(self):
        """
        Returns true if the payment is for a renewal.
        """
        return self.period.subscription.period_set.count() > 1
    is_renewal.boolean = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Overrides the save method. If the object is newly created,
        generate a code and set the due on date.
        """
        # If object is newly created
        if not self.pk:
            # Set due on date
            self.due_on = timezone.now().date() + config.PERIOD_OF_PAYMENT

            # Generate code
            while True:
                try:
                    code = 'ZS-' + str(randint(1000, 9999)) + '-' + str(randint(1000, 9999))
                    self.code = code
                    # Try creating the payment object
                    with transaction.atomic():
                        super().save(force_insert, force_update, using, update_fields)
                except IntegrityError:
                    continue
                break

        # If object existed already
        else:
            super().save(force_insert, force_update, using, update_fields)

    def handle(self):
        """
        Handles the payment by sending an invoice via email
        if the amount is not zero. Would also handle other
        payment methods.
        """
        # If purchase was for free, confirm payment
        if self.amount == 0:
            self.confirm()
            return True

        # Send invoice via email
        if self.method == 'invoice':
            self.send_invoice()
            return True

        # All other payment methods are not yet supported
        return False

    def send_invoice(self):
        """
        Sends an email that contains the payment details
        for this payment.
        """
        if not self.is_renewal:
            # New subscription
            template = 'emails/payment_invoice_new.txt'
        else:
            # Renewal subscription
            template = 'emails/payment_invoice_renewal.txt'

        # Add accounting emails to recipient list
        recipient_list = [self.period.subscription.user.email]
        recipient_list += config.EMAIL_ACCOUNTING.split(';')

        send_mail(
            subject=settings.EMAIL_SUBJECT_PREFIX + 'Rechnung',
            message=render_to_string(template, {
                'to_name': self.period.subscription.user.first_name,
                'payment': self
            }),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False
        )

    def confirm(self):
        """
        Confirms a payment by activating the subscription
        and sending a confirmation email.
        """
        # Confirm payment
        self.paid_at = timezone.now()
        self.save()

        # Adjust period interval
        self.period.start_date = timezone.now().date()
        self.period.end_date = (timezone.now() + self.period.subscription.plan.duration).date()
        self.period.save()

        if not self.is_renewal:
            # New subscription
            subject = 'Abo aktiviert'
            template = 'emails/payment_confirmation_new.txt'
        else:
            # Renewal subscription
            subject = 'Abo verlängert'
            template = 'emails/payment_confirmation_renewal.txt'

        # Send confirmation email
        send_mail(
            subject=settings.EMAIL_SUBJECT_PREFIX + subject,
            message=render_to_string(template, {
                'to_name': self.period.subscription.user.first_name,
                'payment': self
            }),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.period.subscription.user.email],
            fail_silently=False
        )
