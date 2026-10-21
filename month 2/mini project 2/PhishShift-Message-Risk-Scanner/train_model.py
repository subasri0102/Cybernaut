import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "Dataset_5971.csv"


def load_dataset():
    data = pd.read_csv(DATASET_PATH, encoding="latin-1")

    data.columns = data.columns.str.strip().str.upper()

    data = data.dropna(subset=["LABEL", "TEXT"]).copy()

    data["LABEL"] = data["LABEL"].str.strip().str.lower()
    data["TEXT"] = data["TEXT"].str.strip()

    data = data[data["TEXT"] != ""]

    data["LABEL"] = data["LABEL"].replace({
        "spam": "spam",
        "smishing": "smishing",
        "ham": "ham"
    })

    data = data.drop_duplicates(subset=["TEXT"], keep="first")

    print("\nCleaned Dataset Shape:", data.shape)

    print("\nStandardized Label Distribution:")
    print(data["LABEL"].value_counts())

    print("\nTotal Messages:", len(data))

    return data
if __name__ == "__main__":
    data = load_dataset()

    from sklearn.model_selection import train_test_split

    data["risk"] = data["LABEL"].apply(
        lambda label: "risky" if label in ["spam", "smishing"] else "safe"
    )

    print("\nRisk Category Distribution:")
    print(data["risk"].value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        data["TEXT"],
        data["risk"],
        test_size=0.2,
        random_state=42,
        stratify=data["risk"]
    )

    print("\nTraining Messages:", len(X_train))
    print("Testing Messages:", len(X_test))
    # Convert text into numerical features
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # Model 1: Logistic Regression
    lr_model = LogisticRegression(class_weight="balanced", max_iter=1000)
    lr_model.fit(X_train_tfidf, y_train)

    # Model 2: Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_tfidf, y_train)

    print("\nBoth ML models trained successfully!")
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        classification_report,
        confusion_matrix
    )

    models = {
        "Logistic Regression": lr_model,
        "Naive Bayes": nb_model
    }

    for name, model in models.items():
        predictions = model.predict(X_test_tfidf)

        print(f"\n{'=' * 40}")
        print(f"Model: {name}")
        print(f"{'=' * 40}")

        print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
        print("Precision:", round(
            precision_score(y_test, predictions, pos_label="risky"), 4
        ))
        print("Recall:", round(
            recall_score(y_test, predictions, pos_label="risky"), 4
        ))
        print("F1 Score:", round(
            f1_score(y_test, predictions, pos_label="risky"), 4
        ))

        print("\nClassification Report:")
        print(classification_report(y_test, predictions))

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, predictions, labels=["safe", "risky"]))
        import re

    def rules_based_detector(message):
        message_lower = message.lower()
        score = 0
        reasons = []

        suspicious_words = [
            "urgent", "verify", "winner", "won",
            "prize", "claim", "free", "click here",
            "password", "account suspended",
            "bank account", "otp", "blocked"
        ]

        for word in suspicious_words:
            if word in message_lower:
                score += 1
                reasons.append(f"Suspicious keyword: {word}")

        urls = re.findall(r"https?://\S+|www\.\S+", message_lower)

        if urls:
            score += 2
            reasons.append("Contains a URL")

        prediction = "risky" if score >= 2 else "safe"

        return prediction, reasons
        # Evaluate Rules-Based Method
    rules_predictions = [
        rules_based_detector(message)[0]
        for message in X_test
    ]

    print("\n" + "=" * 40)
    print("Model: Rules-Based Method")
    print("=" * 40)

    print("Accuracy:", round(
        accuracy_score(y_test, rules_predictions), 4
    ))

    print("Precision:", round(
        precision_score(y_test, rules_predictions, pos_label="risky", zero_division=0), 4
    ))

    print("Recall:", round(
        recall_score(y_test, rules_predictions, pos_label="risky", zero_division=0), 4
    ))

    print("F1 Score:", round(
        f1_score(y_test, rules_predictions, pos_label="risky", zero_division=0), 4
    ))

    print("\nClassification Report:")
    print(classification_report(y_test, rules_predictions, zero_division=0))

    print("Confusion Matrix:")
    print(confusion_matrix(
        y_test, rules_predictions, labels=["safe", "risky"]
    ))
    import joblib

    MODEL_DIR = BASE_DIR / "models"
    MODEL_DIR.mkdir(exist_ok=True)

    joblib.dump(lr_model, MODEL_DIR / "logistic_regression.pkl")
    joblib.dump(tfidf, MODEL_DIR / "tfidf_vectorizer.pkl")

    print("\nLogistic Regression model saved successfully!")
    print("TF-IDF Vectorizer saved successfully!")
