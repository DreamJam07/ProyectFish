from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("mapa", "0002_datos_santiago")]

    operations = [
        migrations.AddField(
            model_name="comentario",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("color", "Agua de color raro"),
                    ("aceite", "Mancha de aceite"),
                    ("espuma", "Espuma o mal olor"),
                    ("peces", "Peces muertos"),
                    ("basura", "Basura"),
                    ("bien", "Todo bien"),
                ],
                default="bien",
                max_length=20,
                verbose_name="¿qué viste?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="comentario",
            name="texto",
            field=models.TextField(blank=True, max_length=500, verbose_name="¿quieres contar algo más?"),
        ),
    ]
