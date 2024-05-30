from django.template import library
from django.template.loader import render_to_string
from wagtail.contrib.settings.context_processors import (
    SettingProxy,
    SettingModuleProxy,
)
from wagtail_meta.models import (
    MetaTags,
)

register = library.Library()

@register.simple_tag(takes_context=True, name="metatags")
def meta_tags(context, tags=None):
    template = 'wagtail_meta/tags/meta.html'

    if tags is None:
        settings_proxy: SettingProxy = context.get("settings")
        if settings_proxy is None or not isinstance(settings_proxy, SettingProxy):
            raise Exception("settings not found in context")
        
        module = settings_proxy.get("wagtail_meta")
        if module is None or not isinstance(module, SettingModuleProxy):
            raise Exception("wagtail_meta not found in settings")
        
        meta: MetaTags = module.get("metatags")
        if meta is None:
            raise Exception("metatags not found in wagtail_meta settings")
        
        tags = meta.tags

    if not tags:
        return ""
    
    return render_to_string(template, {
        'tags': tags,
        'tag_context': context
    })
