import re

from urllib.parse import (
    urlparse,
    urljoin,
)

from requests import Session

from yazdl.handlers.parser import InfoParser

class InvalidUrlError(Exception):
    """ Raised when a given URL is of an incorrect format """

class UrlHandler:
    _DATA_INFO: dict[str, str] = {
        'share': {
            'field': 'meetingId',
            'content_url_template': '{origin}/nws/recording/1.0/play/share-info/{data_portion}',
        },
        'play': {
            'field': 'fileId',
            'content_url_template': '{origin}/nws/recording/1.0/play/info/{data_portion}',
        },
    }

    def __init__(self, session: Session, parser: InfoParser) -> None:
        self._session = session
        self._parser = parser

    def fetch_content_url(self, url: str) -> str:
        origin = self._build_origin(url)
        url_template, data_portion = self._video_data_info(url)

        return self._build_content_url(url_template, origin, data_portion)

    def origin(self, url: str) -> str:
        return self._build_origin(url)

    def _build_origin(self, url: str) -> str:
        parsed_url = urlparse(url)

        return f'{parsed_url.scheme}://{parsed_url.netloc}'

    def _url_type(self, url: str) -> str:
        try:
            match_res = re.match(r'.*zoom.us/.*/(play|share)/.*', url)
            
            return match_res.group(1)
        except AttributeError as exc:
            raise InvalidUrlError(f'Url: "{url}" is invalid.') from exc

    def _video_data_info(self, url: str) -> str:
        url_type = self._url_type(url)

        raw_data = self._session.get(url).text
        self._parser.feed(raw_data)

        content_data = self._DATA_INFO[url_type]
        url_template = content_data['content_url_template']
        field = content_data['field']

        return url_template, self._parser.data[field]

    def _build_content_url(self, url_template: str, origin: str, data_portion: str) -> str:
        return url_template.format(origin=origin, data_portion=data_portion)

    def join_path(self, url: str, path: str) -> str:
        origin = self._build_origin(url)

        return urljoin(origin, path)
