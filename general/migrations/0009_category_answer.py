# Generated by Django 4.1.7 on 2023-06-29 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(max_length=200)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.answer')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.survey_user')),
            ],
        ),
    ]