
import re
import unicodedata

from spelling_checker import check_spelling


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    return unicodedata.normalize("NFC", text)


# ============================================================
# CHARACTER-LEVEL TYPO CLASSIFICATION
# ============================================================

def classify_character_error(original, corrected):

    original = normalize_text(original)
    corrected = normalize_text(corrected)

    # Same word
    if original == corrected:
        return None

    # --------------------------------------------------------
    # EXTRA CHARACTER
    # Example:
    # ကျောင်းး -> ကျောင်း
    # --------------------------------------------------------

    if len(original) == len(corrected) + 1:

        for i in range(len(original)):

            test = (
                original[:i]
                + original[i + 1:]
            )

            if test == corrected:

                return {
                    "type": "Extra character",
                    "description": "An extra character was typed.",
                    "character": original[i]
                }

    # --------------------------------------------------------
    # MISSING CHARACTER
    # Example:
    # ကျောငး် -> ကျောင်း
    # --------------------------------------------------------

    if len(corrected) == len(original) + 1:

        for i in range(len(corrected)):

            test = (
                corrected[:i]
                + corrected[i + 1:]
            )

            if test == original:

                return {
                    "type": "Missing character",
                    "description": "A character is missing.",
                    "character": corrected[i]
                }

    # --------------------------------------------------------
    # SAME LENGTH
    # --------------------------------------------------------

    if len(original) == len(corrected):

        differences = []

        for i in range(len(original)):

            if original[i] != corrected[i]:
                differences.append(i)

        # ----------------------------------------------------
        # ONE WRONG CHARACTER
        # ----------------------------------------------------

        if len(differences) == 1:

            i = differences[0]

            return {
                "type": "Wrong character",
                "description": "A character was typed incorrectly.",
                "typed": original[i],
                "correct": corrected[i]
            }

        # ----------------------------------------------------
        # SWAPPED CHARACTERS
        # ----------------------------------------------------

        if len(differences) == 2:

            i, j = differences

            if (
                j == i + 1
                and original[i] == corrected[j]
                and original[j] == corrected[i]
            ):

                return {
                    "type": "Swapped characters",
                    "description":
                        "Two neighboring characters were reversed."
                }

    return None


# ============================================================
# WORD TYPO DETECTION
# ============================================================

def detect_word_typos(text):

    results = []

    # Extract Myanmar words
    words = re.findall(
        r"[\u1000-\u109F]+",
        text
    )

    for word in words:

        try:

            suggestions = check_spelling(
                word,
                max_suggestions=5
            )

        except Exception as e:

            print(
                "Spelling checker error:",
                e
            )

            continue

        # No suggestions
        if not suggestions:
            continue

        best = suggestions[0]

        corrected = best.get(
            "word",
            word
        )

        distance = best.get(
            "distance",
            999
        )

        # Already correct
        if (
            corrected == word
            and distance == 0
        ):
            continue

        # Only consider very close matches
        if distance <= 1:

            error = classify_character_error(
                word,
                corrected
            )

            if error:

                results.append({
                    "word": word,
                    "suggestion": corrected,
                    "distance": distance,
                    "error_type":
                        error["type"],
                    "description":
                        error["description"]
                })

    return results


# ============================================================
# FORMATTING TYPO DETECTION
# ============================================================

def detect_formatting_typos(text):

    results = []

    # Normalize Unicode
    text = normalize_text(text)

    # ========================================================
    # 1. MULTIPLE SPACES
    # ========================================================
    #
    # Example:
    # မင်္ဂလာ  ပါ
    #
    # Detects:
    # two or more normal spaces
    # two or more tab characters
    #
    # ========================================================

    for match in re.finditer(
        r"[ \t]{2,}",
        text
    ):

        results.append({

            "type":
                "Extra spaces",

            "text":
                match.group(),

            "description":
                "Multiple spaces were entered.",

            "suggestion":
                " "
        })

    # ========================================================
    # 2. REPEATED PUNCTUATION
    # ========================================================
    #
    # Examples:
    # ။။
    # !!!
    # ???
    # ,,,
    #
    # ========================================================

    for match in re.finditer(
        r"([၊။,.!?])\1+",
        text
    ):

        results.append({

            "type":
                "Repeated punctuation",

            "text":
                match.group(),

            "description":
                "The same punctuation mark was repeated.",

            "suggestion":
                match.group(1)
        })

    # ========================================================
    # 3. SPACE BEFORE PUNCTUATION
    # ========================================================
    #
    # Example:
    # မင်္ဂလာပါ ။
    #
    # ========================================================

    for match in re.finditer(
        r"[ \t]+([၊။,.!?])",
        text
    ):

        results.append({

            "type":
                "Space before punctuation",

            "text":
                match.group(),

            "description":
                "There should not be a space before punctuation.",

            "suggestion":
                match.group(1)
        })

    # ========================================================
    # 4. MISSING SPACE AFTER ENGLISH PUNCTUATION
    # ========================================================
    #
    # Example:
    # Hello,World
    #
    # ========================================================

    for match in re.finditer(
        r"([,.!?])([A-Za-z\u1000-\u109F])",
        text
    ):

        results.append({

            "type":
                "Missing space",

            "text":
                match.group(),

            "description":
                "A space may be required after punctuation.",

            "suggestion":
                match.group(1)
                + " "
                + match.group(2)
        })

    # ========================================================
    # 5. MIXED PUNCTUATION
    # ========================================================
    #
    # Examples:
    # ။!
    # !။
    # ၊?
    #
    # ========================================================

    for match in re.finditer(
        r"[!?][၊။]|[၊။][!?]",
        text
    ):

        results.append({

            "type":
                "Mixed punctuation",

            "text":
                match.group(),

            "description":
                "Mixed punctuation marks were used.",

            "suggestion":
                match.group(0)[0]
        })

    return results


# ============================================================
# COMPLETE TYPOGRAPHICAL CHECK
# ============================================================

def detect_typographical_errors(
    original_text,
    segmented_text
):

    print("\n======================================")
    print("TYPOGRAPHICAL CHECK")
    print("======================================")

    print(
        "Original text:",
        repr(original_text)
    )

    print(
        "Segmented text:",
        repr(segmented_text)
    )

    # --------------------------------------------------------
    # Word-level typos
    # --------------------------------------------------------

    word_typos = detect_word_typos(
        segmented_text
    )

    # --------------------------------------------------------
    # Formatting typos
    # --------------------------------------------------------

    formatting_typos = detect_formatting_typos(
        original_text
    )

    print(
        "Word typos:",
        word_typos
    )

    print(
        "Formatting typos:",
        formatting_typos
    )

    print("======================================\n")

    return {

        "word_typos":
            word_typos,

        "formatting_typos":
            formatting_typos
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_cases = [

        # Extra spaces
        "မင်္ဂလာ  ပါ။",

        # Repeated punctuation
        "မင်္ဂလာပါ။။",

        # Space before punctuation
        "မင်္ဂလာပါ ။",

        # Missing space after English punctuation
        "Hello,World",

        # Mixed punctuation
        "မင်္ဂလာပါ။!",

        # Multiple spaces
        "ဒီနေ့   ရာသီဥတုကောင်းပါတယ်။",

        # Normal sentence
        "မင်္ဂလာပါ။ ဒီနေ့ ရာသီဥတုကောင်းပါတယ်။"
    ]

    for text in test_cases:

        print("\n--------------------------------------")

        print("TEST INPUT:")
        print(text)

        result = detect_typographical_errors(
            text,
            text
        )

        print("RESULT:")
        print(result)

