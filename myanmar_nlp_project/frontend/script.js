
/* ============================================================
   SAYARCHECK - TEXT PROCESSING
   ============================================================ */


/* ============================================================
   PROCESS TEXT
   ============================================================ */

async function processText() {

    const input =
        document.getElementById("inputText");

    const output =
        document.getElementById("outputText");

    const status =
        document.getElementById("status");


    /* ========================================================
       GET INPUT TEXT
       ======================================================== */

    const text =
        input.value.trim();


    /* ========================================================
       EMPTY INPUT
       ======================================================== */

    if (!text) {

        output.innerHTML = `
            <div class="output-placeholder">

                <div class="placeholder-icon">
                    ✓
                </div>

                <p>
                    Please enter Myanmar text first.
                </p>

            </div>
        `;

        status.textContent = "";

        return;
    }


    /* ========================================================
       SHOW PROCESSING
       ======================================================== */

    output.innerHTML = `
        <div class="output-placeholder">

            <div class="placeholder-icon">
                ...
            </div>

            <p>
                Processing your text...
            </p>

        </div>
    `;


    status.textContent =
        "Running SayarCheck...";


    try {

        /* ====================================================
           SEND TEXT TO FLASK
           ==================================================== */

        const response =
            await fetch(
                "/process",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


        /* ====================================================
           GET RESPONSE
           ==================================================== */

        const data =
            await response.json();


        /* ====================================================
           ERROR HANDLING
           ==================================================== */

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Processing failed"
            );

        }


        /* ====================================================
           CLEAR OLD OUTPUT
           ==================================================== */

        output.innerHTML = "";


        /* ====================================================
           PROCESSED / CORRECTED RESULT
           ==================================================== */

        const correctedResult =
            document.createElement("div");


        correctedResult.className =
            "segmented-result";


        correctedResult.textContent =
            data.corrected_result ||
            data.result ||
            "";


        output.appendChild(
            correctedResult
        );


        /* ====================================================
           SPELLING CHECK
           ==================================================== */

        const spellingSection =
            document.createElement("div");


        spellingSection.className =
            "spelling-section";


        const spellingTitle =
            document.createElement("h3");


        spellingTitle.textContent =
            "Spelling Check";


        spellingSection.appendChild(
            spellingTitle
        );


        let spellingErrorCount = 0;


        /* ====================================================
           CHECK SPELLING DATA
           ==================================================== */

        if (
            data.spelling &&
            Array.isArray(data.spelling)
        ) {

            data.spelling.forEach(
                item => {

                    /* ----------------------------------------
                       ONLY SHOW INCORRECT WORDS
                       ---------------------------------------- */

                    if (!item.correct) {

                        spellingErrorCount++;


                        const errorBox =
                            document.createElement(
                                "div"
                            );


                        errorBox.className =
                            "spelling-error";


                        /* ------------------------------------
                           MISSPELLED WORD
                           ------------------------------------ */

                        const word =
                            document.createElement(
                                "strong"
                            );


                        word.textContent =
                            item.word || "";


                        errorBox.appendChild(
                            word
                        );


                        /* ------------------------------------
                           ERROR TYPE
                           ------------------------------------ */

                        if (item.error_type) {

                            const errorType =
                                document.createElement(
                                    "div"
                                );


                            errorType.className =
                                "suggestions";


                            errorType.textContent =
                                "Type: " +
                                item.error_type;


                            errorBox.appendChild(
                                errorType
                            );

                        }


                        /* ------------------------------------
                           SUGGESTIONS
                           ------------------------------------ */

                        if (
                            item.suggestions &&
                            Array.isArray(item.suggestions) &&
                            item.suggestions.length > 0
                        ) {

                            const suggestionText =
                                document.createElement(
                                    "div"
                                );


                            suggestionText.className =
                                "suggestions";


                            const suggestions =
                                item.suggestions
                                    .map(
                                        suggestion => {

                                            if (
                                                typeof suggestion ===
                                                "string"
                                            ) {
                                                return suggestion;
                                            }

                                            return suggestion.word ||
                                                   suggestion.suggestion ||
                                                   "";

                                        }
                                    )
                                    .filter(
                                        suggestion =>
                                            suggestion !== ""
                                    )
                                    .join(", ");


                            suggestionText.textContent =
                                "Suggestions: " +
                                suggestions;


                            errorBox.appendChild(
                                suggestionText
                            );

                        }


                        /* ------------------------------------
                           ADD ERROR BOX
                           ------------------------------------ */

                        spellingSection.appendChild(
                            errorBox
                        );

                    }

                }
            );

        }


        /* ====================================================
           NO SPELLING ERRORS
           ==================================================== */

        if (
            spellingErrorCount === 0
        ) {

            const success =
                document.createElement(
                    "div"
                );


            success.className =
                "spelling-success";


            success.textContent =
                "✓ No spelling errors detected";


            spellingSection.appendChild(
                success
            );

        }


        /* ====================================================
           ADD SPELLING SECTION
           ==================================================== */

        output.appendChild(
            spellingSection
        );


       /* ====================================================
   TYPOGRAPHICAL CHECK
   ==================================================== */

const typoSection = document.createElement("div");

typoSection.className = "spelling-section";


const typoTitle = document.createElement("h3");

typoTitle.textContent = "Typographical Check";

typoSection.appendChild(typoTitle);


let typoCount = 0;


/* ====================================================
   WORD TYPOS
   ==================================================== */

if (
    data.typographical &&
    Array.isArray(data.typographical.word_typos)
) {

    data.typographical.word_typos.forEach(item => {

        typoCount++;

        const errorBox =
            document.createElement("div");

        errorBox.className =
            "spelling-error";


        const word =
            document.createElement("strong");

        word.textContent =
            item.word || "";

        errorBox.appendChild(word);


        const type =
            document.createElement("div");

        type.className =
            "suggestions";

        type.textContent =
            "Type: " +
            (item.error_type || "Typographical error");

        errorBox.appendChild(type);


        if (item.suggestion) {

            const suggestion =
                document.createElement("div");

            suggestion.className =
                "suggestions";

            suggestion.textContent =
                "Suggested: " +
                item.suggestion;

            errorBox.appendChild(suggestion);
        }


        if (item.description) {

            const description =
                document.createElement("div");

            description.className =
                "suggestions";

            description.textContent =
                item.description;

            errorBox.appendChild(description);
        }


        typoSection.appendChild(errorBox);

    });
}


/* ====================================================
   FORMATTING TYPOS
   ==================================================== */

if (
    data.typographical &&
    Array.isArray(data.typographical.formatting_typos)
) {

    data.typographical.formatting_typos.forEach(item => {

        typoCount++;

        const errorBox =
            document.createElement("div");

        errorBox.className =
            "spelling-error";


        const word =
            document.createElement("strong");

        word.textContent =
            item.text || "";

        errorBox.appendChild(word);


        const type =
            document.createElement("div");

        type.className =
            "suggestions";

        type.textContent =
            "Type: " +
            (item.type || "Formatting error");

        errorBox.appendChild(type);


        if (item.description) {

            const description =
                document.createElement("div");

            description.className =
                "suggestions";

            description.textContent =
                item.description;

            errorBox.appendChild(description);
        }


        if (item.suggestion) {

            const suggestion =
                document.createElement("div");

            suggestion.className =
                "suggestions";

            suggestion.textContent =
                "Suggested: " +
                item.suggestion;

            errorBox.appendChild(suggestion);
        }


        typoSection.appendChild(errorBox);

    });
}


/* ====================================================
   NO TYPOGRAPHICAL ERRORS
   ==================================================== */

if (typoCount === 0) {

    const success =
        document.createElement("div");

    success.className =
        "spelling-success";

    success.textContent =
        "✓ No typographical errors detected";

    typoSection.appendChild(success);
}


/* ====================================================
   ADD SECTION TO OUTPUT
   ==================================================== */

output.appendChild(typoSection);
        /* ====================================================
           COMPLETE
           ==================================================== */

        status.textContent =
            "✓ SayarCheck completed successfully";


    } catch (error) {

        /* ====================================================
           ERROR DISPLAY
           ==================================================== */

        console.error(
            "SayarCheck Error:",
            error
        );


        output.innerHTML = `
            <div class="output-placeholder">

                <div class="placeholder-icon">
                    !
                </div>

                <p>
                    Something went wrong.
                </p>

            </div>
        `;


        status.textContent =
            "Error: " +
            error.message;

    }

}


/* ============================================================
   USE EXAMPLE
   ============================================================ */

function useExample(text) {

    const input =
        document.getElementById(
            "inputText"
        );


    input.value =
        text;


    input.focus();


    input.selectionStart =
        input.value.length;


    input.selectionEnd =
        input.value.length;

}


/* ============================================================
   CLEAR TEXT
   ============================================================ */

function clearText() {

    /* --------------------------------------------------------
       CLEAR INPUT
       -------------------------------------------------------- */

    document.getElementById(
        "inputText"
    ).value = "";


    /* --------------------------------------------------------
       RESET OUTPUT
       -------------------------------------------------------- */

    document.getElementById(
        "outputText"
    ).innerHTML = `

        <div class="output-placeholder">

            <div class="placeholder-icon">
                ✓
            </div>

            <p>
                Your processed text
                will appear here.
            </p>

        </div>

    `;


    /* --------------------------------------------------------
       CLEAR STATUS
       -------------------------------------------------------- */

    document.getElementById(
        "status"
    ).textContent = "";

}
