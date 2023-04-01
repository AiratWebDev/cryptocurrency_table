from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название криптовалюты')
    symbol = models.CharField(max_length=10, unique=True, verbose_name='Символьное название')
    price = models.FloatField(verbose_name='Курс')
    slug = models.CharField(max_length=50, unique=True, verbose_name='Слаг')
    percent_change_24h = models.FloatField(verbose_name='Изменение за 24 часа')
    volume_24h = models.BigIntegerField(verbose_name='Объем торгов за 24 часа')
    total_supply = models.IntegerField(verbose_name='Суммарное количество')
    market_cap = models.BigIntegerField(verbose_name='Рыночная капитализация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Криптовалюта'
        verbose_name_plural = 'Криптовалюты'
