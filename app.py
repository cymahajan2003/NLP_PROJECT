from flask import Flask, render_template, request
from Backend.agri import SearchEngine

app=Flask(__name__, template_folder="Frontend", static_folder="Frontend")

search_engine = SearchEngine()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method=="POST":
        query=request.form["query"]
        results=search_engine.search(query)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)



