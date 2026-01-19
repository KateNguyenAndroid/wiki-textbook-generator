import wikipediaapi
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

def get_wikipedia_content(topic):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(topic)
    
    if not page.exists():
        return None
    
    return page.text, page.fullurl

def create_textbook(topics):
    os.makedirs('textbooks', exist_ok=True)
    combined_content = ""

    for topic in topics:
        content, url = get_wikipedia_content(topic)
        
        if content:
            combined_content += f"# {topic}\n\n[Read more here]({url})\n\n" + content + "\n\n---\n\n"
        else:
            print(f"Sorry, the topic '{topic}' does not exist on Wikipedia.")
    
    if combined_content:
        filename = 'textbooks/combined_textbook.md'
        with open(filename, 'w') as f:
            f.write(combined_content)
        
        return filename
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topics = request.form['topics'].split(',')
        topics = [topic.strip() for topic in topics]  # Clean up whitespace
        filename = create_textbook(topics)
        
        if filename:
            flash(f"Textbook created successfully! You can find it at: {filename}")
        else:
            flash("No valid content was generated. Please check your topics.")
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)