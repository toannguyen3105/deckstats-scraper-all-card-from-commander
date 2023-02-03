import os.path

from scrapy.pipelines.files import FilesPipeline
import scrapy


class DeckstatsscraperPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'filename': item.get('file_name')}) for x in
                item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        url = request.url
        media_ext = os.path.splitext(url)[1]
        return 'full/%s%s' % (request.meta['filename'], media_ext)
