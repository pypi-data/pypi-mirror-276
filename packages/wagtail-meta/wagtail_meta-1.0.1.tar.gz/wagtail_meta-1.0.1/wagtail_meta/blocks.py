from django import forms
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

class MetaTagBlock(blocks.StructBlock):
    """Meta tag block."""

    property_name = blocks.CharBlock(required=False)
    property_value = blocks.CharBlock(required=False)
    content = blocks.CharBlock(required=False)

    custom_html_element = blocks.CharBlock(
        required=False,
        label=_("Custom HTML Element"),
    )

    class Meta:
        template = "wagtail_meta/tags/tag.html"
        icon = "bookmark"
        label = _("Meta Tag")

    def clean(self, value):
        value = super().clean(value)
        custom_html_element = value.get("custom_html_element", "")
        if custom_html_element:
            return value
        if not value.get("property_name", ""):
            raise forms.ValidationError(_("Property name is required"))
        if not value.get("property_value", ""):
            raise forms.ValidationError(_("Property name is required"))
        return value
