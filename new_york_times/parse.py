from pathlib import Path

from RPA.Excel.Files import Files

from new_york_times.data import News


class NewYorkTimesParser():
    def _generate_excel_file(self, data: list[News]):
        header = [
            "Title", "Date", "Description", "Image File Name",
            "Search Phrase Count", "Contains Monetary Value",
        ]

        excel_data = [header]

        for news in data:
            excel_data.append([
                news.title,
                news.date.strftime("%Y-%m-%d"),
                news.description,
                news.image_file_name,
                news.search_phrase_count,
                str(news.contains_monetary_value),
            ])

        lib = Files()
        output_path = Path("./output/news_data.xlsx")
        lib.create_workbook(str(output_path), fmt="xlsx",
                            sheet_name="News Data")
        lib.append_rows_to_worksheet(excel_data, name="News Data")
        lib.save_workbook()

    def parse(self, data: list[News]):
        self._generate_excel_file(data)
