# Slides2Notes
Project to automaticly generate lecture notes using AI
## Prerequisites
Python 3.9 or newer.

Poetry for dependency management.

Access to a terminal or command prompt.

Being in country where Gemini API is allowed (works in USA but not in EU). You can use some VPN to work around this.
## Setup
Install Poetry: If you haven't installed Poetry, follow the official [installation guide](https://python-poetry.org/docs/).

### Project Setup:
Clone the repository to your local machine.

run `poetry install` in the project directory to install the required dependencies.

and then `poetry shell` to activate the virtual environment.

Environment Variables: Ensure you have GOOGLE_API_KEY set in your environment variables, as both scripts require access to Google's Generative AI services. You can get your API key here https://ai.google.dev/
## Usage
### Converting Images of Slides to Markdown Notes

Prepare your Images: Ensure all images of slides are in PNG format and located in a known directory.

You can create for example images from your pdf slides using the following command:

`pdftoppm slides.pdf imgslides -pdf`

Run img_to_md.py:

Open a terminal and navigate to your project directory.

Activate the Poetry shell: `poetry shell`

Run the script with the required arguments. For example:

```bash
python3 img_to_md.py --imgpaths "path/to/images/*.png" --output "output.md" --verbose
```

The script will process the images and generate a markdown file with the notes generated using gemini AI.
### Converting Text from Slide to Markdown AI Notes:
Prepare your PDF: Make sure the PDF file of your presentation is accessible.

Run ainotes_from_pdf.py:

Activate the Poetry shell if not already active: `poetry shell`
Execute the script, specifying the PDF path and desired output file. For example:

```bash
python3 ainotes_from_pdf.py --pdf "path/to/presentation.pdf" --output "notes.md" --start 0 --batch_size 3 --verbose
```
The script will convert the PDF to a raw Markdown file, then enhance it into detailed notes, saving the result to notes.md.


#### Final notes
Adjust --batch_size in ainotes_from_pdf.py based on the complexity of your PDFs and the desired detail level in notes.

Also if generation fails for some reason you can opt to start generation from specific chunk using --start argument and giving it an integer.
