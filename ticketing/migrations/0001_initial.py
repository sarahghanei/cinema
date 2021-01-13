# Generated by Django 3.1.2 on 2020-12-16 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('cinema_code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='نام')),
                ('city', models.CharField(default='تهران', max_length=30, verbose_name='شهر')),
                ('capacity', models.IntegerField(verbose_name='ظرفیت')),
                ('phone', models.CharField(max_length=30, null=True, verbose_name='شماره تماس')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('image', models.ImageField(blank=True, null=True, upload_to='cinema_images/', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'سینما',
                'verbose_name_plural': 'سینما',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='عنوان')),
                ('director', models.CharField(max_length=50, verbose_name='کارگردان')),
                ('year', models.IntegerField(verbose_name='سال تولید')),
                ('genre', models.CharField(blank=True, max_length=100, null=True, verbose_name='ژانر')),
                ('length', models.IntegerField(verbose_name='مدت زمان پخش')),
                ('description', models.TextField(verbose_name='توضیح')),
                ('poster', models.ImageField(upload_to='movie_posters/', verbose_name='پوستر')),
            ],
            options={
                'verbose_name': 'فیلم',
                'verbose_name_plural': 'فیلم',
            },
        ),
        migrations.CreateModel(
            name='ShowTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='زمان شروع')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('salable_seats', models.IntegerField(verbose_name='صندلی های قابل فروش')),
                ('free_seats', models.IntegerField(verbose_name='صندلی های فروخته نشده')),
                ('status', models.IntegerField(choices=[(1, 'فروش اغاز نشده'), (2, 'در حال فروش بلیط'), (3, 'بلیط ها تمام شد'), (4, 'فروش بلیط بسته شد'), (5, 'فیلم پخش شد'), (6, 'سانس لغو شد')], verbose_name='وضعیت')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.cinema', verbose_name='سینما')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.movie', verbose_name='فیلم')),
            ],
            options={
                'verbose_name': 'سانس',
                'verbose_name_plural': 'سانس',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_count', models.IntegerField(verbose_name='تعداد صندلی')),
                ('order_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان خرید')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.profile', verbose_name='خریدار')),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.showtime', verbose_name='سانس')),
            ],
            options={
                'verbose_name': 'بلیت',
                'verbose_name_plural': 'بلیت',
            },
        ),
    ]