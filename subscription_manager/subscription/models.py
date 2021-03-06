from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .managers import PlanManager, SubscriptionManager, PeriodManager


class Plan(models.Model):
    """
    Model that holds the data for a plan (a type of subscription).
    Such a plan can or cannot be purchased by users.
    """
    name = models.CharField(
        max_length=50,
        verbose_name='Name'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Beschreibung'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug'
    )
    duration = models.DurationField(
        default=timezone.timedelta(days=365),
        verbose_name='Laufzeit'
    )
    price = models.PositiveIntegerField(
        verbose_name='Preis'
    )
    is_purchasable = models.BooleanField(
        default=True,
        verbose_name='Käuflich'
    )
    is_renewable = models.BooleanField(
        default=True,
        verbose_name='Erneuerbar'
    )
    eligible_active_subscriptions_per_user = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Anzahl aktiver Abos pro Leserin',
        help_text='Kein Wert bedeutet, dass es keine Begrenzung gibt.'
    )
    eligible_email_domains = models.TextField(
        blank=True,
        default='',
        verbose_name='Berechtigte E-Mail-Domains',
        help_text='E-Mail-Adressen müssen mit einem Semikolon getrennt sein.'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Erstellt am'
    )

    class Meta:
        verbose_name = 'Abotyp'
        verbose_name_plural = 'Abotypen'

    objects = PlanManager()

    def __str__(self):
        return self.name

    def get_eligible_email_domains(self):
        """
        Returns a list of the eligible email domains.
        """
        if self.eligible_email_domains is None:
            return []

        eligible_email_domains_list = self.eligible_email_domains.split(';')
        return list(filter(None, eligible_email_domains_list))

    def get_readable_eligible_email_domains(self, conjunction='oder'):
        """
        Returns a readable string of the eligible email domains.
        """
        # Prefixes the @-symbol to all domains
        eligible_email_domains = ['@' + email_domain for email_domain in self.get_eligible_email_domains()]

        # Converts list to string of comma- and conjunction-separated domains and returns it
        if len(eligible_email_domains) == 0:
            return ''
        elif len(eligible_email_domains) == 1:
            return eligible_email_domains[0]
        else:
            return ', '.join(eligible_email_domains[:-1]) + ' ' + conjunction + ' ' + eligible_email_domains[-1]

    def is_eligible(self, user, purpose='purchase'):
        """
        Checks whether a given user is eligible
        to purchase the subscription.
        """
        if user is not None and self in Plan.objects.filter_eligible(user, purpose):
            return True
        return False
    is_eligible.boolean = True


class Subscription(models.Model):
    """
    Model that holds the data for a user's subscription (an instance of a plan).
    A purchased plan corresponds to a subscription.
    """
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Account'
    )
    plan = models.ForeignKey(
        to='Plan',
        on_delete=models.PROTECT,
        verbose_name='Abotyp'
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='Vorname'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Nachname'
    )
    address_line = models.CharField(
        max_length=100,
        verbose_name='Adresszeile'
    )
    additional_address_line = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Zusätzliche Adresszeile'
    )
    postcode = models.CharField(
        max_length=8,
        verbose_name='Postleitzahl'
    )
    town = models.CharField(
        max_length=100,
        verbose_name='Ort'
    )
    country = models.CharField(
        max_length=50,
        default='Schweiz',
        verbose_name='Land'
    )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Gekündigt am'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Erstellt am'
    )

    objects = SubscriptionManager()

    class Meta:
        verbose_name = 'Abo'
        verbose_name_plural = 'Abos'

    def __str__(self):
        return 'Abo #{} ({} {}, {})'.format(self.pk, self.first_name, self.last_name, self.town)

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def has_ended(self):
        """
        True if the subscription has ended.
        """
        return self.end_date is not None and self.end_date <= timezone.now().date()
    has_ended.boolean = True

    def get_first_period(self):
        """
        Returns the first period of the subscription.
        """
        return self.period_set.order_by('start_date').first()

    def get_last_period(self):
        """
        Returns the last period of the subscription.
        """
        return self.period_set.order_by('start_date').last()

    def is_renewable(self):
        """
        Returns true if the subscription can be renewed by its user.
        """
        if self.plan.is_eligible(self.user, 'renewal') and self.expires_in_lte(30) and self.is_paid:
            return True
        return False
    is_renewable.boolean = True

    def renew(self):
        """
        Renews the subscription by the duration of the plan.
        """
        # Get last period
        last_period = self.get_last_period()
        if last_period is None:
            return None

        # Create new period object
        return Period.objects.create(
            subscription=self,
            start_date=last_period.end_date + timezone.timedelta(days=1),
            end_date=last_period.end_date + timezone.timedelta(days=1) + self.plan.duration
        )

    def expires_in_lte(self, days):
        """
        Returns true if subscription expires in less than
        the given amount of days.
        """
        # Check if end_date is instance of date
        return self.end_date <= timezone.now().date() + timezone.timedelta(days=days)


class Period(models.Model):
    """
    Model that holds the data of a period. A period is one cycle of a user's
    subscription. If a user renews her subscription, a new period is created
    for that subscription.
    """
    subscription = models.ForeignKey(
        to='Subscription',
        on_delete=models.CASCADE,
        verbose_name='Abonnement'
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Anfangsdatum'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Enddatum'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Erstellt am'
    )

    objects = PeriodManager()

    class Meta:
        verbose_name = 'Periode'
        verbose_name_plural = 'Perioden'

    def __str__(self):
        return 'Periode #{} ({} bis {})'.format(self.pk, self.start_date, self.end_date)

    def has_started(self):
        """
        True if the period has started.
        """
        return self.start_date is not None and self.start_date <= timezone.now().date()
    has_started.boolean = True

    def has_ended(self):
        """
        True if the period has ended.
        """
        return self.end_date is not None and self.end_date <= timezone.now().date()
    has_ended.boolean = True

    def is_active(self):
        """
        The period is active if it has started but not ended yet.
        These inequations have to hold: start_date <= now < end_date.
        It has also to be paid.
        """
        return self.has_started() and not self.has_ended() and self.payment.is_paid()
    is_active.boolean = True
