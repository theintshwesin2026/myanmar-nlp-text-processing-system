import json
import re

from symspellpy import SymSpell


# ============================================================
# DICTIONARY
# ============================================================

DICTIONARY_PATH = (
    "preprocessing/spelling_dictionary.json"
)


# ============================================================
# LOAD WORD FREQUENCIES
# ============================================================

with open(
    DICTIONARY_PATH,
    "r",
    encoding="utf-8"
) as f:

    word_frequencies = json.load(f)


# ============================================================
# CREATE SYMSPELL
# ============================================================

sym_spell = SymSpell(
    max_dictionary_edit_distance=2,
    prefix_length=7
)


# ============================================================
# LOAD MYANMAR WORDS
# ============================================================

for word, frequency in word_frequencies.items():

    # Skip very short entries

    if len(word) < 2:
        continue


    # Keep Myanmar words only

    if not re.search(
        r"[\u1000-\u109F]",
        word
    ):
        continue


    # Skip words containing Latin characters

    if re.search(
        r"[A-Za-z]",
        word
    ):
        continue


    sym_spell.create_dictionary_entry(
        word,
        frequency
    )


print(
    "Spelling dictionary loaded."
)

print(
    "Unique words:",
    len(word_frequencies)
)


# ============================================================
# SPELLING CHECK
# ============================================================

def check_spelling(
    word,
    max_suggestions=5
):

    suggestions = sym_spell.lookup(
        word,
        verbosity=2,
        max_edit_distance=2
    )


    results = []


    for suggestion in suggestions[
        :max_suggestions
    ]:

        results.append({

            "word":
                suggestion.term,

            "distance":
                suggestion.distance,

            "frequency":
                suggestion.count

        })


    return results


# ============================================================
# AUTOMATIC SPELLING CORRECTION
# ============================================================

def correct_word(word):
    """
    Automatically correct a word only when
    SymSpell finds a very close spelling match.
    """

    suggestions = check_spelling(
        word,
        max_suggestions=5
    )

    # No suggestion
    if not suggestions:
        return word

    best = suggestions[0]

    # Already correct
    if best["distance"] == 0:
        return word

    # Only auto-correct very close matches
    if best["distance"] == 1:
        return best["word"]

    # Do NOT change uncertain words
    return word
# ============================================================
# AUTOMATIC SPELLING CORRECTION
# ============================================================

def correct_text(text):

    """
    Automatically correct spelling
    in a segmented sentence.
    """

    words = text.split()

    corrected_words = []


    for word in words:

        corrected_word = correct_word(
            word
        )


        corrected_words.append(
            corrected_word
        )


    return " ".join(
        corrected_words
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_words = [

        "မြန်မာ",

        "အဆင်ပြေ်",

        "နိုင်ငံ"

    ]


    for word in test_words:

        print(
            "\nInput:",
            word
        )


        suggestions = check_spelling(
            word
        )


        if not suggestions:

            print(
                "No suggestions found."
            )


        else:

            for suggestion in suggestions:

                print(
                    f"  {suggestion['word']}"
                    f" | distance={suggestion['distance']}"
                    f" | frequency={suggestion['frequency']}"
                )


        print(
            "Corrected:",
            correct_word(word)
        )