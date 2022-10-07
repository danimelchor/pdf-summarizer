import os
import webbrowser
from src.HTML import ContentLink, H, P
import src.utils as utils
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.PDFFile import PDFFile

MODEL = "facebook/bart-large-cnn"

class Summarizer:
    def __init__(self, output: str) -> None:
        # Config
        self.output = output

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)

        # Load model
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)

    def summarize_pdf(self, pdf_file: PDFFile):
        max_importance = pdf_file.get_max_importance()

        # Generate summary
        section_summaries = []
        for section, text in pdf_file.get_sections():
            summarized_text = self._summarize(text)
            section_summaries.append(
                self._gen_section(section, summarized_text, max_importance)
            )
        
        # Generate table of contents
        table_of_contents = self._generate_table_of_contents(pdf_file)

        # Generate html file
        utils.store_tokens_as_html(section_summaries, table_of_contents, pdf_file, self.output)

        # Open html file
        webbrowser.open('file://' + os.path.realpath(self.output))

    def _generate_table_of_contents(self, pdf_file: PDFFile):
        titles = pdf_file.get_titles()
        max_importance = pdf_file.get_max_importance()

        if max_importance == float('inf'):
            return
        
        # Generate table of contents
        table_of_contents = []

        # Generate table of contents
        for title in titles:
            # Current relative importance
            importance = utils.get_title_importance(title)
            importance = importance - max_importance + 1

            section_title = ContentLink(title, importance)
            table_of_contents.append(section_title)
        
        return table_of_contents

    def _gen_section(self, section: str, sentences: list, max_importance: int):
        # Get title importance 1.1 vs 1.1.1
        importance = utils.get_title_importance(section)
        importance = importance - max_importance + 1

        section_title = H(section, importance)

        # Generate section
        sentences = [s.strip() for s in sentences]
        section_text = [P(s) for s in sentences]

        return (section_title, section_text)

    
    def _summarize(self, text: str) -> list:
        """
        Summarize text

        Args:
            section (str): Section title
            text (str): Text to summarize

        Returns:
            str: Summary
        """
        batch_tokens = utils.batch_tokens(text)
        
        sentences = []
        for batch in batch_tokens:
            input_tokenized = self.tokenizer.encode(
                ' '.join(batch),
                return_tensors='pt'
            )
            summary_ids = self.model.generate(
                input_tokenized,
                length_penalty=3.0,
                min_length=10,
                max_length=70
            )
            output = [
                self.tokenizer.decode(
                    g, 
                    skip_special_tokens=True, 
                    clean_up_tokenization_spaces=False
                ) for g in summary_ids
            ]
            sentences.extend(output)
        return sentences