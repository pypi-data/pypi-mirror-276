from urllib.parse import urlparse, urljoin

import re

class Streams:
    def __init__(self, content: dict[str, str], origin: str | None) -> None:
        self._content = content
        self._origin = origin

    def _build_url(self, url: str) -> str:
        if self._origin:
            parsed = urlparse(url)

            if not parsed.netloc:
                return urljoin(self._origin, url)

        return url

    @property
    def screen(self) -> str:
        return self._build_url(self._content['shareMp4Url'])

    @property
    def speaker(self) -> str:
        return self._build_url(self._content['speakerMp4Url'])

    @property
    def subtitles(self) -> str:
        return self._build_url(self._content['ccUrl'])

    @property
    def transcription(self) -> str:
        return self._build_url(self._content['transcriptUrl'])

    def _sanitize(self, string: str) -> str:
        return re.sub(r'[^ a-zA-Z0-9_{}()-]', '_', string)

    @property
    def title(self) -> str:
        title = self._content['meet']['topic']
        clips = self._content['totalClips']
        curr_clip = self._content['currentClip']
        
        if clips > 1:
            return self._sanitize(f'{title} - Recording {curr_clip} of {clips}')

        return self._sanitize(title)
