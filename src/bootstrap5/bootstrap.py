from importlib import import_module

from django.conf import settings
from django.templatetags.static import static

BOOTSTRAP5_VERSION = '5.3.0-alpha3-dist'
BOOTSTRAP_STATIC_PREFIX = "bootstrap5/bootstrap-" + BOOTSTRAP5_VERSION + "/"
BOOTSTRAP5_DEFAULTS = {
    "css_url": {
        "href": static(BOOTSTRAP_STATIC_PREFIX + "css/bootstrap.css"),
    },
    "javascript_url": {
        "url": static(BOOTSTRAP_STATIC_PREFIX + "js/bootstrap.bundle.min.js"),
    },
    "theme_url": None,
    "javascript_in_head": False,
    "use_i18n": False,
    "horizontal_label_class": "col-md-3",
    "horizontal_field_class": "col-md-9",
    "set_placeholder": True,
    "required_css_class": "",
    "error_css_class": "is-invalid",
    "success_css_class": "is-valid",
    "formset_renderers": {"default": "bootstrap5.renderers.FormsetRenderer"},
    "form_renderers": {"default": "bootstrap5.renderers.FormRenderer"},
    "field_renderers": {
        "default": "bootstrap5.renderers.FieldRenderer",
        "inline": "bootstrap5.renderers.InlineFieldRenderer",
        "horizontal": "bootstrap5.renderers.HorizontalFieldRenderer",
    },
}


def get_bootstrap_setting(name, default=None):
    """Read a setting."""
    # Start with a copy of default settings
    BOOTSTRAP5 = BOOTSTRAP5_DEFAULTS.copy()

    # Override with user settings from settings.py
    BOOTSTRAP5.update(getattr(settings, "BOOTSTRAP5", {}))

    # Update use_i18n
    BOOTSTRAP5["use_i18n"] = i18n_enabled()

    return BOOTSTRAP5.get(name, default)


def javascript_url():
    """Return the full url to the Bootstrap JavaScript file."""
    return get_bootstrap_setting("javascript_url")


def css_url():
    """Return the full url to the Bootstrap CSS file."""
    return get_bootstrap_setting("css_url")


def theme_url():
    """Return the full url to the theme CSS file."""
    return get_bootstrap_setting("theme_url")


def i18n_enabled():
    """Return the projects i18n setting."""
    return getattr(settings, "USE_I18N", False)


def get_renderer(renderers, **kwargs):
    layout = kwargs.get("layout", "")
    path = renderers.get(layout, renderers["default"])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting("formset_renderers")
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting("form_renderers")
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting("field_renderers")
    return get_renderer(renderers, **kwargs)
