from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier
import numpy as np

app = Flask(__name__)

# If-else rules for detailed breakdown
def get_breakdown(age, skin_type, primary_concern, secondary_concerns, sunscreen, cleansing, diet, sleep):
    age = int(age)
    breakdown = f"Your skin is {skin_type.lower()}"

    if skin_type == "Oily":
        breakdown += ", especially in the T-zone"
    elif skin_type == "Dry":
        breakdown += ", prone to tightness"
    elif skin_type == "Combination":
        breakdown += ", with mixed oily and dry areas"

    if primary_concern != "None":
        breakdown += f", with mild {primary_concern.lower()}"
        if primary_concern == "Acne":
            breakdown += " on the cheeks"
        elif primary_concern == "Redness":
            breakdown += " around sensitive areas"

    if secondary_concerns:
        concerns = ", ".join(secondary_concerns).lower()
        breakdown += f" and occasional {concerns}"

    if diet == "High sugar/fat":
        breakdown += ", likely triggered by a high-sugar diet"
    elif diet == "Balanced":
        breakdown += ", supported by a balanced diet"

    if cleansing == "Once daily":
        breakdown += ". Cleansing once daily may cause clogged pores"
    elif cleansing == "Less often":
        breakdown += ". Infrequent cleansing may lead to buildup"
    else:
        breakdown += ". Regular cleansing helps balance your skin"

    if sunscreen == "Rarely/never":
        breakdown += ", worsened by minimal sun protection"
    elif sunscreen == "Daily":
        breakdown += ", protected by daily sunscreen"

    if sleep == "Less than 5 hours":
        breakdown += ". Poor sleep may increase stress-related issues"
    else:
        breakdown += ". Stable sleep supports skin health"

    return breakdown + "."

# Fake data for classifier
def train_classifier():
    X = [
        [20, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0],
        [30, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [25, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [22, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0],
        [28, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [20, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 2, 0],
        [35, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [24, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [27, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [21, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 2, 0],
        [29, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [23, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0],
        [31, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [26, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
        [19, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0]
    ]
    y = [
        "Acne Routine", "Dry Routine", "Combo Routine", "Acne Routine", "Normal Routine",
        "Acne Routine", "Dry Routine", "Combo Routine", "Normal Routine", "Acne Routine",
        "Dry Routine", "Acne Routine", "Normal Routine", "Combo Routine", "Acne Routine"
    ]
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    return clf

classifier = train_classifier()

# Routine mapping
routines = {
    "Acne Routine": [
        "Cleanse with a foaming cleanser (Product: CeraVe Foaming Cleanser)",
        "Treat with a targeted solution (Product: Neutrogena On-the-Spot Acne Treatment)",
        "Moisturize with a lightweight gel (Product: Clinique Moisture Surge)",
        "Protect with sunscreen (Product: La Roche-Posay Anthelios SPF 50)"
    ],
    "Dry Routine": [
        "Cleanse with a hydrating cleanser (Product: CeraVe Hydrating Cleanser)",
        "Apply a nourishing serum (Product: Paula's Choice Hyaluronic Acid Booster)",
        "Moisturize with a rich cream (Product: Cetaphil Moisturizing Cream)",
        "Protect with sunscreen (Product: Neutrogena Hydro Boost SPF 30)"
    ],
    "Combo Routine": [
        "Cleanse with a gentle cleanser (Product: CeraVe Hydrating Cleanser)",
        "Balance with a light toner (Product: Paula's Choice Skin Balancing Toner)",
        "Moisturize with a gel-cream (Product: Neutrogena Hydro Boost Gel-Cream)",
        "Protect with sunscreen (Product: La Roche-Posay Anthelios SPF 50)"
    ],
    "Normal Routine": [
        "Cleanse with a mild cleanser (Product: Cetaphil Gentle Skin Cleanser)",
        "Hydrate with a light lotion (Product: Clinique Dramatically Different Lotion)",
        "Moisturize with a balanced cream (Product: CeraVe Daily Moisturizing Lotion)",
        "Protect with sunscreen (Product: Neutrogena Ultra Sheer SPF 45)"
    ]
}

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/quiz")
def quiz():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    age = request.form["age"]
    skin_type = request.form["skin_type"]
    primary_concern = request.form["primary_concern"]
    secondary_concerns = request.form.getlist("secondary_concerns")
    # If "None" is selected, treat as no secondary concerns
    if "None" in secondary_concerns:
        secondary_concerns = []
    sunscreen = request.form["sunscreen"]
    cleansing = request.form["cleansing"]
    diet = request.form["diet"]
    sleep = request.form["sleep"]

    breakdown = get_breakdown(age, skin_type, primary_concern, secondary_concerns, sunscreen, cleansing, diet, sleep)
    features = [
        int(age),
        1 if skin_type == "Oily" else 0,
        1 if skin_type == "Dry" else 0,
        1 if skin_type == "Combination" else 0,
        1 if skin_type == "Normal" else 0,
        1 if primary_concern == "Acne" else 0,
        1 if primary_concern == "Dryness" else 0,
        1 if primary_concern == "Redness" else 0,
        1 if primary_concern == "Wrinkles" else 0,
        1 if "Acne" in secondary_concerns else 0,
        1 if "Redness" in secondary_concerns else 0,
        1 if "Dryness" in secondary_concerns else 0,
        1 if "Wrinkles" in secondary_concerns else 0,
        1 if sunscreen == "Daily" else 0,
        1 if sunscreen == "Sometimes" else 0,
        2 if cleansing == "Twice daily" else 1 if cleansing == "Once daily" else 0,
        1 if diet == "High sugar/fat" else 0,
        2 if sleep == "7+ hours" else 1 if sleep == "5-7 hours" else 0
    ]
    routine_label = classifier.predict([features])[0]
    routine = routines[routine_label]

    return render_template("result.html", breakdown=breakdown, routine=routine)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tips")
def tips():
    return render_template("tips.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)