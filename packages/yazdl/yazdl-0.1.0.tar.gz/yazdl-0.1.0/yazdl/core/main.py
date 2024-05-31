import sys
import requests

from argparse import Namespace

from yazdl.handlers.parser import InfoParser
from yazdl.handlers.url_handler import UrlHandler
from yazdl.handlers.data_handler import DataHandler
from yazdl.core.zoom_downloader import ZoomDownloader
from yazdl.core.headers import default_headers
from yazdl.core.options import Options


def init_downloader(args: Namespace, session: requests.Session) -> ZoomDownloader:
    parser = InfoParser()
    url_handler = UrlHandler(session, parser)
    data_handler = DataHandler(session, url_handler)

    return ZoomDownloader(args, data_handler)

def start_session(args: Namespace) -> None:
    with requests.Session() as session:
        session.headers = default_headers

        zoom_downloader = init_downloader(args, session)

        for url in args.urls:
            print(f'Downloading URL: "{url}"')
            zoom_downloader.download_data(url)

def main() -> None:
    options = Options()
    parsed_args = options.parse(sys.argv[1:])

    start_session(parsed_args)
