# Generated by Django 4.0 on 2022-02-17 12:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=100)),
                ('delivery_address', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('type', models.CharField(choices=[('food', 'food'), ('acc', 'accompaniments'), ('bev', 'beverages')], max_length=100)),
                ('available', models.CharField(choices=[('Unavailable', 'unavailable'), ('Available', 'available')], max_length=50)),
                ('size', models.CharField(choices=[('Full', 'full'), (0.25, 'quarter'), (0.5, 'half')], max_length=20)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('coords', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(max_length=50)),
                ('open_status', models.CharField(choices=[('OP', 'open'), ('CL', 'closed')], max_length=10)),
                ('days_open', models.CharField(choices=[('Everyday', 'everyday'), ('Weekdays', 'weekdays'), ('Everyday excluding Sunday', 'everyday excluding sunday'), ('Everyday plus holidays', 'everyday plus holidays')], max_length=100)),
                ('fish_type', models.CharField(choices=[('Fresh, Ungutted, Chilled', 1), ('Fresh, Ungutted, Frozen', 2), ('Fresh, Gutted, Chilled', 3), ('Fresh, Gutted, Frozen', 4), ('Processed, Fillet, Chilled', 5), ('Processed, Fillet, Frozen', 6), ('Processed, Sundried', 7), ('Processed, Smoked', 8), ('Processed, Fried', 9)], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(choices=[('UP', 'Unprocessed'), ('P', 'Processed')], max_length=5)),
                ('label', models.CharField(choices=[('P', 'primary'), ('S', 'Processed'), ('D', 'danger')], max_length=2)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mongers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=80)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('coords', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.fooditem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.billingaddress')),
                ('items', models.ManyToManyField(to='store.RestaurantOrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=80)),
                ('location', models.CharField(max_length=100)),
                ('coords', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('open_status', models.CharField(choices=[('OP', 'open'), ('CL', 'closed')], max_length=10)),
                ('days_open', models.CharField(choices=[('Everyday', 'everyday'), ('Weekdays', 'weekdays'), ('Everyday excluding Sunday', 'everyday excluding sunday'), ('Everyday plus holidays', 'everyday plus holidays')], max_length=100)),
                ('food_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.fooditem')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpesa_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.billingaddress')),
                ('items', models.ManyToManyField(to='store.OrderItem')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        
    ]
