# Myanmar NLP System
### Myanmar Word Segmentation & Spelling Assistance

A Myanmar-language text processing project that combines Unicode normalization, syllable tokenization, a **BiLSTM-CRF** sequence-labeling model for word segmentation, and dictionary-based spelling suggestions.

> **Project status:** Research / academic project. The repository contains the application and model code. Large model and dictionary files are intentionally handled separately because they exceed GitHub's normal file-size recommendations.

## Preview

<!-- Add your own screenshots to the screenshots/ folder and keep these filenames,
     or change the paths below to match your image names. -->
| Application interface | Processed Myanmar text |
|---|---|
| ![Application interface](screenshots/app-interface.png) | ![Segmentation result](screenshots/segmentation-result.png) |

**Before publishing:** Replace these preview images with real screenshots from your running application. Do not leave broken image links in the final repository.

## Features

- Myanmar Unicode NFC normalization and zero-width-space cleanup
- Myanmar syllable-like tokenization before model inference
- Word segmentation using a trained BiLSTM-CRF model
- Dictionary-based spelling suggestions using SymSpell
- Flask backend with a simple HTML, CSS, and JavaScript interface
- CPU, NVIDIA CUDA, and Apple MPS device selection where supported

## How it works

1. The user enters Myanmar text in the web interface.
2. The Flask API receives the text through `POST /process`.
3. The text is normalized and split into syllable-like tokens.
4. Tokens are mapped to vocabulary IDs.
5. The BiLSTM-CRF model predicts beginning/inside (`B`/`I`) tags.
6. The predicted tags are combined to produce segmented words.
7. The spelling checker looks up each segmented word and returns possible suggestions.

## Model and reported baseline

The following figures are recorded in `BASELINE_RESULT.txt` and are reported project results, not an independent reproduction or guarantee.

| Item | Reported value |
|---|---:|
| Model | BiLSTM-CRF |
| Task | Myanmar word segmentation |
| Training examples | 489,719 |
| Validation examples | 54,414 |
| Official test examples | 28,639 |
| Validation F1 | 0.9013 |
| Official test F1 | 0.9008 |
| Vocabulary size | 54,395 |
| Embedding dimension | 128 |
| LSTM hidden dimension | 128 |
| LSTM layers | 2 |
| Dropout | 0.3 |
| Optimizer | Adam / AdamW in the training script |
| Training epochs | 3 |

**Important:** The reported evaluation values should be accompanied by the dataset split and evaluation method when presenting this project. The training script currently creates a 90/10 split from the dataset's `train` partition; the official test result is recorded separately.

## Technology stack

- **Language:** Python
- **Backend:** Flask
- **Machine learning:** PyTorch, BiLSTM, CRF
- **Text processing:** Python `unicodedata`, regular expressions, SymSpell
- **Frontend:** HTML, CSS, JavaScript
- **Dataset loading:** Hugging Face `datasets`

## Repository structure

```text
myanmar_nlp_project/
├── app.py
├── train.py
├── predict.py
├── spelling_checker.py
├── models/
│   ├── bilstm_crf.py
│   └── dataset.py
├── preprocessing/
│   ├── syllable_tokenizer.py
│   ├── unicode_normalizer.py
│   ├── vocabulary.py
│   ├── vocab.json                 # large vocabulary; manage separately if needed
│   └── spelling_dictionary.json   # large file; do not push directly to GitHub
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── checkpoints/
│   └── best_model.pt              # model weights; manage separately if needed
├── augmentation/
├── screenshots/
├── BASELINE_RESULT.txt
├── requirements.txt
├── .gitignore
└── README.md
```

The uploaded project archive does not include the original dataset files. The training script loads the dataset from Hugging Face using `chuuhtetnaing/myanmar-text-segmentation-dataset`.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/myanmar-nlp-project.git
cd myanmar-nlp-project
```

Replace `YOUR-USERNAME` with your GitHub username and use your actual repository name.

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add the required model and dictionary files

The application expects these files at the following locations:

```text
checkpoints/best_model.pt
preprocessing/vocab.json
preprocessing/spelling_dictionary.json
```

They are large binary/data assets and may be distributed separately (for example, through Git LFS or a suitable model/dataset hosting service). Download them from the project's official release location and place them at the paths above.

**Do not create fake or empty files with these names.** The application will not work without valid files that match the model architecture and vocabulary.

### 5. Run the web application

From the project root:

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

Stop the server with `Ctrl + C`.

## Training

The training script downloads the dataset through Hugging Face `datasets`:

```bash
python train.py
```

Training can require substantial memory, disk space, and time. The script automatically selects Apple MPS, NVIDIA CUDA, or CPU when available. Training on CPU may be significantly slower.

## API

### `POST /process`

Processes a Myanmar text string.

**Request body:**

```json
{
  "text": "မြန်မာစာကို ဒီနေရာတွင် ရိုက်ထည့်ပါ။"
}
```

**Successful response shape:**

```json
{
  "result": "segmented Myanmar text",
  "spelling": [
    {
      "word": "example",
      "correct": true,
      "suggestions": []
    }
  ]
}
```

The exact spelling suggestions depend on the dictionary contents and the input text.

## Screenshots: how to add them

1. Start the app using `python app.py`.
2. Open `http://127.0.0.1:5000`.
3. Take a screenshot of the empty/input interface and save it as `screenshots/app-interface.png`.
4. Enter a representative Myanmar sentence and click **Process Text**.
5. Take another screenshot showing the processed output and save it as `screenshots/segmentation-result.png`.
6. Check that Myanmar characters are readable and that no personal information, local file paths, debug console, or API secrets are visible.
7. Commit the screenshots with the README.

On Windows, use `Win + Shift + S` to capture the relevant area. On macOS, use `Shift + Command + 4`.

## Current limitations and notes

- Segmentation quality depends on the training data, vocabulary, tokenizer, and model checkpoint.
- Tokens not found in the vocabulary are mapped to the `<UNK>` token.
- Spelling suggestions are dictionary/edit-distance based; they are not a complete Myanmar grammar checker.
- The application loads its model and spelling dictionary when `app.py` starts.
- The project archive does not contain the source dataset itself.
- Large checkpoints and dictionaries should be distributed separately or through Git LFS rather than committed as ordinary Git files.
- Run and test the project locally before describing it as deployed or production-ready.

## Future improvements

- Add unit tests for normalization, tokenization, segmentation, and spelling suggestions.
- Improve error handling and input validation in the Flask API.
- Add a clear loading state and more informative error messages to the interface.
- Provide reproducible environment versions and documented model/dataset download links.
- Deploy a demo so visitors can try the application without installing it.

## Acknowledgements

- Dataset: [`chuuhtetnaing/myanmar-text-segmentation-dataset`](https://huggingface.co/datasets/chuuhtetnaing/myanmar-text-segmentation-dataset)
- PyTorch, Flask, Hugging Face Datasets, and SymSpell contributors.

## Author

**Theint Shwe Sin**

Computer Science / IT student interested in software development, natural language processing, and building practical web applications.

- GitHub: [YOUR-GITHUB-USERNAME](https://github.com/theintshwesin2026)
- LinkedIn: [YOUR-LINKEDIN-PROFILE](https://www.linkedin.com/in/theint-shwe-sin-67a0aa421?utm_source=share_via&utm_content=profile&utm_medium=member_ios)

---

If you use or build on this project, please provide appropriate credit and check the licenses/terms of the dataset and dependencies.
