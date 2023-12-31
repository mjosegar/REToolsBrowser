# Generated by Django 4.1.7 on 2023-06-29 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0009_category_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='general.question'),
        ),
        migrations.CreateModel(
            name='User_Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.survey_user')),
            ],
        ),
    ]
