# NLP-Assistant

# NLP Word Predictor & Dictionary

## README File

Now, let's create a README.md file for your project:

```markdown:c:\Users\Palguna\Desktop\akash\README.md
# NLP Word Predictor & Dictionary

A Flask-based web application that uses GPT-2 for word prediction and WordNet for synonym lookup and example sentences.

![Application Screenshot](static/images/screenshot.png)

## Features

- **Word Prediction**: Uses GPT-2 to predict the next word(s) in a given prompt
- **Synonym Lookup**: Finds synonyms for a given word using WordNet
- **Example Sentences**: Provides example sentences for words using WordNet

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone this repository or download the source code:

```bash
git clone https://github.com/yourusername/nlp-word-predictor.git
cd nlp-word-predictor
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install flask transformers torch nltk
```

4. Download required NLTK data:

```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

## Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

## Usage Examples

### Word Prediction

1. Enter a prompt in the "Word Prediction" tab, such as:
   ```
   The weather is
   ```

2. Click "Generate"

3. Example output:
   ```
   - nice
   - beautiful
   - changing
   ```

### Synonym Lookup

1. Enter a word in the "Synonym Lookup" tab, such as:
   ```
   happy
   ```

2. Click "Find Synonyms"

3. Example output:
   
   Synonyms:
   ```
   - glad
   - joyful
   - content
   - pleased
   - delighted
   ```
   
   Example Sentences:
   ```
   - happy (a): I was happy to see her.
   - happy (a): She was happy about the new job.
   ```

## Project Structure

```
nlp-word-predictor/
├── app.py                  # Main Flask application
├── static/
│   ├── style.css           # CSS styles
│   └── images/             # Images for the application
├── templates/
│   └── index.html          # HTML template
└── README.md               # This file
```

## Technologies Used

- **Flask**: Web framework
- **Transformers**: Hugging Face library for NLP models
- **PyTorch**: Deep learning framework
- **NLTK**: Natural Language Toolkit for WordNet
- **HTML/CSS/JavaScript**: Frontend

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for the Transformers library
- Princeton University for WordNet
```

To complete the UI improvements, you'll need to create a folder for images:

```bash
mkdir -p c:\Users\Palguna\Desktop\akash\static\images
```
