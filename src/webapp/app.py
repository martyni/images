'''Basic flask app'''
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unique.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

GOOD_DATA = {
    "mandatory": "<mandatory>",
    "optional": "<optional(optional)>",
}


class Basic(db.Model):  # pylint: disable=too-few-public-methods
    '''Basic class to hold message data'''
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    mandatory = db.Column(db.String(100), nullable=False)
    optional = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        '''Return sql data as dict'''
        return {
            "id": self.id,
            "mandatory": self.mandatory,
            "optional": self.optional,
            "date": self.date.isoformat(),
        }


@app.route('/basic', methods=['GET'])
def get_paginated_items():
    '''Return paginated items based on page and per_page values'''
    page = int(request.args.get('page')) if request.args.get('page') else 1
    per_page = int(request.args.get('per_page')
                   ) if request.args.get('per_page') else 5
    items = Basic.query.order_by(Basic.date.desc()) \
        .paginate(page=page,
                  per_page=per_page,
                  error_out=False)
    return jsonify({
        "items": [item.to_dict() for item in items.items],
        "total": items.total,
        "page": items.page,
        "pages": items.pages,
        "next_page": f'/basic?page={ page + 1 }&per_page={ per_page }'
    }), 200


@app.route('/basic', methods=['POST'])
def receive_message():
    '''URL for recieving items'''
    data = request.get_json()
    print(data)

    if not data or 'mandatory' not in data:
        return jsonify({
            'error': 'Invalid input',
            'recieved': f'{data}',
            'expected': f'{GOOD_DATA}'}), 400

    new_item = Basic(
        mandatory=data['mandatory'],
        optional=data.get('optional'))
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201


def main():
    '''Entry point for test container'''
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
