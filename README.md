# Sentence Corrector

A Python-based sentence correction tool powered by the Qwen3-0.6B language model. This tool automatically detects and corrects grammatical errors, spelling mistakes, and other language issues while preserving the original meaning of sentences.

## Features

- **Multi-language support** - correct sentences in any language
- **Batch processing** - correct multiple sentences at once
- **Delta encoding format** - get compact diff representations of corrections
- **Programmatic API** - integrate into your Python projects

## Installation

This project uses Python virtual environments to manage dependencies and ensure isolation from your system Python installation.

### Prerequisites

Before installing, ensure you have:
- `uv`, an extremely fast Python package and project manager.
- `make` utility (usually pre-installed on Linux/macOS, available via tools like MinGW on Windows)
- A CUDA-compatible GPU is highly recommended for optimal performance, though the tool can run on CPU
- At least 6GB of free disk space for the model and dependencies

### Installation Steps

Create a virtual environment and install all required packages:

```bash
make install
```

This command will:
1. Create a new virtual environment in the `.venv` directory
2. Install all necessary Python packages including vLLM and its dependencies
<!-- 3. Download the Qwen3-0.6B model automatically on first use -->

The installation may take several minutes depending on your internet connection, as it needs to download the language model and various Python packages.

## Post-Installation

### Activating the Virtual Environment

Before running any code, you need to activate the virtual environment. This ensures that you're using the correct Python interpreter and packages.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

On Windows, use:

```bash
.venv\Scripts\activate
```

Once activated, you'll see a prefix in your terminal prompt, indicating that the virtual environment is active.

### Deactivating the Virtual Environment

When you're done working with the project, you can exit the virtual environment:

```bash
deactivate
```

## Usage

The Sentence Corrector can be integrete in different ways: through the command-line interface (CLI) or via a web service for HTTP-based integrations.

### CLI

The `CLIrrector.py` script provides a simple command-line interface for correcting sentences.

#### CLI Options

- `sentence` - The sentence to correct (required)
- `-f, --format` - Output format: `sentence` (default) or `encode`
- `-l, --language` - Target language for correction (default: `french`)

#### Basic correction

Correct a sentence in French (default language):

```bash
uv run CLIrrector.py 'Bonjours le monde'
```

Output:
```
Bonjour le monde
```

#### Delta encoding format

Get corrections as delta encoding (shows only the differences):

```bash
uv run CLIrrector.py --format encode 'Bonjours le monde'
```

Output:
```
[(7, 1, '')]
```

#### Different languages

Correct sentences in different languages:

```bash
uv run CLIrrector.py --language english 'Hello every one'
```

Output:
```
Hello everyone
```

### SentenceCorrector API

Use the `SentenceCorrector` class directly in your Python code:

```python
from srcs.SentenceCorrector import SentenceCorrector

# Initialize the corrector
corrector = SentenceCorrector(
    target_language="english",
    format="sentence"
)

# Correct a single sentence
result = corrector.correct("This are a test sentense")
print(result[0])  # Output: "This is a test sentence"

# Correct multiple sentences (batch processing)
sentences = [
    "I has a pen",
    "She don't like apples",
    "They was here yesterday"
]
results = corrector.correct(sentences)
for correction in results:
    print(correction)
```

#### Using delta encoding

Delta encoding provides a compact representation of changes:

```python
corrector = SentenceCorrector(
    target_language="french",
    format="encode"
)

result = corrector.correct("Bonjours le monde")
print(result[0])  # Output: [(7, 1, '')]
```

Each tuple in the delta contains:
- Start position in the original string
- Length of the section to replace
- Replacement text

## How It Works

The Sentence Corrector uses the Qwen3-0.6B language model to analyze and correct sentences:

1. **Input Processing**: Sentences are formatted into a chat template
2. **Model Inference**: The language model generates corrections
3. **Output Formatting**: Results are returned in the specified format (full sentence or delta encoding)

## Acknowledgments

- Built with [vLLM](https://docs.vllm.ai/en/stable/index.html)
- Powered by [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) model