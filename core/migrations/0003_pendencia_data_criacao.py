from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_documento_nome_arquivo_documento_arquivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendencia',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
