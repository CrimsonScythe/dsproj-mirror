from scrapy.exporters import CsvItemExporter

class CsvPipeline(object):
    def __init__(self):
        self.file = open("wikinews_data_clean.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        """
        for key, value in item.items():
            is_string = (isinstance(value, basestring))
            if (is_string and ("," in value.encode('utf-8'))):
                item[key] = "\"" + value + "\""
        """
        self.exporter.export_item(item)
        return item
