"""module luxapp.py: A Flask app, define endpoints:
    /
    /search
    /obj/<obj_id>
    404
"""
from html import escape
from flask import Flask, request, render_template, jsonify
import requests
from model.database import get_objects_info, summary, label, produced_by, classified_as, information

def check_url_exists(url):
    """_summary_
    Args:
        url (_type_): the url

    Returns:
        bool : whether the url exists or not
    """
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return url
        if response.status_code == 307:
            return url
        return False
    except requests.exceptions.RequestException:
        return False

app = Flask(__name__, template_folder='view')

@app.route('/')
def index():
    """Render the HTML template 'index.html'
    """
    # Render the HTML template
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    """extract the inputs and display search result here
    """
    label = request.args.get('l', '').strip()
    agent = request.args.get('a', '').strip()
    classification = request.args.get('c', '').strip()
    date = request.args.get('d', '').strip()

    if not (label or agent or classification or date):
        return jsonify({"error": "No search terms provided. Please enter some search terms."})

    artworks = get_objects_info(label, agent, classification, date)
    artworks = artworks[:1000]
    results = []
    for artwork in artworks:
        artwork_data = artwork.to_dict()
        # Ensure data is escaped to prevent XSS attacks
        artwork_data = {k: escape(v) if isinstance(v, str) else v for k, v in artwork_data.items()}
        results.append(artwork_data)

    return jsonify(results)

@app.route('/obj', methods=['GET'])
def obj_without_id():
    """handle bad client: missing obj_id
    """
    return render_template("404.html", message="Error: missing object id."), 404

@app.route('/obj/<obj_id>', methods=['GET'])
def object_detail(obj_id):
    """display detailed information of the selected object
    """
    summ = summary(obj_id)
    if summ is None:
        return render_template("404.html", message=f"Error: no object with id {obj_id} exists"), 404

    lbl = label(obj_id)
    prod = produced_by(obj_id)
    img_url = f"https://media.collections.yale.edu/thumbnail/yuag/obj/{obj_id}"

    img_url = check_url_exists(img_url)

    print(img_url)

    classified = classified_as(obj_id)

    references = information(obj_id)

    return render_template("object.html", summary=summ, label=lbl, producers=prod,
                           img_url=img_url, classified_as=classified, references=references)

if __name__ == '__main__':
    app.run(debug=True)
