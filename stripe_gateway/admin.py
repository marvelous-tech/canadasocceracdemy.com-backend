from django.contrib import admin
from stripe_gateway.models import Webhook, WebhookError
import json
from pygments import highlight
from pygments import lexers
from pygments import formatters


from django.utils.safestring import mark_safe

# Register your models here.


@admin.register(Webhook)
class WebhookModelAdmin(admin.ModelAdmin):
    list_display = [
        'event_type',
        'event_id',
        'is_succeed',
        'object_id',
        'customer_id',
        'created',
        'updated'
    ]
    exclude = ['body', ]
    readonly_fields = ['body_pretty', ]

    def body_pretty(self, instance):
        """Function to display pretty version of our data"""

        # Get the Pygments formatter
        formatter = formatters.HtmlFormatter(linenos='table', style='colorful')

        # Highlight the data
        response = highlight(instance.body, lexers.JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        print(style)
        print(response)
        # Safe the output
        return mark_safe(style + response)


@admin.register(WebhookError)
class WebhookErrorModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'created',
        'updated'
    ]

