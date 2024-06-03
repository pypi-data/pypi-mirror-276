from contextlib import asynccontextmanager
import logging
from pathlib import Path
import typing as t

from .._utils import relative_to_cwd
from ..typealiases import AsyncGeneratorContextManager
from ._apis import Page


logger = logging.getLogger(__name__)


T = t.TypeVar('T')


@asynccontextmanager
async def renewing(
    p: AsyncGeneratorContextManager[T], n: int
) -> t.AsyncGenerator[t.AsyncGenerator[T, None], None]:
    yield auto_renew(p, n)


async def auto_renew(p: AsyncGeneratorContextManager[T], n: int) -> t.AsyncGenerator[T, None]:
    while True:
        async with p() as y:
            for _ in range(n):
                yield y


async def screenshot(
    page: Page,
    *,
    file=Path.cwd() / '.temp' / 'screenshot.png',
):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_bytes(await page.screenshot())
    logger.info(f' -> screenshot: ./{relative_to_cwd(file)}')
