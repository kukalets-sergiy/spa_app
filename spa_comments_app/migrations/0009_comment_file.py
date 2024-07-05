# Generated by Django 4.2 on 2024-07-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("spa_comments_app", "0008_alter_comment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="file",
            field=models.FileField(
                blank=True,
                help_text="Upload an image or text file.",
                null=True,
                upload_to="comment_files/",
            ),
        ),
    ]
