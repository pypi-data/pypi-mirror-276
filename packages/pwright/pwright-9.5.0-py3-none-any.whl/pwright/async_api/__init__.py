import sys

from ..typealiases import AsyncGenerator as AsyncGenerator
from ..typealiases import AsyncGeneratorContextManager as AsyncGeneratorContextManager
from ..typealiases import (
    AsyncGeneratorContextManagerAsyncGenerator as AsyncGeneratorContextManagerAsyncGenerator,
)
from ._apis import Browser as Browser
from ._apis import BrowserContext as BrowserContext
from ._apis import Dialog as Dialog
from ._apis import ElementHandle as ElementHandle
from ._apis import Error as Error
from ._apis import FrameLocator as FrameLocator
from ._apis import Locator as Locator
from ._apis import Page as Page
from ._apis import Playwright as Playwright
from ._apis import Route as Route
from ._apis import TimeoutError as TimeoutError
from ._apis import playwright as playwright
from ._briefs import pw_browser as pw_browser
from ._briefs import pw_context as pw_context
from ._briefs import pw_page as pw_page
from ._cms import playwright_browser as playwright_browser
from ._cms import playwright_context as playwright_context
from ._cms import playwright_page as playwright_page
from .utils import auto_renew as auto_renew
from .utils import renewing as renewing
from .utils import screenshot as screenshot


Eh = ElementHandle
playwright = playwright


Generator = AsyncGenerator
GeneratorContextManager = AsyncGeneratorContextManager
GeneratorContextManagerGenerator = AsyncGeneratorContextManagerAsyncGenerator


if sys.version_info < (3, 10):
    from ._compatibilities import anext as anext
