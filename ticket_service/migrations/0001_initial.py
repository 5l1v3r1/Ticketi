# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 05:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROGRESSING', 'Progressing'), ('SOLVED', 'Solved'), ('CLOSED', 'Closed')], max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('creation_time', models.DateField(auto_now_add=True)),
                ('being_unknown', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Department')),
            ],
        ),
        migrations.CreateModel(
            name='edit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('new_body', models.TextField()),
                ('new_title', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('Comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrivateTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('addressed_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=100)),
                ('picture_path', models.CharField(max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('reffered_to', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reopen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SetConfirmationLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True)),
                ('limit_value', models.IntegerField(default=0)),
                ('need_to_confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('body', models.TextField()),
                ('summary_len', models.IntegerField(default=0)),
                ('priority', models.CharField(choices=[('LOW', 'Low'), ('NORMAL', 'Normal'), ('IMPORTANT', 'Important')], default='NORMAL', max_length=15)),
                ('is_public', models.BooleanField(default=True)),
                ('being_unknown', models.BooleanField(default=False)),
                ('creation_time', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROGRESSING', 'Progressing'), ('SOLVED', 'Solved'), ('CLOSED', 'Closed')], default='PENDING', max_length=15)),
                ('need_to_confirmed', models.BooleanField(default=False)),
                ('minimum_approvers_count', models.IntegerField(default=0)),
                ('addressed_users', models.ManyToManyField(related_name='ticket_M2M_addressed_users', to=settings.AUTH_USER_MODEL)),
                ('cc_users', models.ManyToManyField(blank=True, related_name='ticket_M2M_cc_users', to=settings.AUTH_USER_MODEL)),
                ('contributers', models.ManyToManyField(related_name='ticket_M2M_contributers', to=settings.AUTH_USER_MODEL)),
                ('in_list_contributers', models.ManyToManyField(blank=True, related_name='ticket_M2M_in_list_contributers', to=settings.AUTH_USER_MODEL)),
                ('known_approvers', models.ManyToManyField(blank=True, related_name='ticket_M2M_known_approvers', to=settings.AUTH_USER_MODEL)),
                ('known_denials', models.ManyToManyField(blank=True, related_name='ticket_M2M_known_denials', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Ticket')),
                ('tag_list', models.ManyToManyField(blank=True, to='ticket_service.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('department', models.ManyToManyField(to='ticket_service.Department')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Type'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='unknown_approvers',
            field=models.ManyToManyField(blank=True, related_name='ticket_M2M_unknown_approvers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='unknown_denials',
            field=models.ManyToManyField(blank=True, related_name='ticket_M2M_unknown_denials', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='setconfirmationlimit',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_setconfirmationlimit_activity_ticket_related', related_query_name='ticket_service_setconfirmationlimit_activity_ticket_relateds', to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='setconfirmationlimit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_setconfirmationlimit_activity_user_related', related_query_name='ticket_service_setconfirmationlimit_activity_user_relateds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reopen',
            name='new_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='reopen',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_reopen_activity_ticket_related', related_query_name='ticket_service_reopen_activity_ticket_relateds', to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='reopen',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_reopen_activity_user_related', related_query_name='ticket_service_reopen_activity_user_relateds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='referral',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_referral_activity_ticket_related', related_query_name='ticket_service_referral_activity_ticket_relateds', to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='referral',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_referral_activity_user_related', related_query_name='ticket_service_referral_activity_user_relateds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publicattachment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='privateticket',
            name='parent_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='privateattachment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.PrivateTicket'),
        ),
        migrations.AddField(
            model_name='edit',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_edit_activity_ticket_related', related_query_name='ticket_service_edit_activity_ticket_relateds', to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='edit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_edit_activity_user_related', related_query_name='ticket_service_edit_activity_user_relateds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='changestatus',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_changestatus_activity_ticket_related', related_query_name='ticket_service_changestatus_activity_ticket_relateds', to='ticket_service.Ticket'),
        ),
        migrations.AddField(
            model_name='changestatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_service_changestatus_activity_user_related', related_query_name='ticket_service_changestatus_activity_user_relateds', to=settings.AUTH_USER_MODEL),
        ),
    ]
