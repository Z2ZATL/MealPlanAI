import csv, math
from collections import defaultdict, Counter
from pathlib import Path

# === user inputs (แก้ได้) ===
BUDGET = 20.0                 # งบรวมทั้งสัปดาห์
SERVINGS = 2                  # จำนวนคน
DIET_TAGS = {"vegetarian": False, "vegan": False, "halal": False}  # ตัวอย่าง flag
ALLERGIES = set()             # เช่น {"peanut", "shrimp"}
TIME_PER_DAY = 40             # นาทีสูงสุดต่อมื้อ
PANTRY = {"rice","egg","garlic","onion","salt","soy sauce","oil"}  # ของที่มีอยู่แล้ว

# paths relative to this file, not current working dir
ROOT = Path(__file__).resolve().parents[1]   # /workspaces/MealPlanAI
RECIPES_CSV = ROOT / "data" / "recipes_sample.csv"
PRICES_CSV  = ROOT / "data" / "ingredient_prices.csv"



def load_recipes(path):
    recipes = []
    with open(path, newline='', encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            ing = [x.strip() for x in row["ingredients"].split(";") if x.strip()]
            tags = set(t.strip() for t in row["tags"].split(";") if t.strip())
            recipes.append({
                "id": int(row["id"]),
                "title": row["title"],
                "tags": tags,
                "time": int(row["time_mins"]),
                "ingredients": ing
            })
    return recipes

def load_prices(path):
    price = {}
    with open(path, newline='', encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            price[row["ingredient"]] = float(row["price"])
    return price

def est_missing_cost(ingredients, prices, pantry):
    # ประเมินค่าใช้จ่ายเฉพาะวัตถุดิบที่ "ไม่มีในครัว"
    cost = 0.0
    for ing in ingredients:
        if ing not in pantry:
            cost += prices.get(ing, 0.8)  # ถ้าไม่ทราบราคา ใส่ประมาณการ 0.8
    return cost

def compatible(recipe):
    # กรองตามเวลา/อาการแพ้/แท็กง่ายๆ
    if recipe["time"] > TIME_PER_DAY:
        return False
    if ANY_ALLERGY := (ALLERGIES & set(recipe["ingredients"])):
        return False
    # ตัวอย่าง: ถ้าเลือก vegetarian จริงๆ ให้ตัดเมนูที่ไม่ใช่ออก
    if DIET_TAGS.get("vegetarian", False):
        animal = {"chicken","beef","salmon","fish sauce"}
        if any(a in recipe["ingredients"] for a in animal):
            return False
    return True

def score_recipe(recipe, prices, pantry):
    # คะแนนพื้นฐาน: สัดส่วนวัตถุดิบที่มีอยู่ + โบนัสแท็กตรงกับ "quick"
    ing = recipe["ingredients"]
    have = len([i for i in ing if i in pantry])
    coverage = have / max(1, len(ing))
    bonus_tag = 0.1 if "quick" in recipe["tags"] else 0.0
    # ลงโทษตามต้นทุนที่ต้องซื้อเพิ่ม (normalize คร่าวๆ)
    cost = est_missing_cost(ing, prices, pantry)
    penalty = cost / 10.0
    return coverage + bonus_tag - penalty, cost

def plan_week(recipes, prices, pantry, budget, days=7):
    # จัดเรียงตามคะแนน แล้วเลือกแบบ greedy ไม่เกินงบ
    scored = []
    for r in recipes:
        if not compatible(r):
            continue
        s, c = score_recipe(r, prices, pantry)
        scored.append((s, c, r))
    scored.sort(reverse=True, key=lambda x: x[0])

    chosen, spend = [], 0.0
    used_titles = set()
    for s, c, r in scored:
        if len(chosen) >= days: break
        if r["title"] in used_titles: 
            continue
        if spend + c <= budget:
            chosen.append((r, c))
            spend += c
            used_titles.add(r["title"])
    return chosen, spend

def main():
    recipes = load_recipes(RECIPES_CSV)
    prices = load_prices(PRICES_CSV)
    chosen, spend = plan_week(recipes, prices, PANTRY, BUDGET)

    print("=== MealPlanAI (prototype) ===")
    print(f"Budget: {BUDGET:.2f} | Pantry items: {len(PANTRY)} | Target days: {7}")
    print(f"Chosen meals: {len(chosen)} | Estimated new-cost: {spend:.2f}\n")
    for i, (r, c) in enumerate(chosen, 1):
        print(f"{i}. {r['title']}  ({r['time']} min)  new-cost≈ {c:.2f}")
        print(f"   ingredients: {', '.join(r['ingredients'])}")
    if len(chosen) < 7:
        print("\nNote: Not enough compatible recipes under budget/time constraints.")

if __name__ == "__main__":
    main()
