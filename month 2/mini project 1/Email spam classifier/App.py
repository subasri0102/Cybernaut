from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

data = pd.read_csv("spam.csv", encoding="latin-1")
data = data[["v1", "v2"]]
data.columns = ["label", "message"]

X = data["message"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_tfidf, y)


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    message = ""

    if request.method == "POST":
        message = request.form.get("message", "").strip()

        if message:
            message_tfidf = vectorizer.transform([message])
            prediction = lr_model.predict(message_tfidf)[0]
            result = prediction.upper()

    return render_template(
        "index.html",
        result=result,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
