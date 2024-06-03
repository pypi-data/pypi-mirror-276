import re


def replace_array_value(texts, matched_text, sub_text, new_text):

    # Compile the regex pattern for better performance if texts is large
    pattern = re.compile(matched_text)
    sub = re.compile(sub_text)

    # Check if texts is a string and not a list
    if isinstance(texts, str):

        return re.sub(
            sub, new_text, texts
        )  # Apply the replacement and return the modified string
    elif isinstance(texts, list):
        # Use list comprehension to iterate over each item, search for the pattern and replace
        updated_texts = [
            (re.sub(sub, new_text, text) if re.match(pattern, text) else text)
            for text in texts
        ]
        return updated_texts
    else:
        raise ValueError("texts must be a string or a list of strings")


def replace_texts(src: list[str], texts: list[str] | str, new_text: str, bias=3):
    # loader = TextLoader(dir="../../datasets/text/_INVENTORY/words")
    # loader.load_file("personal-pronoun.txt")

    # replace start with personal noun
    pps = "|".join(text for text in src)
    matched_text = f"^({pps}).{{{bias},}}"
    sub_text = f"^({pps})"
    texts = replace_array_value(texts, matched_text, sub_text, new_text)

    # replace between personal noun
    pps = "|".join(text for text in src)
    matched_text = f"^.{{{bias},}}({pps})"
    sub_text = f"({pps})"
    texts = replace_array_value(texts, matched_text, sub_text, new_text)

    return texts
