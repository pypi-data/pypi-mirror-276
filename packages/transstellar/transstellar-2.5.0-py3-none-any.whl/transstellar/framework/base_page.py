import sys
from urllib.parse import ParseResult, urlparse

from transstellar.framework.page_decorator_meta import PageDecoratorMeta

from .element import Element


class BasePage(Element, metaclass=PageDecoratorMeta):
    XPATH_CURRENT = "//body"

    def go_to(self, url: str):
        self.driver.get(url)

        self.set_current_dom_element(None)

    def get_page(self, page_class):
        return page_class(self.app)

    def get_page_from_module(self, module, page_class):
        return getattr(sys.modules[module], page_class)(self.app)

    def get_current_url(self) -> ParseResult:
        return urlparse(self.app.driver.current_url)
