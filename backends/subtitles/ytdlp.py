import os
import yt_dlp
from vtt_to_srt.vtt_to_srt import ConvertFile

from .base import BaseSubtitlesBackend, BaseSubtitlesBackendSettings, BaseSubtitlesInputRequest, BaseSubtitlesOutputSchema
from .simplesrt import process_srt


class YtDlpSubtitlesInputRequest(BaseSubtitlesInputRequest):
    pass


class YtDlpSubtitlesOutputSchema(BaseSubtitlesOutputSchema):
    pass


class YtDlpSubtitlesSettings(BaseSubtitlesBackendSettings):
    YT_DLP__POSTPROCESSOR: str = "srt_fix:when=before_dl"
    YT_DLP__SKIP_DOWNLOAD: bool = True
    YT_DLP__WRITE_SUBTITLES: bool = True
    YT_DLP__WRITE_AUTO_SUBS: bool = True


class YtDlpSubtitlesBackend(BaseSubtitlesBackend):

    configuration_schema = YtDlpSubtitlesSettings
    output_schema = YtDlpSubtitlesOutputSchema

    params: YtDlpSubtitlesSettings

    @staticmethod
    def convert_vtt_to_srt(vtt_path: str) -> str:
        # Write vtt file to srt file and return the srt file path
        convert_file = ConvertFile(vtt_path, "utf-8")
        convert_file.convert()

    def extract_subtitles(self, request: YtDlpSubtitlesInputRequest) -> YtDlpSubtitlesOutputSchema:
        ydl_opts = {
            'writesubtitles': self.params.YT_DLP__WRITE_SUBTITLES,
            'writeautomaticsub': self.params.YT_DLP__WRITE_AUTO_SUBS,
            'subtitleslangs': [request.language],
            'skip_download': self.params.YT_DLP__SKIP_DOWNLOAD,
            'subtitleslangs': [request.language],
            'subtitlesformat': request.format,
            'convertsubtitles': 'srt',
            'outtmpl': '.temp/%(id)s.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(request.url, download=True)
        
        if request.format == 'vtt':
            # Convert vtt to srt
            self.convert_vtt_to_srt(f".temp/{info_dict['id']}.{request.language}.vtt")
        
        srt_path = f".temp/{info_dict['id']}.{request.language}.srt"
        
        # Process srt file
        subtitles = process_srt(srt_path)

        # Delete the temporary files
        try:
            os.remove(f".temp/{info_dict['id']}.{request.language}.vtt")
            os.remove(f".temp/{info_dict['id']}.{request.language}.srt")
        except:
            pass

        return YtDlpSubtitlesOutputSchema(subtitles=subtitles)
