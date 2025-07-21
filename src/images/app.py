'''Basic flask app'''
import os

import uuid
from datetime import datetime
from flask import Flask, request, jsonify, flash, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from time import sleep
from pathlib import Path
from werkzeug.utils import secure_filename
from images.image import Picture


UPLOAD_FOLDER = '/home/martyni/repos/images/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unique.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


def allowed_file(filename):
    '''Checks if file extension is present and if file is allowed'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Basic(db.Model):  # pylint: disable=too-few-public-methods
    '''Basic class to hold message data'''
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    file_format = db.Column(db.Text, nullable=False)
    colour = db.Column(db.Boolean, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        '''Return sql data as dict'''
        return {
            "id": self.id,
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "file_fomat": self.file_format,
            "colour": self.colour,
            "url": self.url,
            "date": self.date.isoformat(),
        }


@app.route('/images', methods=['GET'])
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


# @app.route('/basic', methods=['POST'])
def receive_messege(data):
    '''URL for recieving items'''
    # data = request.get_json()
    print(data)
    fields = ["height", "width", "colour", "file_format"]
    good_data = {f: f"{f}" for f in fields}
    for field in fields:
        if not data or field not in data:
            return jsonify({
                'error': f'required {field} missing',
                'recieved': f'{data}',
                'expected': f'{good_data}'}), 400

    new_item = Basic(
        file_format=data.get('file_format'),
        colour=data.get('colour'),
        height=data.get('height'),
        width=data.get('width'),
        url=data.get('url'),
        name=data.get('name'),
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    name = request.args.get("name", "my_guy.jpeg")
    data = '{}'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = os.path.join(UPLOAD_FOLDER, filename)
            other_filename = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            if full_filename != other_filename:
                print(f'full: {full_filename}, other: {other_filename}')
            print(f'full_filename: {full_filename}')
            file.save(full_filename)
            pic = Picture(filename, app.config['UPLOAD_FOLDER'])
            width, height = pic.size()
            data = {
                "file_format": file.filename.split(".", )[-1],
                "width": width,
                "height": height,
                "name": file.filename,
                "url": f'/images/{file.filename}',
                "colour": True
            }
            data = receive_messege(data)[0]

            return redirect(url_for('upload_file', name=filename))
    return f'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <img src="/images/{name}" alt="Italian Trulli">
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/images/<filename>')
def send_report(filename):
    width = request.args.get("width")
    height = request.args.get("height")
    squish = request.args.get("squish")
    new_format = request.args.get("new_format")
    if request.args.get("width") or request.args.get(
            "height") or request.args.get("new_format"):
        filename = secure_filename(filename)
        whole_path = f'{UPLOAD_FOLDER}/{filename}'
        app.logger.info(f'whole_path : {whole_path}')
        resize_picture = Picture(
            filename,
            path=UPLOAD_FOLDER,
            logger=app.logger.info)
        filename = resize_picture.resize(
            width=width,
            height=height,
            squish=squish,
            new_format=new_format)
    app.logger.info(f'looking at {filename}')
    return send_from_directory(UPLOAD_FOLDER, filename)


def main():
    '''Entry point for test container'''
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    main()
