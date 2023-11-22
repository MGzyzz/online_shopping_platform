from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_merge_20231103_1333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
