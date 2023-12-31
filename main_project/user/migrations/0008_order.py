# Generated by Django 4.2.1 on 2023-06-26 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0003_alter_products_main_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0007_address_aduser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Status', models.CharField(max_length=50)),
                ('Qty', models.PositiveIntegerField()),
                ('PaymentMethod', models.CharField(max_length=20)),
                ('Date', models.DateField(auto_now_add=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.products')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address')),
                ('user_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
