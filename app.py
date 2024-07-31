"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

# configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "s3cr3tk3y"

connect_db(app)

@app.route('/')
def root():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """List all cupcakes"""
    cupcakes = Cupcake.query.all()
    return jsonify(cupcakes=[cupcake.serialize() for cupcake in cupcakes])

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data on specific cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake instance"""
    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake=new_cupcake.serialize()), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake instance"""
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake instance"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")