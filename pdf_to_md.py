import google.generativeai as genai
import os
import glob
import argparse
import PIL.Image
from tqdm import tqdm
import prompts

VERBOSE = False

def printing(*args, **kwargs):
    if VERBOSE:
        tqdm.write(*args, **kwargs)

def load_model():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-pro-vision")
    return model

def get_text_from_image(model, png_slides, intro_prompt=prompts.basic_eng, new_image_prompt=prompts.new_image_prompt_eng):
    # chat = model.start_chat(history=[])
    results = []
    response = model.generate_content([intro_prompt, PIL.Image.open(png_slides[2])])
    results.append(response.text)
    printing(response.text)

    for slide in tqdm(png_slides[3:10]):
        image = PIL.Image.open(slide)
        response = model.generate_content([new_image_prompt,image])
        results.append(response.text)
        printing(response.text)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    parser.add_argument('--imgpaths', nargs='*', help='Path to PNG images, e.g., "*.png"', required=True)
    parser.add_argument('--output', type=str, help='Path to output markdown file', default="output.md")
    parser.add_argument('--verbose', action='store_true', help='Print verbose output')
    args = parser.parse_args()
    VERBOSE = args.verbose

    img_paths = []
    for path in args.imgpaths:
        img_paths.extend(glob.glob(path))


    model = load_model()
    results = get_text_from_image(model, img_paths)
    result = "\n".join(results)
    result = result.replace(" #", "#")
    with open(args.output, "w") as f:
        f.write(result)
