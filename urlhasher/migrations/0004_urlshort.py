# Generated by Django 4.1.2 on 2023-04-02 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('urlhasher', '0003_alter_url_clicks_remaining'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlShort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=12, null=True, unique=True)),
                ('url', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='url_id', to='urlhasher.url', unique=True)),
            ],
        ),
    ]
