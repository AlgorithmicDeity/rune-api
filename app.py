from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

# Load all 24 runes from your detailed JSON file
with open('runes_detailed_full.json', 'r', encoding='utf-8') as f:
    runes = json.load(f)

# Keywords mapped to focus types
KEYWORDS = {
    "emotional_spiritual_meaning": ["feel", "grief", "love", "sad", "heal", "heart", "intuition", "peace"],
    "shadow_aspect": ["block", "fear", "trauma", "pain", "anger", "avoid", "wound", "resist"],
    "material_meaning": ["job", "career", "money", "move", "house", "physical", "work", "health"],
    "light_aspect": ["strength", "success", "blessing", "help", "support", "power", "growth"]
}

# Analyze question to determine focus
def determine_focus(question):
    lower = question.lower()
    for focus, words in KEYWORDS.items():
        if any(word in lower for word in words):
            return focus
    return "essence_summary"

# /cast endpoint to return rune reading
@app.route('/cast', methods=['GET'])
def cast_runes():
    n = int(request.args.get("n", 3))
    question = request.args.get("question", "What do I need to know?").strip()
    focus = determine_focus(question)

    drawn_runes = random.sample(runes, min(n, len(runes)))
    spread_positions = ["past", "present", "future", "above", "below", "within", "without"]

    cards = []
    for i, rune in enumerate(drawn_runes):
        cards.append({
            "name": rune["name"],
            "meaning": rune.get(focus, rune["essence_summary"]),
            "spread_position": spread_positions[i % len(spread_positions)],
            "element": rune["elemental_force"],
            "deity": rune["deity_connection"]
        })

    names = ', '.join(card["name"] for card in cards)
    final_summary = (
        f"In response to your question: '{question}', "
        f"the runes {names} have emerged. This reading focuses on your "
        f"{focus.replace('_', ' ')} — inviting you to reflect on each message within the current of your life."
    )

    return jsonify({
        "question": question,
        "focus": focus,
        "cards": cards,
        "final_summary": final_summary
    })

if __name__ == "__main__":
    app.run()
