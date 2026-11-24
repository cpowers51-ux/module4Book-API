from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "Welcome to the Book API!"

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    book = Book(
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )


    db.session.add(book)
    db.session.commit()

    return jsonify({"message": "Book added successfully!"}), 201


@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    output = []

    for book in books:
        book_data = {
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "publisher": book.publisher
        }
        output.append(book_data)

    return jsonify(output)

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = db.get_or_404(Book, id)
    data = request.get_json()

    book.book_name = data["book_name"]
    book.author = data["author"]
    book.publisher = data["publisher"]

    db.session.commit()

    return jsonify({"message":"Book updated successfully!"})

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = db.get_or_404(Book, id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)