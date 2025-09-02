from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Category, Term

update_bp = Blueprint("update", __name__)


@update_bp.route("/api/admin/lowercase-terms", methods=["POST"])
def lowercase_all_terms():
    session = Session()
    try:
        terms = session.query(Term).all()
        changed = 0
        for term in terms:
            if term.name != term.name.lower():
                term.name = term.name.lower()
                changed += 1
        session.commit()
        return jsonify({"success": True, "changed": changed})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# Adjust path if needed
DB_URL = "sqlite:///categories.db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


@update_bp.route("/api/update-term", methods=["POST"])
def update_term():
    data = request.get_json()
    old_category = data.get("oldCategory")
    old_term = data.get("oldTerm")
    new_category = data.get("newCategory")
    new_term = data.get("newTerm")
    if not (old_category and old_term and new_category and new_term):
        return jsonify({"error": "Missing data"}), 400
    session = Session()
    try:
        # Find or create the new category
        category = session.query(Category).filter_by(name=new_category).first()
        if not category:
            category = Category(name=new_category)
            session.add(category)
            session.commit()
        # Remove old term if it exists
        old_cat = session.query(Category).filter_by(name=old_category).first()
        if old_cat:
            term = (
                session.query(Term)
                .filter_by(name=old_term, category_id=old_cat.id)
                .first()
            )
            if term:
                session.delete(term)
                session.commit()
        # Add new term if not exists
        existing = (
            session.query(Term)
            .filter_by(name=new_term, category_id=category.id)
            .first()
        )
        if not existing:
            session.add(Term(name=new_term, category_id=category.id))
            session.commit()
        return jsonify({"success": True})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@update_bp.route("/api/categories", methods=["GET"])
def get_categories():
    session = Session()
    try:
        categories = session.query(Category).all()
        result = []
        for cat in categories:
            result.append(
                {"name": cat.name, "terms": [term.name for term in cat.terms]}
            )
        return jsonify({"categories": result})
    finally:
        session.close()


@update_bp.route("/api/create-category", methods=["POST"])
def create_category():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing category name"}), 400
    session = Session()
    try:
        if session.query(Category).filter_by(name=name).first():
            return jsonify({"error": "Category already exists"}), 400
        session.add(Category(name=name))
        session.commit()
        return jsonify({"success": True})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@update_bp.route("/api/add-term", methods=["POST"])
def add_term():
    data = request.get_json()
    category_name = data.get("category")
    term = data.get("term")
    if term:
        term = term.lower()
    if not (category_name and term):
        return jsonify({"error": "Missing data"}), 400
    session = Session()
    try:
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404
        if session.query(Term).filter_by(name=term, category_id=category.id).first():
            return jsonify({"error": "Term already exists in this category"}), 400
        session.add(Term(name=term.lower(), category_id=category.id))
        session.commit()
        return jsonify({"success": True})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@update_bp.route("/api/recategorize-term", methods=["POST"])
def recategorize_term():
    data = request.get_json()
    term = data.get("term")
    new_category = data.get("newCategory")
    if not (term and new_category):
        return jsonify({"error": "Missing data"}), 400
    session = Session()
    try:
        # Find the term and its current category
        term_obj = session.query(Term).filter_by(name=term).first()
        if not term_obj:
            return jsonify({"error": "Term not found"}), 404
        category = session.query(Category).filter_by(name=new_category).first()
        if not category:
            category = Category(name=new_category)
            session.add(category)
            session.commit()
        term_obj.category_id = category.id
        session.commit()
        return jsonify({"success": True})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@update_bp.route("/api/rename-category", methods=["POST"])
def rename_category():
    data = request.get_json()
    old_name = data.get("oldName")
    new_name = data.get("newName")
    if not (old_name and new_name):
        return jsonify({"error": "Missing data"}), 400
    session = Session()
    try:
        category = session.query(Category).filter_by(name=old_name).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404
        if session.query(Category).filter_by(name=new_name).first():
            return jsonify({"error": "New category name already exists"}), 400
        category.name = new_name
        session.commit()
        return jsonify({"success": True})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
