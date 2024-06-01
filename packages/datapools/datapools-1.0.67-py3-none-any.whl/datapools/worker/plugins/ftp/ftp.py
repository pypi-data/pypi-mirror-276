import io
import asyncio
import traceback
from ftplib import FTP

from typing import Union, List, Optional

# import httpx
from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywriteTimeoutError
from playwright.async_api import async_playwright

from ....common.logger import logger

# from ....common.storage import BaseStorage
from ....common.types import CrawlerBackTask, CrawlerContent, CrawlerDemoUser, DatapoolContentType
from ...utils import canonicalize_url
from ..base_plugin import BasePlugin, BaseTag, BasePluginException, BaseReader
from ...worker import WorkerTask
from .ftp_dir_listing import DirectoryListing


class FTPReader(BaseReader):
    ftp: FTP
    filepath: str

    def __init__(self, ftp: FTP, filepath):
        super().__init__()
        self.ftp = ftp
        self.filepath = filepath

    def read_to(self, f: io.IOBase):
        cmd = f"RETR {self.filepath}"
        self.ftp.retrbinary(cmd, callback=f.write)


class FTPPlugin(BasePlugin):
    host: str
    user: str
    passwd: str
    ftp: FTP
    copyright_tags: List[BaseTag]

    def __init__(self, ctx, host="", user="anonymous", passwd="", demo_tag: Optional[str] = None):
        super().__init__(ctx)
        self.host = host
        self.user = user
        self.passwd = passwd
        self.copyright_tags = []
        if demo_tag:
            self.copyright_tags.append(BaseTag(demo_tag))

    @staticmethod
    def is_supported(url):
        p = BasePlugin.parse_url(url)
        return p.scheme == "ftp"

    async def process(self, task: WorkerTask):
        self.ftp = FTP(self.host, self.user, self.passwd)
        pwd = self.ftp.pwd()
        async for x in self._scan_dir(pwd, 0):
            yield x
        del self.ftp

    async def _scan_dir(self, path, rec):
        # logger.info(f"scanning {path}")
        lister = DirectoryListing()
        self.ftp.dir(path, lister)

        local_copyright_tag = await self._try_find_license(path, lister.contents)
        if len(self.copyright_tags) == 0:
            logger.info(f"no copyright tag in {path}")
            return
        copyright_tag = self.copyright_tags[-1]

        # copyright_tag is pushed to self.copyright_tags

        for item in lister.contents:
            logger.info("\t" * rec + item["permissions"] + "\t" + item["filename"] + "\t" + item["d"])
            if DirectoryListing.is_dir(item["permissions"]):
                sub_path = path + item["filename"] + "/"
                async for x in self._scan_dir(sub_path, rec + 1):
                    yield x
            else:
                if item["filename"] == BasePlugin.license_filename:
                    continue

                filepath = f'{path}{item["filename"]}'
                # content = await self.download(filepath)
                # if content:
                #     tag = None
                #     try:
                #         content_type = BasePlugin.get_content_type_by_content(content)
                #         if content_type == DatapoolContentType.Image:
                #             tag = BasePlugin.parse_image_tag(content)

                yield CrawlerContent(
                    # tag_id=str(tag) if tag is not None else None,
                    # tag_keepout=tag.is_keepout() if tag is not None else None,
                    copyright_tag_id=str(copyright_tag),
                    copyright_tag_keepout=copyright_tag.is_keepout(),
                    # type=content_type,
                    url=filepath,
                    # content=content,
                    content=FTPReader(self.ftp, filepath),
                )
                # except BasePluginException:
                #     print(traceback.format_exc())
                #     continue
        if local_copyright_tag:
            self.copyright_tags.pop()

    async def _try_find_license(self, path, dir_contents) -> Optional[BaseTag]:
        for item in dir_contents:
            if item["filename"] == BasePlugin.license_filename and not DirectoryListing.is_dir(item["permissions"]):
                logger.info("found license.txt")
                content = await self.download(f'{path}{item["filename"]}')
                if content:
                    logger.info(f"got license content: {content=}")
                    tag = await BasePlugin.parse_tag_in(content.decode())
                    # logger.info(f"{tag_id=}")
                    logger.info(f"{tag=}")
                    if tag:
                        self.copyright_tags.append(tag)
                        return tag
        return None

    async def download(self, path):
        res = b""

        def gather_content(batch):
            nonlocal res
            res += batch

        cmd = f"retr {path}"
        # print(cmd)
        try:
            self.ftp.retrbinary(cmd, gather_content)
            # print(content)
            return res
        except Exception:
            logger.error(f"failed retr {path}")
        return None
