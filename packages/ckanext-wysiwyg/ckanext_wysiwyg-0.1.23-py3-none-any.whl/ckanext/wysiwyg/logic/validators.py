import ckanext.wysiwyg.utils as wysiwyg_utils


def wysiwyg_sanitize_html(html: str) -> str:
    return wysiwyg_utils.sanitize_html(html)
