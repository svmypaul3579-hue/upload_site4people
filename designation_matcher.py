import pandas as pd
from sentence_transformers import SentenceTransformer, util

df = pd.read_csv("designations.csv")
skil_cat = pd.read_csv("Wo_Skill_Categories.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")


def find_best_match(skills, values):
    skills_text = ", ".join(skills)

    skill_embedding = model.encode(
        skills_text,
        convert_to_tensor=True
    )

    value_embeddings = model.encode(
        values,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        skill_embedding,
        value_embeddings
    )[0]

    best_index = scores.argmax().item()

    return values[best_index], float(scores[best_index])


def find_best_designation_and_category(skills):

    # -----------------------------
    # Designations
    # -----------------------------
    designation_df = df[
        ["designation", "value"]
    ].dropna(subset=["designation"])

    designation_df["designation"] = (
        designation_df["designation"]
        .astype(str)
        .str.strip()
    )

    designations = designation_df["designation"].tolist()

    # -----------------------------
    # Skill Categories
    # -----------------------------
    category_df = skil_cat[
        ["id", "name"]
    ].dropna(subset=["name"])

    category_df["name"] = (
        category_df["name"]
        .astype(str)
        .str.strip()
    )

    categories = category_df["name"].unique().tolist()

    # -----------------------------
    # Best Designation
    # -----------------------------
    best_designation, designation_score = find_best_match(
        skills,
        designations
    )

    # Get value belonging to designation
    matched_row = designation_df[
        designation_df["designation"] == best_designation
    ]

    if not matched_row.empty:
        designation_value = str(matched_row.iloc[0]["value"])
    else:
        designation_value = None

    # -----------------------------
    # Best Skill Category
    # -----------------------------
    best_category, category_score = find_best_match(
        skills,
        categories
    )

    # Get ID belonging to category
    matched_skill_row = category_df[
        category_df["name"] == best_category
    ]

    if not matched_skill_row.empty:
        skill_id = str(matched_skill_row.iloc[0]["id"])
    else:
        skill_id = None

    # -----------------------------
    # Result
    # -----------------------------
    return {
        "designation": best_designation,
        "designation_value": designation_value,
        "designation_score": designation_score,
        "skill_category": best_category,
        "category_score": category_score,
        "skill_category_id": skill_id
    }


skills = [
    "Business Development & Sales",
    "Lead Generation",
    "Client Acquisition",
    "Account Management",
    "Proposal Preparation",
    "Commercial Negotiation",
    "Relationship Management"
]

# result = find_best_designation_and_category(skills)

# print(result)