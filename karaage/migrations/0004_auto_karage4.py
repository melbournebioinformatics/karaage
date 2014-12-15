# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import audit_log.models.fields
import jsonfield.fields
import mptt.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('karaage', '0003_unique_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('username', models.CharField(max_length=255)),
                ('foreign_id', models.CharField(help_text='The foreign identifier from the datastore.', db_index=True, null=True, max_length=255)),
                ('date_created', models.DateField()),
                ('date_deleted', models.DateField(null=True, blank=True)),
                ('disk_quota', models.IntegerField(help_text='In GB', null=True, blank=True)),
                ('shell', models.CharField(max_length=50)),
                ('login_enabled', models.BooleanField(default=True)),
                ('extra_data', jsonfield.fields.JSONField(help_text='Datastore specific values should be stored in this field.', default={})),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_account_audit_log_entry', null=True, to='karaage.Person')),
                ('default_project', models.ForeignKey(null=True, blank=True, to='karaage.Project')),
                ('machine_category', models.ForeignKey(to='karaage.MachineCategory')),
                ('person', models.ForeignKey(to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.FloatField()),
            ],
            options={
                'ordering': ['allocation_pool'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllocationAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.FloatField()),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_allocation_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllocationPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
            options={
                'ordering': ['-end', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllocationPeriodAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_allocationperiod_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllocationPool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('period', models.ForeignKey(to='karaage.AllocationPeriod')),
                ('project', models.ForeignKey(to='karaage.Project')),
            ],
            options={
                'ordering': ['-period__end', '-grant__expires', '-grant__project__end_date', 'grant__project__name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AllocationPoolAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_allocationpool_audit_log_entry', null=True, to='karaage.Person')),
                ('period', models.ForeignKey(to='karaage.AllocationPeriod')),
                ('project', models.ForeignKey(to='karaage.Project')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CareerLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('level', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['level'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CareerLevelAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('level', models.CharField(max_length=255, blank=False, null=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_careerlevel_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('begins', models.DateField()),
                ('expires', models.DateField()),
                ('project', models.ForeignKey(to='karaage.Project')),
            ],
            options={
                'ordering': ['-expires', '-project__end_date', 'project__name', 'description'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrantAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('description', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('begins', models.DateField()),
                ('expires', models.DateField()),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_grant_audit_log_entry', null=True, to='karaage.Person')),
                ('project', models.ForeignKey(to='karaage.Project')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('foreign_id', models.CharField(help_text='The foreign identifier from the datastore.', db_index=True, null=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('extra_data', jsonfield.fields.JSONField(help_text='Datastore specific values should be stored in this field.', default={})),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_group_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstituteAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('saml_entityid', models.CharField(db_index=True, null=True, blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_institute_audit_log_entry', null=True, to='karaage.Person')),
                ('group', models.OneToOneField(to='karaage.Group')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstituteDelegateAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('send_email', models.BooleanField()),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_institutedelegate_audit_log_entry', null=True, to='karaage.Person')),
                ('institute', models.ForeignKey(to='karaage.Institute')),
                ('person', models.ForeignKey(to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstituteQuotaAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('quota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cap', models.IntegerField(null=True, blank=True)),
                ('disk_quota', models.IntegerField(null=True, blank=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_institutequota_audit_log_entry', null=True, to='karaage.Person')),
                ('institute', models.ForeignKey(to='karaage.Institute')),
                ('machine_category', models.ForeignKey(to='karaage.MachineCategory')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineCategoryAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('datastore', models.CharField(help_text='Modifying this value on existing categories will affect accounts created under the old datastore', max_length=255, choices=[('dummy', 'dummy')])),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_machinecategory_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('username', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(db_index=True, null=True, max_length=75)),
                ('short_name', models.CharField(max_length=30)),
                ('full_name', models.CharField(max_length=60)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('saml_id', models.CharField(editable=False, db_index=True, null=True, blank=True, max_length=200)),
                ('position', models.CharField(null=True, blank=True, max_length=200)),
                ('telephone', models.CharField(null=True, blank=True, max_length=200)),
                ('mobile', models.CharField(null=True, blank=True, max_length=200)),
                ('department', models.CharField(null=True, blank=True, max_length=200)),
                ('supervisor', models.CharField(null=True, blank=True, max_length=100)),
                ('title', models.CharField(null=True, blank=True, max_length=10, choices=[('', ''), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Ms', 'Ms'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('A/Prof', 'A/Prof')])),
                ('address', models.CharField(null=True, blank=True, max_length=200)),
                ('city', models.CharField(null=True, blank=True, max_length=100)),
                ('postcode', models.CharField(null=True, blank=True, max_length=8)),
                ('state', models.CharField(null=True, blank=True, max_length=4, choices=[('', '--------'), ('ACT', 'ACT'), ('NSW', 'New South Wales'), ('NT', 'Northern Territory'), ('QLD', 'Queensland'), ('SA', 'South Australia'), ('TAS', 'Tasmania'), ('VIC', 'Victoria'), ('WA', 'Western Australia')])),
                ('country', models.CharField(null=True, blank=True, max_length=2, choices=[('AU', 'Australia'), ('NZ', 'New Zealand'), ('GB', 'United Kingdom'), ('DE', 'Germany'), ('US', 'United States'), ('', '--------------------------------------'), ('AD', 'Andorra'), ('AE', 'United Arab Emirates'), ('AF', 'Afghanistan'), ('AG', 'Antigua and Barbuda'), ('AI', 'Anguilla'), ('AL', 'Albania'), ('AM', 'Armenia'), ('AN', 'Netherlands Antilles'), ('AO', 'Angola'), ('AQ', 'Antarctica'), ('AR', 'Argentina'), ('AS', 'American Samoa'), ('AT', 'Austria'), ('AW', 'Aruba'), ('AX', 'Aland Islands'), ('AZ', 'Azerbaijan'), ('BA', 'Bosnia and Herzegovina'), ('BB', 'Barbados'), ('BD', 'Bangladesh'), ('BE', 'Belgium'), ('BF', 'Burkina Faso'), ('BG', 'Bulgaria'), ('BH', 'Bahrain'), ('BI', 'Burundi'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BN', 'Brunei Darussalam'), ('BO', 'Bolivia'), ('BR', 'Brazil'), ('BS', 'Bahamas'), ('BT', 'Bhutan'), ('BV', 'Bouvet Island'), ('BW', 'Botswana'), ('BY', 'Belarus'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CC', 'Cocos (Keeling) Islands'), ('CD', 'Congo'), ('CF', 'Central African Republic'), ('CG', 'Congo'), ('CH', 'Switzerland'), ('CI', "Cote d'Ivoire"), ('CK', 'Cook Islands'), ('CL', 'Chile'), ('CM', 'Cameroon'), ('CN', 'China'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('CU', 'Cuba'), ('CV', 'Cape Verde'), ('CX', 'Christmas Island'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DJ', 'Djibouti'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('DZ', 'Algeria'), ('EC', 'Ecuador'), ('EE', 'Estonia'), ('EG', 'Egypt'), ('EH', 'Western Sahara'), ('ER', 'Eritrea'), ('ES', 'Spain'), ('ET', 'Ethiopia'), ('FI', 'Finland'), ('FJ', 'Fiji'), ('FK', 'Falkland Islands'), ('FM', 'Micronesia'), ('FO', 'Faroe Islands'), ('FR', 'France'), ('GA', 'Gabon'), ('GD', 'Grenada'), ('GE', 'Georgia'), ('GF', 'French Guiana'), ('GG', 'Guernsey'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GL', 'Greenland'), ('GM', 'Gambia'), ('GN', 'Guinea'), ('GP', 'Guadeloupe'), ('GQ', 'Equatorial Guinea'), ('GR', 'Greece'), ('GS', 'South Georgia and the South Sandwich Islands'), ('GT', 'Guatemala'), ('GU', 'Guam'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HK', 'Hong Kong'), ('HM', 'Heard Island and McDonald Islands'), ('HN', 'Honduras'), ('HR', 'Croatia'), ('HT', 'Haiti'), ('HU', 'Hungary'), ('ID', 'Indonesia'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IM', 'Isle of Man'), ('IN', 'India'), ('IO', 'British Indian Ocean Territory'), ('IQ', 'Iraq'), ('IR', 'Iran'), ('IS', 'Iceland'), ('IT', 'Italy'), ('JE', 'Jersey'), ('JM', 'Jamaica'), ('JO', 'Jordan'), ('JP', 'Japan'), ('KE', 'Kenya'), ('KG', 'Kyrgyzstan'), ('KH', 'Cambodia'), ('KI', 'Kiribati'), ('KM', 'Comoros'), ('KN', 'Saint Kitts and Nevis'), ('KP', 'Korea'), ('KR', 'Korea'), ('KW', 'Kuwait'), ('KY', 'Cayman Islands'), ('KZ', 'Kazakhstan'), ('LA', "Lao People's Democratic Republic"), ('LB', 'Lebanon'), ('LC', 'Saint Lucia'), ('LI', 'Liechtenstein'), ('LK', 'Sri Lanka'), ('LR', 'Liberia'), ('LS', 'Lesotho'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('LV', 'Latvia'), ('LY', 'Libyan Arab Jamahiriya'), ('MA', 'Morocco'), ('MC', 'Monaco'), ('MD', 'Moldova'), ('ME', 'Montenegro'), ('MG', 'Madagascar'), ('MH', 'Marshall Islands'), ('MK', 'Macedonia'), ('ML', 'Mali'), ('MM', 'Myanmar'), ('MN', 'Mongolia'), ('MO', 'Macao'), ('MP', 'Northern Mariana Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MS', 'Montserrat'), ('MT', 'Malta'), ('MU', 'Mauritius'), ('MV', 'Maldives'), ('MW', 'Malawi'), ('MX', 'Mexico'), ('MY', 'Malaysia'), ('MZ', 'Mozambique'), ('NA', 'Namibia'), ('NC', 'New Caledonia'), ('NE', 'Niger'), ('NF', 'Norfolk Island'), ('NG', 'Nigeria'), ('NI', 'Nicaragua'), ('NL', 'Netherlands'), ('NO', 'Norway'), ('NP', 'Nepal'), ('NR', 'Nauru'), ('NU', 'Niue'), ('OM', 'Oman'), ('PA', 'Panama'), ('PE', 'Peru'), ('PF', 'French Polynesia'), ('PG', 'Papua New Guinea'), ('PH', 'Philippines'), ('PK', 'Pakistan'), ('PL', 'Poland'), ('PM', 'Saint Pierre and Miquelon'), ('PN', 'Pitcairn'), ('PR', 'Puerto Rico'), ('PS', 'Palestinian Territory'), ('PT', 'Portugal'), ('PW', 'Palau'), ('PY', 'Paraguay'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RS', 'Serbia'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('SA', 'Saudi Arabia'), ('SB', 'Solomon Islands'), ('SC', 'Seychelles'), ('SD', 'Sudan'), ('SE', 'Sweden'), ('SG', 'Singapore'), ('SH', 'Saint Helena'), ('SI', 'Slovenia'), ('SJ', 'Svalbard and Jan Mayen'), ('SK', 'Slovakia'), ('SL', 'Sierra Leone'), ('SM', 'San Marino'), ('SN', 'Senegal'), ('SO', 'Somalia'), ('SR', 'Suriname'), ('ST', 'Sao Tome and Principe'), ('SV', 'El Salvador'), ('SY', 'Syrian Arab Republic'), ('SZ', 'Swaziland'), ('TC', 'Turks and Caicos Islands'), ('TD', 'Chad'), ('TF', 'French Southern Territories'), ('TG', 'Togo'), ('TH', 'Thailand'), ('TJ', 'Tajikistan'), ('TK', 'Tokelau'), ('TL', 'Timor-Leste'), ('TM', 'Turkmenistan'), ('TN', 'Tunisia'), ('TO', 'Tonga'), ('TR', 'Turkey'), ('TT', 'Trinidad and Tobago'), ('TV', 'Tuvalu'), ('TW', 'Taiwan'), ('TZ', 'Tanzania'), ('UA', 'Ukraine'), ('UG', 'Uganda'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VA', 'Vatican City'), ('VC', 'Saint Vincent and the Grenadines'), ('VE', 'Venezuela'), ('VG', 'Virgin Islands (British)'), ('VI', 'Virgin Islands (US)'), ('VN', 'Viet Nam'), ('VU', 'Vanuatu'), ('WF', 'Wallis and Futuna'), ('WS', 'Samoa'), ('YE', 'Yemen'), ('YT', 'Mayotte'), ('ZA', 'South Africa'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')])),
                ('website', models.URLField(null=True, blank=True)),
                ('fax', models.CharField(null=True, blank=True, max_length=50)),
                ('comment', models.TextField(null=True, blank=True)),
                ('date_approved', models.DateField(null=True, blank=True)),
                ('date_deleted', models.DateField(null=True, blank=True)),
                ('last_usage', models.DateField(null=True, blank=True)),
                ('expires', models.DateField(null=True, blank=True)),
                ('is_systemuser', models.BooleanField(default=False)),
                ('login_enabled', models.BooleanField(default=True)),
                ('legacy_ldap_password', models.CharField(null=True, blank=True, max_length=128)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_person_audit_log_entry', null=True, to='karaage.PersonAuditLogEntry')),
                ('approved_by', models.ForeignKey(null=True, blank=True, related_name='_auditlog_user_approver', to='karaage.Person')),
                ('career_level', models.ForeignKey(null=True, blank=False, to='karaage.CareerLevel')),
                ('deleted_by', models.ForeignKey(null=True, blank=True, related_name='_auditlog_user_deletor', to='karaage.Person')),
                ('institute', models.ForeignKey(to='karaage.Institute')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('allocation_mode', models.CharField(default='private', max_length=20, choices=[('private', 'Private (this project only)'), ('shared', 'Shared (this project and all sub-projects)')])),
                ('pid', models.CharField(db_index=True, max_length=255)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('start_date', models.DateField(default=datetime.datetime.today)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('additional_req', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('date_approved', models.DateField(editable=False, null=True, blank=True)),
                ('date_deleted', models.DateField(editable=False, null=True, blank=True)),
                ('last_usage', models.DateField(editable=False, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_project_audit_log_entry', null=True, to='karaage.Person')),
                ('approved_by', models.ForeignKey(editable=False, blank=True, related_name='_auditlog_project_approver', null=True, to='karaage.Person')),
                ('deleted_by', models.ForeignKey(editable=False, blank=True, related_name='_auditlog_project_deletor', null=True, to='karaage.Person')),
                ('group', models.OneToOneField(to='karaage.Group')),
                ('institute', models.ForeignKey(to='karaage.Institute')),
                ('parent', mptt.fields.TreeForeignKey(null=True, blank=True, related_name='_auditlog_children', to='karaage.Project')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('level', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['level'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectLevelAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('level', models.CharField(max_length=255)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_projectlevel_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('is_project_supervisor', models.BooleanField(default=False)),
                ('is_project_leader', models.BooleanField(default=False)),
                ('is_default_project', models.BooleanField(default=False)),
                ('is_primary_contact', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='karaage.Person')),
                ('project', models.ForeignKey(to='karaage.Project')),
                ('project_level', models.ForeignKey(to='karaage.ProjectLevel', null=True, blank=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectQuotaAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('cap', models.IntegerField(null=True, blank=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_projectquota_audit_log_entry', null=True, to='karaage.Person')),
                ('machine_category', models.ForeignKey(to='karaage.MachineCategory')),
                ('project', models.ForeignKey(to='karaage.Project')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicNotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('note', models.TextField()),
                ('when', models.DateTimeField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('person', models.ForeignKey(to='karaage.Person')),
            ],
            options={
                'ordering': ['-when'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('scaling_factor', models.FloatField()),
                ('resource_type', models.CharField(max_length=255, choices=[('slurm_cpu', 'Slurm (CPU)'), ('slurm_mem', 'Slurm (MEM)'), ('gpfs', 'GPFS')])),
                ('quantity', models.BigIntegerField()),
                ('machine', models.ForeignKey(to='karaage.Machine')),
            ],
            options={
                'ordering': ['resource_type'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('scaling_factor', models.FloatField()),
                ('resource_type', models.CharField(max_length=255, choices=[('slurm_cpu', 'Slurm (CPU)'), ('slurm_mem', 'Slurm (MEM)'), ('gpfs', 'GPFS')])),
                ('quantity', models.BigIntegerField()),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_resource_audit_log_entry', null=True, to='karaage.Person')),
                ('machine', models.ForeignKey(to='karaage.Machine')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourcePool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourcePoolAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_resourcepool_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('opened', models.DateField()),
                ('closed', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchemeAuditLogEntry',
            fields=[
                ('id', models.IntegerField(db_index=True, verbose_name='ID', blank=True, auto_created=True)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('opened', models.DateField()),
                ('closed', models.DateField(null=True, blank=True)),
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action_date', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('action_type', models.CharField(editable=False, max_length=1, choices=[('I', 'Created'), ('U', 'Changed'), ('D', 'Deleted')])),
                ('action_user', audit_log.models.fields.LastUserField(editable=False, related_name='_scheme_audit_log_entry', null=True, to='karaage.Person')),
            ],
            options={
                'ordering': ('-action_date',),
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('count', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=255)),
                ('range_start', models.DateTimeField()),
                ('range_end', models.DateTimeField()),
                ('raw_used', models.FloatField()),
                ('used', models.FloatField()),
                ('account', models.ForeignKey(to='karaage.Account')),
                ('allocated_project', models.ForeignKey(null=True, related_name='allocated_usage', to='karaage.Project')),
                ('allocation_period', models.ForeignKey(null=True, to='karaage.AllocationPeriod')),
                ('allocation_pool', models.ForeignKey(null=True, to='karaage.AllocationPool')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('grant', models.ForeignKey(null=True, to='karaage.Grant')),
                ('machine', models.ForeignKey(to='karaage.Machine')),
                ('person', models.ForeignKey(null=True, to='karaage.Person')),
                ('person_career_level', models.ForeignKey(to='karaage.CareerLevel', null=True, blank=True)),
                ('person_institute', models.ForeignKey(null=True, related_name='person_institute', to='karaage.Institute')),
                ('person_project_level', models.ForeignKey(to='karaage.ProjectLevel', null=True, blank=True)),
                ('project_institute', models.ForeignKey(related_name='project_institute', to='karaage.Institute')),
                ('resource', models.ForeignKey(to='karaage.Resource')),
                ('resource_pool', models.ForeignKey(null=True, to='karaage.ResourcePool')),
                ('scheme', models.ForeignKey(null=True, to='karaage.Scheme')),
                ('submitted_project', models.ForeignKey(related_name='submitted_usage', to='karaage.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resourceauditlogentry',
            name='resource_pool',
            field=models.ForeignKey(to='karaage.ResourcePool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='resource_pool',
            field=models.ForeignKey(to='karaage.ResourcePool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grantauditlogentry',
            name='scheme',
            field=models.ForeignKey(to='karaage.Scheme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grant',
            name='scheme',
            field=models.ForeignKey(to='karaage.Scheme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allocationpoolauditlogentry',
            name='resource_pool',
            field=models.ForeignKey(to='karaage.ResourcePool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allocationpool',
            name='resource_pool',
            field=models.ForeignKey(to='karaage.ResourcePool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allocationauditlogentry',
            name='allocation_pool',
            field=models.ForeignKey(to='karaage.AllocationPool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allocationauditlogentry',
            name='grant',
            field=models.ForeignKey(to='karaage.Grant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allocation',
            name='allocation_pool',
            field=models.ForeignKey(to='karaage.AllocationPool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='allocation',
            name='grant',
            field=models.ForeignKey(to='karaage.Grant'),
            preserve_default=True,
        ),
        migrations.RunSQL(
            '''
                INSERT INTO karaage_projectmembership (
                    person_id,
                    project_id,
                    is_project_supervisor,
                    is_project_leader,
                    is_default_project,
                    is_primary_contact
                ) SELECT
                    members.person_id,
                    project.id,
                    0::bool,
                    leaders.id IS NOT NULL,
                    members.person_id IN (
                        SELECT person_id
                        FROM account
                        WHERE default_project_id = project.id
                    ),
                    0::bool
                    FROM people_group_members members
                        INNER JOIN people_group grp ON (
                            members.group_id = grp.id
                        )
                        INNER JOIN project ON (
                            project.pid = grp.name
                        )
                        LEFT JOIN project_leaders leaders ON (
                            leaders.project_id = project.id
                        )
            ''',
            '''
                UPDATE account SET default_project_id = (
                    SELECT membership.project_id
                    FROM karaage_projectmembership membership
                    WHERE membership.is_default_project
                    AND account.person_id = membership.person_id
                );

                INSERT INTO project_leaders (
                    project_id,
                    person_id
                ) SELECT project_id, person_id
                FROM karaage_projectmembership
                WHERE is_project_leader
                ORDER BY id;
            ''',
        ),
        migrations.RemoveField(
            model_name='project',
            name='leaders',
        ),
        migrations.AddField(
            model_name='person',
            name='career_level',
            field=models.ForeignKey(null=True, blank=False, to='karaage.CareerLevel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='allocation_mode',
            field=models.CharField(default='private', max_length=20, choices=[('private', 'Private (this project only)'), ('shared', 'Shared (this project and all sub-projects)')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='level',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='lft',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='parent',
            field=mptt.fields.TreeForeignKey(null=True, blank=True, related_name='children', to='karaage.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='rght',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='tree_id',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='institute',
            name='group',
            field=models.OneToOneField(to='karaage.Group'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='machinecategory',
            name='datastore',
            field=models.CharField(help_text='Modifying this value on existing categories will affect accounts created under the old datastore', max_length=255, choices=[('dummy', 'dummy')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='group',
            field=models.OneToOneField(to='karaage.Group'),
            preserve_default=True,
        ),
    ]
