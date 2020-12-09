from django.contrib import admin
from email_client.models import Email

# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = (
        'ein',
        'status',
        'from_email',
        'to_email',
        'subject',
        'created',
        'status_code'
    )


admin.site.register(Email, EmailAdmin)
