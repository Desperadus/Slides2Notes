import argparse
import os
import textwrap
import time

from tqdm import tqdm

# Assuming the use of a hypothetical `genai` library similar to the one mentioned
import google.generativeai as genai

VERBOSE = False

# Function to configure the API and load the chat model


def load_model():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    return model


# Function to read and chunk the Markdown content
def read_and_chunk_md_file(filepath, slides_per_chunk=3):
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
def generate_notes_for_chunks(model, chunks, output_filepath, start_chunk):
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

def save_notes_to_file(note, output_filepath, mode='wa'):
    with open(output_filepath, mode) as output_file:
            output_file.write(note + "\n\n")

# Main function to tie everything together
def main(md_filepath, output_filepath, start_chunk):
    model = load_model()
    chunks = read_and_chunk_md_file(md_filepath)
    notes = generate_notes_for_chunks(model, chunks, output_filepath, start_chunk)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate detailed notes from a Markdown file"
    )
    parser.add_argument(
        "--mdpath", type=str, help="Path to the Markdown file", required=True
    )
    parser.add_argument(
        "--output", type=str, help="Path to output notes file", default="notes.md"
    )
    parser.add_argument(
        "--start", type=int, help="Chunk to start from", default=0
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print the generated notes to stdout"
    )
    args = parser.parse_args()
    VERBOSE = args.verbose

    main(args.mdpath, args.output, args.start)
