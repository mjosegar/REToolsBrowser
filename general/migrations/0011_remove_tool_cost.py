# Generated by Django 4.1.7 on 2023-07-02 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0010_remove_answer_user_answer_question_user_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='cost',
        ),
    ]
