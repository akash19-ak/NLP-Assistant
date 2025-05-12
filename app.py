from flask import Flask, render_template, request, url_for
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from nltk.corpus import wordnet as wn
import nltk
import os
import random

# Ensure WordNet is available
try:
    wn.synsets('dog')
except:
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('averaged_perceptron_tagger')

# Load GPT-2 model with explicit model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Configure Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_text = []
    synonyms = []
    antonyms = []
    examples = []
    framed_sentences = []
    categories = {}

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "generate":
            prompt = request.form['prompt']
            output = generator(prompt, max_new_tokens=5, num_return_sequences=3)
            generated_words = set()
            for o in output:
                full_text = o['generated_text']
                new_part = full_text[len(prompt):].strip()
                first_word = new_part.split()[0] if new_part else ''
                if first_word:
                    generated_words.add(first_word)
            generated_text = list(generated_words)

        elif action == "synonym":
            word = request.form['word']
            synsets = wn.synsets(word)
            seen = set()
            if not synsets:
                synonyms.append(f"No synonyms found for '{word}'")
            else:
                for syn in synsets:
                    # Add synonyms
                    for lemma in syn.lemmas():
                        name = lemma.name().replace('_', ' ')
                        if name.lower() != word.lower() and name not in seen:
                            synonyms.append(name)
                            seen.add(name)

                    # Add example sentences
                    for example in syn.examples():
                        example_clean = example.strip().capitalize()
                        examples.append(f"{syn.name().split('.')[0]} ({syn.pos()}): {example_clean}")
        
        # New functionality: Antonym lookup
        elif action == "antonym":
            word = request.form['word']
            synsets = wn.synsets(word)
            seen = set()
            if not synsets:
                antonyms.append(f"No antonyms found for '{word}'")
            else:
                found_antonyms = False
                for syn in synsets:
                    for lemma in syn.lemmas():
                        for antonym in lemma.antonyms():
                            antonym_name = antonym.name().replace('_', ' ')
                            if antonym_name not in seen:
                                antonyms.append(antonym_name)
                                seen.add(antonym_name)
                                found_antonyms = True
                
                if not found_antonyms:
                    antonyms.append(f"No antonyms found for '{word}'")

        # New functionality: Sentence Framer
        elif action == "frame":
            word = request.form['word']
            templates = [
                "The {} was an important part of the discussion.",
                "I've never seen such a {} before.",
                "Can you explain what {} means in this context?",
                "Everyone was talking about the {} at the meeting.",
                "The {} is essential for understanding this concept.",
                "She mentioned {} as a key factor in her decision.",
                "The book contains several references to {}.",
                "We need to consider {} when making our plans."
            ]
            
            # Generate framed sentences
            for template in templates[:3]:  # Limit to 3 sentences
                framed_sentences.append(template.format(word))
            
            # Also try to get a real example from WordNet
            synsets = wn.synsets(word)
            if synsets:
                for syn in synsets[:2]:  # Get examples from first 2 synsets
                    for example in syn.examples():
                        if word.lower() in example.lower():
                            framed_sentences.append(f"WordNet: {example.strip().capitalize()}")
                            break

        # New functionality: Word Categorizer
        elif action == "categorize":
            word = request.form['word']
            synsets = wn.synsets(word)

            if not synsets:
                categories["message"] = f"No information found for '{word}'"
            else:
                pos_mapping = {
                    'n': 'Noun',
                    'v': 'Verb',
                    'a': 'Adjective',
                    's': 'Adjective Satellite',
                    'r': 'Adverb'
                }

                # Collect POS
                pos_set = {pos_mapping.get(syn.pos(), syn.pos()) for syn in synsets}
                categories["Part of Speech"] = list(pos_set)

                # Collect Hypernyms (categories)
                hypernyms = set()
                for syn in synsets[:2]:
                    for hyper in syn.hypernyms():
                        name = hyper.name().split('.')[0].replace('_', ' ')
                        hypernyms.add(name)
                if hypernyms:
                    categories["Categories"] = list(hypernyms)

                # Collect Lexname Domains (safer alternative to topic_domains)
                lexnames = {syn.lexname().replace('.', ' ').title() for syn in synsets}
                if lexnames:
                    categories["Domains"] = list(lexnames)

    return render_template('index.html',
                           generated_text=generated_text,
                           synonyms=synonyms,
                           antonyms=antonyms,
                           examples=examples,
                           framed_sentences=framed_sentences,
                           categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
