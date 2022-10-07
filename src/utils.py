import argparse
import os
from pydoc import describe
import re
from nltk import sent_tokenize

def parse_args():
    parser = argparse.ArgumentParser()

    # Input pdf file
    parser.add_argument('-i', "--input", type=str, required=True, help="Input pdf file")

    # Output file
    parser.add_argument('-o', "--output", type=str, default="summary.html", help="Output file")

    # Start page (inclusive)
    parser.add_argument('-s', "--start", type=int, default=1, help="Start page")

    # End page (inclusive)
    parser.add_argument('-e', "--end", type=int, default=1, help="End page")

    return parser.parse_args()

def batch_tokens(text: str, batch_size: int = 1024) -> list:
    """
    Batch text into tokens of size batch_size

    Args:
        text (str): Text to batch
        batch_size (int, optional): Size of each batch. Defaults to 1024.

    Returns:
        list: List of batches
    """
    batches = []
    sent = []
    length = 0
    for sentence in sent_tokenize(text):
        length += len(sentence)
        if length <= batch_size:
            sent.append(sentence)
        else:
            batches.append(sent)
            sent = [sentence]
            length = len(sentence)

    if sent:
        batches.append(sent)

    return batches

def get_title_importance(title: str) -> int:
    """
    Get title importance

    Args:
        title (str): Title

    Returns:
        int: Importance
    """
    return len(title.split(" ")[0].split("."))

def clean_text(text: str) -> str:
    """
    Clean text

    Args:
        text (str): Text

    Returns:
        str: Clean text
    """

    # Remove header and footer
    text = re.sub(r"^[^\n]+\n", "", text)
    text = re.sub(r"\n[^\n]+$", "", text)

    # Remove multiple newlines
    text = re.sub("\n{2,}", "\n", text)

    # Fix hyphenation
    text = text.replace("-\n", "")

    # Remove multiple spaces
    text = re.sub(" +", " ", text)

    text = text.strip()
    text = text.encode("utf-8", "ignore").decode('utf-8')

    return text

def process_content(text: str) -> str:
    """
    Process content that will be fed to model.

    Args:
        text (str): Text

    Returns:
        str: Processed text
    """ 
    # Remove newlines
    clean_text = text.replace("\n", " ")

    return clean_text

def parse_id(id: str) -> str:
    id = id.lower()
    id = re.sub(r"[^a-z- ]", "", id)
    id = id.strip()
    id = id.replace(" ", "-")
    return id

def store_tokens_as_html(section_summaries, table_of_contents, pdf, output_file) -> str:
    """
    Convert markdown file to html and
    save it to a file

    Args:
        file (str): Markdown file

    Returns:
        str: HTML
    """
    current_abs_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_abs_path, "..", "assets", "base.html")
    styles_path = os.path.join(current_abs_path, "..", "assets", "styles.css")
    script_path = os.path.join(current_abs_path, "..", "assets", "script.js")

    with open(base_path, "r") as f:
        base = f.read()
    
    with open(styles_path, "r") as f:
        styles = f.read()

    with open(script_path, "r") as f:
        script = f.read()

    # Generate summary
    html = ""
    for sect, summ in section_summaries:
        html += f"{sect}\n\n"
        for para in summ: 
            html += f"{para}\n\n"

    # Generate table of contents
    contents_html = ""
    for cont_link in table_of_contents:
        contents_html += f"{cont_link}\n"

    # Generate html
    output_html = base.replace("{{content}}", html).replace("{{styles}}", styles).replace("{{file_name}}", pdf.file_name).replace("{{table_of_contents}}", contents_html).replace("{{script}}", script)

    with open(output_file, "w") as f:
        f.write(output_html)

