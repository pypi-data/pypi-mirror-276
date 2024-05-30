import os
import sys
from typing import Optional

import markdown2
from weasyprint import CSS, HTML

DEBUG = False


def html_to_pdf(
    html_file: str, pdf_file: str, css_file: Optional[str] = None
) -> None:
    # Create an HTML object with the content and CSS styles
    with open(html_file, "r") as htmlf:
        html_content = htmlf.read()
        css_content = ""
        if css_file:
            with open(css_file, "r") as css:
                css_content = css.read()
        html = HTML(string=html_content, base_url=os.getcwd())
        css = CSS(string=css_content, base_url=os.getcwd())
        html.write_pdf(pdf_file, stylesheets=[css])


def md_to_html(md_file: str, html_file: Optional[str]) -> None:
    # Convert Markdown to HTML with the table extension enabled
    with open(md_file, "r") as mdf:
        md_content = mdf.read()
        html_content = markdown2.markdown(md_content, extras=["tables"])
        if DEBUG:
            print(html_content)
        if html_file:
            with open(html_file, "w") as html:
                html.write(html_content)


def md_to_pdf(md_file: str, pdf_file: str, css_file: Optional[str] = None):
    html_file = md_file.replace(".md", ".html")
    md_to_html(md_file, html_file)
    html_to_pdf(html_file, pdf_file, css_file)
    os.remove(html_file)


if __name__ == "__main__":
    input_file = "sample.md"
    # get os command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    html_file = input_file.replace(".md", ".html")
    pdf_file = input_file.replace(".md", ".pdf")
    # md_to_html(input_file, html_file)
    # html_to_pdf(html_file, pdf_file)
    md_to_pdf(input_file, pdf_file)
