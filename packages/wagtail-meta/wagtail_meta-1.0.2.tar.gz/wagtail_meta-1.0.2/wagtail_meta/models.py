from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.registry import register_setting
from wagtail.contrib.settings.models import (
    BaseSiteSetting,
)

from .blocks import MetaTagBlock


@register_setting
class MetaTags(BaseSiteSetting):

    tags = StreamField([
        ("meta", MetaTagBlock()),
    ], blank=True, null=True, verbose_name=_("Meta Tags"), use_json_field=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("tags"),
        ], heading=_("Meta Tags"), help_text=mark_safe(_(
            "<pre>Meta tags to be included in the <head> of the page.\n"
            "This can be used to add custom meta tags, such as OpenGraph tags.\n"
            "Note: These tags are not validated, so be careful!\n"
            "You can try to use context variables by enclosing them in '{{ }}'\n"
            "The entire context for the rendered page is passed to the 'Custom HTML Element' or 'Property Content'</pre>"
            "<a href=\"https://ogp.me/\" target=\"_blank\">OpenGraph Meta Tags</a> "
            "<a href=\"https://www.w3schools.com/tags/tag_meta.asp\" target=\"_blank\">W3 Meta Tags</a>"
        ))),
    ]

    class Meta:
        verbose_name = _("Meta Tags")
        verbose_name_plural = _("Meta Tags")