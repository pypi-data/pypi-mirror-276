from lxml.html.clean import Cleaner
from lxml.etree import ParseError


def sanitize_html(html: str) -> str:
    if not html:
        return ""

    try:
        result = Cleaner(
            page_structure=True,
            meta=False,
            embedded=False,
            links=False,
            style=False,
            processing_instructions=True,
            inline_style=False,
            scripts=False,
            javascript=True,
            comments=True,
            frames=False,
            forms=False,
            annoying_tags=True,
            remove_unknown_tags=True,
            safe_attrs_only=False,
        ).clean_html(html)
    except ParseError:
        return ""

    return result
