import re
import json

from html.parser import HTMLParser

class PayloadError(Exception):
    """ Raised when theres an error on the payload formatting """

class InfoParser(HTMLParser):
    _payload_re: re.Pattern = re.compile(r'.*?({.*})')
    _add_quotes_re: re.Pattern  = re.compile(r'(?<={|,)(.*?):')

    _is_script: bool = False
    _init_data_tag: str  = '__data__'
    _data: dict[str, str] 

    def _clear(self) -> None:
        self._is_script = False
        self._data = None

    def _parse_data(self, data: str) -> str:
        clean_data = data.replace('\n', '').replace("'", '"')

        try:
            payload = self._payload_re.match(clean_data).group(1)
            quoted_payload = self._add_quotes_re.sub(
                lambda match: f'"{match.group(1)}":',
                payload,
            )
            json_data = json.loads(quoted_payload)

            return json_data
        except AttributeError as e:
            raise PayloadError('An error occurred when parsing the initial payload') from e
        except json.decoder.JSONDecodeError as e:
            raise PayloadError(f'Unable to parse the payload as JSON: "{e}"') from e
        except KeyError as e:
            raise PayloadError(f'Unable to find expected field: "{e}"') from e

    def feed(self, data) -> None:
        self._clear()

        super().feed(data)

    def handle_starttag(self, tag: str, attrs: tuple[str]) -> None:
        if tag == 'script':
            self._is_script = True

    def handle_endtag(self, tag: str) -> None:
        if tag == 'script':
            self._is_script = False

    def handle_data(self, data: str) -> None:
        if self._is_script and data.find(self._init_data_tag) > -1:
            self._data = self._parse_data(data)

    @property
    def data(self) -> dict[str, str]:
        return self._data
