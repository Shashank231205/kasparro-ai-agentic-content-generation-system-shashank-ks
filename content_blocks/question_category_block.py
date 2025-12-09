"""
Categorizes user questions into buckets.
This is deterministic and does not call an LLM.
"""

def categorize_questions_block(questions):
    categorized = {
        "Informational": [],
        "Usage": [],
        "Safety": [],
        "Purchase": [],
        "Comparison": []
    }

    for q in questions:
        category = q.category
        if category not in categorized:
            categorized["Informational"].append(q.question)
        else:
            categorized[category].append(q.question)

    faq_items = []
    for cat, qs in categorized.items():
        for q in qs:
            faq_items.append({
                "category": cat,
                "question": q
            })

    return faq_items
