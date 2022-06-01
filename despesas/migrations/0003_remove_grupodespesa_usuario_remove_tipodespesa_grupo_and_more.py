# Generated by Django 4.0.4 on 2022-05-24 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
        ('despesas', '0002_rename_status_formapagamento_ativo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupodespesa',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='tipodespesa',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='tipodespesa',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='despesa',
            name='fpag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.formapagamento'),
        ),
        migrations.AlterField(
            model_name='despesa',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cadastros.tipodespesa'),
        ),
        migrations.DeleteModel(
            name='FormaPagamento',
        ),
        migrations.DeleteModel(
            name='GrupoDespesa',
        ),
        migrations.DeleteModel(
            name='TipoDespesa',
        ),
    ]