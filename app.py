from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

app = Flask(__name__)

MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)

collection = client["ev_db"]["vehicles"]


@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    fast = collection.with_options(write_concern=WriteConcern(w=1))
    result = fast.insert_one(request.json)
    return jsonify({"inserted_id": str(result.inserted_id)})


@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    safe = collection.with_options(write_concern=WriteConcern(w="majority"))
    result = safe.insert_one(request.json)
    return jsonify({"inserted_id": str(result.inserted_id)})


@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    tesla_primary = collection.with_options(read_preference=ReadPreference.PRIMARY)
    total_count = tesla_primary.count_documents({"Make": "TESLA"})
    return jsonify({"count": total_count})


@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    bmw_secondary = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    total_count = bmw_secondary.count_documents({"Make": "BMW"})
    return jsonify({"count": total_count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
