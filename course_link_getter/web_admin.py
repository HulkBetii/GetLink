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


@app.route("/add", methods=["GET", "POST"])
def add_course():
    data = load_catalog()
    categories = data.get("categories", [])

    if request.method == "POST":
        course_id = request.form.get("id", "").strip()
        title_en = request.form.get("title_en", "").strip()
        category = request.form.get("category", "").strip()
        subcategory = request.form.get("subcategory", "").strip()
        provider = request.form.get("provider", "").strip()
        link = request.form.get("link", "").strip()
        tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]

        if not course_id or not title_en or not category or not subcategory or not link:
            flash("Please fill required fields (id, title, category, subcategory, link)", "danger")
            return render_template("form.html", mode="add", categories=categories, values=request.form)

        if get_course_by_id(data.get("courses", []), course_id):
            flash("ID already exists", "danger")
            return render_template("form.html", mode="add", categories=categories, values=request.form)

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
        provider = request.form.get("provider", "").strip()
        link = request.form.get("link", "").strip()
        tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]

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


