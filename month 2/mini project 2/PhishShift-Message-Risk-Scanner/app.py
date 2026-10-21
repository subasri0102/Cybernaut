from flask import Flask, render_template, request
import joblib
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

model = joblib.load(MODEL_DIR / "logistic_regression.pkl")
tfidf = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    message = ""
    result_class = ""

    if request.method == "POST":
        message = request.form.get("message", "").strip()

        if message:
            message_tfidf = tfidf.transform([message])
            result = model.predict(message_tfidf)[0]

            if result == "risky":
                prediction = "Risky Message"
                result_class = "risky"
            else:
                prediction = "Safe Message"
                result_class = "safe"

    return render_template(
        "index.html",
        prediction=prediction,
        message=message,
        result_class=result_class
    )


if __name__ == "__main__":
    app.run(debug=True)
