import argparse
import os
import textwrap
import time

from tqdm import tqdm

# Assuming the use of a hypothetical `genai` library similar to the one mentioned
import google.generativeai as genai

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os
from typing import List

VERBOSE = False

def pdf_to_markdown(pdf_filepath: str, output_filepath: str) -> str:
    """
    Converts a PDF file to Markdown format.

    Args:
        pdf_filepath (str): Path to the PDF file.
        output_filepath (str): Path to the output Markdown file.

    Returns:
        str: Path to the raw output Markdown file.
    """
    # Split the output_filepath into directory, base (file name without extension), and extension
    directory, filename = os.path.split(output_filepath)
    base, extension = os.path.splitext(filename)

    # Add '_raw' to the base and reconstruct the file path
    raw_output_filepath = os.path.join(directory, base + '_raw' + extension)

    with open(raw_output_filepath, "w", encoding="utf-8") as md_file:
        for page_num, page_layout in enumerate(extract_pages(pdf_filepath)):
            md_file.write(f"\n\nNEW PAGE [{page_num + 1}]\n\n")
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    md_file.write(element.get_text())

    print(f"Raw markdown file from presentations generated at: {raw_output_filepath}")
    return raw_output_filepath


# Function to configure the API and load the chat model
def load_model() -> genai.GenerativeModel:
    """
    Configures the API and loads the chat model.

    Returns:
        genai.GenerativeModel: The loaded chat model.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    return model

# Function to read and chunk the Markdown content
def read_and_chunk_md_file(filepath: str, slides_per_chunk: int = 3) -> List[str]:
    """
    Reads a Markdown file and chunks the content.

    Args:
        filepath (str): Path to the Markdown file.
        slides_per_chunk (int, optional): Number of slides per chunk. Defaults to 3.

    Returns:
        List[str]: List of chunks.
    """    
    with open(filepath, "r") as file:
        content = file.read()

    # Split the content into pages
    pages = content.split("NEW PAGE")

    # Remove the first element if it's empty (this happens if the file starts with "NEW PAGE")
    if pages and not pages[0].strip():
        pages = pages[1:]

    # Group every 3 pages together into a chunk
    chunks = [
        "\n".join(pages[i : i + slides_per_chunk])
        for i in range(0, len(pages), slides_per_chunk)
    ]

    return chunks


# Function to generate detailed notes for each chunk
def generate_notes_for_chunks(model: genai.GenerativeModel, chunks: List[str], output_filepath: str, start_chunk: int) -> List[str]:
    """
    Generates detailed notes for each chunk.

    Args:
        model (genai.GenerativeModel): The chat model.
        chunks (List[str]): List of chunks.
        output_filepath (str): Path to the output notes file.
        start_chunk (int): Chunk to start from.

    Returns:
        List[str]: List of generated notes.
    """    
    
    chat = model.start_chat(history=[])
    prompt = """Generate detailed and information rich notes from these sparse slides. Notes you generate should be very informative and detailed (as much as possible) for the exam preparation. 
    Write your response formated in markdown and if there is mathematics or special characters enclose it in double dollar signs for Latex. Do not write any conclusion or anything like that - just informations for the exam prep in markdown and put math and special symbols between double dollar signs.\n\n"""
    notes = []
    for i, chunk in enumerate(tqdm(chunks[start_chunk:])):
        try:
            response = chat.send_message(prompt + chunk)
            notes.append(response.text)
            if VERBOSE:
                print(response.text)
        except Exception as e:
            time.sleep(11)
            model = load_model()
            chat = model.start_chat(history=[])
            print(f"Error: {e}")

            response = chat.send_message(prompt + chunk)
            notes.append(response.text)
            if VERBOSE:
                print(response.text)
        # Save notes to file after each chunk
        save_notes_to_file(response.text, output_filepath, mode='a')
    return notes

def save_notes_to_file(note: str, output_filepath: str, mode: str = 'wa') -> None:
    """
    Saves a note to a file.

    Args:
        note (str): The note to save.
        output_filepath (str): Path to the output file.
        mode (str, optional): Mode to open the file in. Defaults to 'wa'.
    """    
    with open(output_filepath, mode) as output_file:
            output_file.write(note + "\n\n")

# Main function to tie everything together
def main(pdf_filepath: str, output_filepath: str, start_chunk: int, batch_size: int) -> None:
    """
    Main function to tie everything together.

    Args:
        pdf_filepath (str): Path to the PDF file.
        output_filepath (str): Path to the output notes file.
        start_chunk (int): Chunk to start from.
    """
    model = load_model()
    raw_md_filepath = pdf_to_markdown(pdf_filepath, output_filepath)
    chunks = read_and_chunk_md_file(raw_md_filepath, slides_per_chunk=batch_size)
    notes = generate_notes_for_chunks(model, chunks, output_filepath, start_chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate detailed notes from a Markdown file"
    )
    parser.add_argument(
        "--pdf", type=str, help="Path to the Markdown file", required=True
    )
    parser.add_argument(
        "--output", type=str, help="Path to output notes file", default="notes.md"
    )
    parser.add_argument(
        "--start", type=int, help="Chunk to start from", default=0
    )
    parser.add_argument(
        "--batch_size", type=int, help="Number of slides per chunk", default=3
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print the generated notes to stdout"
    )
    args = parser.parse_args()
    VERBOSE = args.verbose

    main(args.pdf, args.output, args.start, args.batch_size)
