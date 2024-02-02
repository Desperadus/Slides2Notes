import argparse
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os


def pdf_to_markdown(pdf_filepath, output_filepath):
    with open(output_filepath, "w", encoding="utf-8") as md_file:
        for page_num, page_layout in enumerate(extract_pages(pdf_filepath)):
            md_file.write(f"\n\nNEW PAGE [{page_num + 1}]\n\n")
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    md_file.write(element.get_text())

    print(f"Markdown file generated at: {output_filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown with page labels"
    )
    parser.add_argument(
        "--pdfpath", type=str, help="Path to the PDF file", required=True
    )
    parser.add_argument(
        "--output", type=str, help="Path to output Markdown file", default="output.md"
    )
    args = parser.parse_args()

    if not os.path.exists(args.pdfpath):
        print("PDF file does not exist.")
    else:
        pdf_to_markdown(args.pdfpath, args.output)
