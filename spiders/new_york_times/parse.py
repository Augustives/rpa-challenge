from RPA.Excel.Files import Files

from spiders.new_york_times.data import News
from utils.parse import BaseParser


class NewYorkTimesParser(BaseParser):
    def generate_excel_file(self, data: list[News]):
        header = [
            "Title",
            "Date",
            "Description",
            "Image File Name",
            "Search Phrase Count",
            "Contains Monetary Value",
        ]

        excel_data = [header]

        for news in data:
            excel_data.append(
                [
                    news.title,
                    news.date,
                    news.description,
                    news.image_file_name,
                    news.search_phrase_count,
                    str(news.contains_monetary_value),
                ]
            )

        lib = Files()
        lib.create_workbook(
            "./output/news_data.xlsx", fmt="xlsx", sheet_name="News Data"
        )
        lib.append_rows_to_worksheet(excel_data, name="News Data")
        lib.save_workbook()

    def parse(self, data: list[News]):
        self.generate_excel_file(data)
