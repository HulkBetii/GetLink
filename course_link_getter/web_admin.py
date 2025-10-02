"""
Simple Flask-based admin to manage the catalog JSON (list/add/edit/delete).

Run:
    cd course_link_getter
    python web_admin.py

This app intentionally focuses on core fields and English title for simplicity.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from threading import Lock

from flask import Flask, render_template, request, redirect, url_for, flash


APP_ROOT = Path(__file__).resolve().parent
DATA_PATH = APP_ROOT / "assets" / "catalog.multilingual.json"

app = Flask(__name__)
app.secret_key = "dev-key"  # replace for production
_io_lock = Lock()


def load_catalog() -> Dict[str, Any]:
    with _io_lock:
        if not DATA_PATH.exists():
            return {"categories": [], "courses": []}
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)


def save_catalog(data: Dict[str, Any]) -> None:
    with _io_lock:
        with DATA_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def get_course_by_id(courses: List[Dict[str, Any]], course_id: str) -> Optional[Dict[str, Any]]:
    for c in courses:
        if c.get("id") == course_id:
            return c
    return None


@app.route("/")
def index():
    data = load_catalog()
    courses = data.get("courses", [])
    categories = sorted({(c.get("category"), c.get("subcategory")) for c in courses})
    return render_template("index.html", courses=courses, categories=categories)


# ---------------------- Category Management ----------------------

@app.route("/categories")
def list_categories():
    data = load_catalog()
    cats = data.get("categories", [])
    # normalize to simple structure: name + subcategories list
    normalized = []
    for c in cats:
        name = c.get("name") if isinstance(c, dict) else c
        subs = c.get("subcategories", []) if isinstance(c, dict) else []
        normalized.append({"name": name, "subcategories": subs})
    return render_template("categories.html", categories=normalized)


@app.route("/categories/add", methods=["GET", "POST"])
def add_category():
    data = load_catalog()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Category name is required", "danger")
            return render_template("category_form.html", mode="add", values=request.form)
        # ensure unique
        names = { (c.get("name") if isinstance(c, dict) else c) for c in data.get("categories", []) }
        if name in names:
            flash("Category already exists", "danger")
            return render_template("category_form.html", mode="add", values=request.form)
        data.setdefault("categories", []).append({"name": name, "subcategories": []})
        save_catalog(data)
        flash("Category added", "success")
        return redirect(url_for("list_categories"))
    return render_template("category_form.html", mode="add", values={})


@app.route("/categories/edit/<name>", methods=["GET", "POST"])
def edit_category(name: str):
    data = load_catalog()
    cats = data.get("categories", [])
    cat = None
    for c in cats:
        n = c.get("name") if isinstance(c, dict) else c
        if n == name:
            cat = c
            break
    if not cat:
        flash("Category not found", "danger")
        return redirect(url_for("list_categories"))

    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        subs_raw = request.form.get("subcategories", "")
        subs = [s.strip() for s in subs_raw.split(",") if s.strip()]
        if not new_name:
            flash("Category name is required", "danger")
            return render_template("category_form.html", mode="edit", values=request.form, original=name)
        # update cat
        cat["name"] = new_name
        cat["subcategories"] = subs
        # update courses referencing the old name
        for course in data.get("courses", []):
            if course.get("category") == name:
                course["category"] = new_name
                # if current subcategory not in list anymore, keep as-is (user can adjust later)
        save_catalog(data)
        flash("Category updated", "success")
        return redirect(url_for("list_categories"))

    initial = {
        "name": cat.get("name") if isinstance(cat, dict) else cat,
        "subcategories": ", ".join(cat.get("subcategories", [])) if isinstance(cat, dict) else "",
    }
    return render_template("category_form.html", mode="edit", values=initial, original=name)


@app.post("/categories/delete/<name>")
def delete_category(name: str):
    data = load_catalog()
    cats = data.get("categories", [])
    new_cats = []
    for c in cats:
        n = c.get("name") if isinstance(c, dict) else c
        if n != name:
            new_cats.append(c)
    data["categories"] = new_cats
    # cascade: remove courses in this category
    data["courses"] = [cr for cr in data.get("courses", []) if cr.get("category") != name]
    save_catalog(data)
    flash("Category deleted (and its courses)", "success")
    return redirect(url_for("list_categories"))


def _next_id(existing: List[Dict[str, Any]]) -> str:
    """Generate a simple auto-increment id like c-0001, c-0002."""
    prefix = "c-"
    max_num = 0
    for c in existing:
        cid = str(c.get("id", ""))
        if cid.startswith(prefix):
            try:
                max_num = max(max_num, int(cid.split("-", 1)[1]))
            except Exception:
                continue
    return f"{prefix}{max_num + 1:04d}"


@app.route("/add", methods=["GET", "POST"])
def add_course():
    data = load_catalog()
    categories = data.get("categories", [])

    if request.method == "POST":
        # ID is auto-generated
        title_en = request.form.get("title_en", "").strip()
        category = request.form.get("category", "").strip()
        subcategory = request.form.get("subcategory", "").strip()
        provider = request.form.get("provider", "").strip() or None
        link = request.form.get("link", "").strip()
        raw_tags = request.form.get("tags", "")
        tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
        if not tags_list:
            tags_list = ["en", "vi", "es", "de", "it", "pt", "ja", "ko", "zh", "fr"]
        tags: Optional[List[str]] = tags_list

        if not title_en or not category or not subcategory or not link:
            flash("Please fill required fields (title, category, subcategory, link)", "danger")
            return render_template("form.html", mode="add", categories=categories, values=request.form)

        # Generate new id
        course_id = _next_id(data.get("courses", []))

        new_course = {
            "id": course_id,
            "title": {"en": title_en},
            "category": category,
            "subcategory": subcategory,
            "provider": provider,
            "link": link,
            "tags": tags,
        }
        data.setdefault("courses", []).append(new_course)
        save_catalog(data)
        flash("Course added", "success")
        return redirect(url_for("index"))

    return render_template("form.html", mode="add", categories=categories, values={})


@app.route("/edit/<course_id>", methods=["GET", "POST"])
def edit_course(course_id: str):
    data = load_catalog()
    categories = data.get("categories", [])
    course = get_course_by_id(data.get("courses", []), course_id)
    if not course:
        flash("Course not found", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title_en = request.form.get("title_en", "").strip()
        category = request.form.get("category", "").strip()
        subcategory = request.form.get("subcategory", "").strip()
        provider = request.form.get("provider", "").strip() or None
        link = request.form.get("link", "").strip()
        raw_tags = request.form.get("tags", "")
        tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
        tags: Optional[List[str]] = tags_list if tags_list else None

        if not title_en or not category or not subcategory or not link:
            flash("Please fill required fields (title, category, subcategory, link)", "danger")
            return render_template("form.html", mode="edit", categories=categories, values=request.form, course_id=course_id)

        # Update fields
        title = course.get("title")
        if isinstance(title, dict):
            title["en"] = title_en
        else:
            course["title"] = {"en": title_en}

        course["category"] = category
        course["subcategory"] = subcategory
        course["provider"] = provider
        course["link"] = link
        course["tags"] = tags

        save_catalog(data)
        flash("Course updated", "success")
        return redirect(url_for("index"))

    # Prepare initial values for the form
    initial = {
        "id": course.get("id", ""),
        "title_en": (course.get("title", {}) or {}).get("en") if isinstance(course.get("title"), dict) else course.get("title", ""),
        "category": course.get("category", ""),
        "subcategory": course.get("subcategory", ""),
        "provider": course.get("provider", ""),
        "link": course.get("link", ""),
        "tags": ", ".join(course.get("tags", [])),
    }
    return render_template("form.html", mode="edit", categories=categories, values=initial, course_id=course_id)


@app.post("/delete/<course_id>")
def delete_course(course_id: str):
    data = load_catalog()
    courses = data.get("courses", [])
    new_courses = [c for c in courses if c.get("id") != course_id]
    if len(new_courses) == len(courses):
        flash("Course not found", "warning")
    else:
        data["courses"] = new_courses
        save_catalog(data)
        flash("Course deleted", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=8082)


