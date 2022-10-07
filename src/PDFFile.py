import pdfplumber
import re
import src.utils as utils


class PDFFile:
    """
    A class to represent a PDF file.
    """
    
    def __init__(self, file_name: str, start_page: int, end_page: int) -> None:
        self.file_name = file_name
        self.start_page = start_page
        self.end_page = end_page

        self.sections = []
        self.max_importance = float('inf')

        self.get_sections()

    def get_max_importance(self):
        """
        Get max importance of sections

        Returns:
            int: Max importance
        """
        return self.max_importance

    def get_titles(self):
        """
        Get titles of sections

        Returns:
            list: Titles
        """
        return [title for title, _ in self.get_sections()]

    def get_contents(self):
        """
        Get contents of sections

        Returns:
            list: Contents
        """
        return [content for _, content in self.get_sections()]

    def get_sections(self):
        """
        Extract text from pdf

        Args:
            start (int): Start page
            end (int): End page
            file (str): File path

        Returns:
            str: Text
        """

        # Dont load if already loaded
        if self.sections:
            return self.sections

        text = ""

        pages = [i for i in range(self.start_page, self.end_page + 1)]
        with pdfplumber.open(self.file_name, pages=pages) as pdf:
            text = " ".join(
                [
                    page.extract_text()
                    for page
                    in pdf.pages]
            )

        # Remove first and last lines
        text = utils.clean_text(text)

        # Split text into sections
        sections = re.split(r"(?=\n[0-9]\.[0-9])", text)
        regexp = re.compile(r"(?<=\n)[0-9]\.[0-9][^\n]+")

        res = []
        for section in sections:
            matches = regexp.search(section)
            clean = regexp.sub('', section)

            # If section has a title
            if matches:
                title = matches.group(0)

                # Clean title
                title = title.strip()
                
                # Clean text
                content = utils.process_content(clean)

                # Save section
                res.append((title, content))

                # Importance
                importance = len(title.split(" ")[0].split("."))
                self.max_importance = min(self.max_importance, importance)
                

        self.sections = res
        return res