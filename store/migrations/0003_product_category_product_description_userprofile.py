# Generated by Django 4.1.3 on 2023-05-24 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Clothes', 'Clothes'), ('Shoes', 'Shoes'), ('Hair Wigs', 'Hair Wigs'), ('Jewelry', 'Jewelry'), ('Cosmetics', 'Cosmetics'), ('Foods & Beverages', 'Foods & Beverages'), ('Furnitures', 'Furnitures'), ('Office Equiptments', 'Office Equiptments'), ('Books', 'Books'), ('Game Accessories', 'Game Accessories'), ('Electronics', 'Electronics'), ('Beauty & Fashion', 'Beauty & Fashion'), ('Auto & Parts', 'Auto & Parts'), ('Kenyan Foods', 'Kenyan Foods')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=100, null=True)),
                ('lastName', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_pic', models.ImageField(default='avatar.png', upload_to='profileImages')),
                ('phoneNumber', models.IntegerField(null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=100)),
                ('profession', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField()),
                ('homeAddress', models.CharField(blank=True, max_length=200, null=True)),
                ('mailingAddress', models.CharField(blank=True, max_length=100, null=True)),
                ('about', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
