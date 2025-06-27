from django.db import models
from customers.models import AddCustomerModel

GEHRA = [
    ('gool', 'گول'),
    ('chorus', 'چورس'),
    ('kurta', 'کرتا'),
]

ASTEEN = [
    ('kaf', 'کاف'),
    ('double_kaf', 'ڈبل کاف'),
    ('gool', 'گول'),
    ('kani', 'کانی'),
    ('other', 'دیگر'),
]

GALA = [
    ('half ban', 'ہاف بین'),
    ('collar', 'کالر'),
    ('sada','سادہ گلا'),
    ('full ban', 'فل بین'),
    ('v_gala','وی گلا'),
    ('shabazi', 'شبازی'),
]

SEELAI = [
    ('single', 'سنگل'),
    ('double', 'ڈبل'),
    ('triple', 'ٹرپل'),
    ('ghoom', 'گھوم'),
    ('chamak','چمک داگھہ')
]

class AddMeasurementModel(models.Model):
    customer = models.ForeignKey(AddCustomerModel, on_delete=models.CASCADE, blank=True, verbose_name='کسٹمر')
    lambayi = models.DecimalField(verbose_name='لمبائی', default=0, decimal_places=2, max_digits=5)
    choriyi = models.DecimalField(verbose_name='چوڑائی', default=0, decimal_places=2, max_digits=5)
    chest = models.DecimalField(verbose_name='چھاتی', default=0, decimal_places=2, max_digits=5)
    bazoo = models.DecimalField(verbose_name='بازو', default=0, decimal_places=2, max_digits=5)
    asteen = models.CharField(verbose_name='آستین', max_length=20, choices=ASTEEN, default='kaf')
    asteen_choriti = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='آستین چوڑائی')
    monda = models.DecimalField(verbose_name='مونڈھا', default=0, decimal_places=2, max_digits=5)
    teera = models.DecimalField(verbose_name='تیرا', default=0, decimal_places=2, max_digits=5)
    gala = models.DecimalField(verbose_name='گلا سائز', default=0, decimal_places=2, max_digits=5)
    gala_type = models.CharField(choices=GALA, default='half ban', max_length=30, verbose_name='گلا قسم')
    shalwar = models.DecimalField(verbose_name='شلوار', default=0, decimal_places=2, max_digits=5)
    pancha = models.DecimalField(verbose_name='پانچہ', default=0, decimal_places=2, max_digits=5)
    gehra = models.CharField(verbose_name='گہرا', max_length=20, default='gool', choices=GEHRA)
    pockets = models.CharField(max_length=100, verbose_name='پاکٹ')
    seelai = models.CharField(max_length=20, verbose_name='سلائی', choices=SEELAI, default='single')
    extra = models.TextField(verbose_name='باقی معلومات', blank=True, null=True)

    def __str__(self):
        return self.customer.customer_name