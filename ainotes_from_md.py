import argparse
import os
import textwrap

from tqdm import tqdm

# Assuming the use of a hypothetical `genai` library similar to the one mentioned
import google.generativeai as genai


# Function to configure the API and load the chat model
def load_model():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    return model


# Function to read and chunk the Markdown content
def read_and_chunk_md_file(filepath, chunk_size=200):
    with open(filepath, "r") as file:
        content = file.read()

    # Split the content into words and re-join into chunks
    words = content.split()
    chunks = [
        " ".join(words[i: i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]
    return chunks


# Function to generate detailed notes for each chunk
def generate_notes_for_chunks(model, chunks):
    chat = model.start_chat(history=[])
    notes = []
    for chunk in tqdm(chunks):
        response = chat.send_message(chunk)
        notes.append(response.text)
    return notes


# Main function to tie everything together
def main(md_filepath, output_filepath):
    model = load_model()
    chunks = read_and_chunk_md_file(md_filepath)
    notes = generate_notes_for_chunks(model, chunks)

    # Save the generated notes to an output file
    with open(output_filepath, "w") as output_file:
        for note in notes:
            output_file.write(note + "\n\n")


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
    args = parser.parse_args()

    main(args.mdpath, args.output)
