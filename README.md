# MealPlanAI

Final project for the Building AI course

## Summary

**Building AI course project** — A smart, budget-aware meal recommender that turns what you already have at home into a 7-day plan and a grocery list, minimizing cost and food waste while fitting dietary preferences and time limits.

## Background

Planning meals is hard: we overbuy, forget what’s in the pantry, and waste food. Recipe sites rarely know your prices, pantry, or weekday time limits. **MealPlanAI** plans a week of meals around the ingredients you already have, your budget, diet/allergy rules, and how much time you can spend each day.

## Data and AI techniques

* **Data**

  * Sample recipes (`data/recipes_sample.csv`) with ingredients, tags, and prep time
  * Sample price list (`data/ingredient_prices.csv`) used to estimate missing-item cost
  * User pantry (a simple list in the script for now)
* **Features**

  * Ingredient coverage (how much of a recipe matches your pantry)
  * Estimated new-cost (only items you must buy)
  * Time constraint and simple dietary tags
* **Methods (prototype)**

  * Content-based scoring (pantry–recipe similarity + cost penalty + quick-tag bonus)
  * Greedy constraint selection to fill **7 dinners** under budget & time limits
  * (Roadmap) NLP normalization, embeddings for similarity, collaborative filtering

## How is it used?

1. Set budget, servings, diet/allergy rules, time limit, and pantry in the script.
2. Run the planner to get 7 suggested meals and an estimate of what you need to buy.
3. Edit/accept; iterate weekly.

### Quick start

```bash
# (optional) create a virtual env
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install minimal requirements
pip install -r requirements.txt  # (contains: numpy>=1.24)

# run from the repository root
python3 src/mealplan.py
```

### Configuration (edit at the top of `src/mealplan.py`)

```python
BUDGET = 20.0                 # total weekly budget
SERVINGS = 2                  # (placeholder in prototype)
DIET_TAGS = {"vegetarian": False, "vegan": False, "halal": False}
ALLERGIES = set()             # e.g. {"peanut", "shrimp"}
TIME_PER_DAY = 40             # max minutes per meal
PANTRY = {"rice","egg","garlic","onion","salt","soy sauce","oil"}
```

### Example output

```
=== MealPlanAI (prototype) ===
Budget: 20.00 | Pantry items: 7 | Target days: 7
Chosen meals: 7 | Estimated new-cost: 18.30

1. Fried Rice  (15 min)  new-cost≈ 0.80
   ingredients: rice, egg, garlic, soy sauce, carrot, peas, oil, salt
2. Tomato Pasta  (20 min)  new-cost≈ 2.30
   ingredients: tomato, garlic, onion, pasta, olive oil, salt
...
```

> If the budget/time constraints are too strict, the script will plan fewer than 7 meals and print a note.

## Project structure

```
data/
  recipes_sample.csv
  ingredient_prices.csv
src/
  mealplan.py
README.md
LICENSE
requirements.txt
```

## Challenges

* **Data quality** — ingredient names and units vary; prices are approximate.
* **Safety** — allergen handling should be conservative; always show warnings.
* **Cold start** — without ratings/preferences the plan may be generic.
* **Culture & variety** — avoid bias toward a single cuisine; ensure diversity.
* **Privacy** — pantry and dietary data are personal; store locally or with consent.

## What next?

* Ingredient normalization (NLP), embeddings for robust similarity.
* Real-world price integration (partner APIs or weekly flyers); per-serving scaling.
* “Diversity constraints” to avoid repeating similar meals.
* Feedback loop (ratings/leftovers) and collaborative filtering.
* Simple web UI or mobile app; barcode scanning for pantry.

## Acknowledgments

Sample data crafted for prototyping. Inspired by open recipe datasets and public nutrition tables (e.g., Open Food Facts). Any third-party data/code used in future iterations will be credited here with their respective licenses.

## License

This project is released under the **MIT License** (see `LICENSE`).
