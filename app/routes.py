from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Donation

main = Blueprint("main", __name__)

@main.route("/signup", methods=["POST"])
def signup():
    data = request.json
    user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@main.route("/donate", methods=["POST"])
def donate():
    data = request.json
    donation = Donation(user_id=data["user_id"], amount=data["amount"], message=data["message"])
    db.session.add(donation)
    db.session.commit()
    return jsonify({"message": "Donation received"}), 201

@main.route("/donations", methods=["GET"])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{"user_id": d.user_id, "amount": d.amount, "message": d.message} for d in donations])
