from flask import Flask, jsonify, render_template, request, Blueprint, current_app
from model import *
from datetime import datetime
from urllib.parse import urlparse

#region Fetchers
fetchers = Blueprint('fetchers',__name__, static_folder='static')
@fetchers.route('/urls', methods=['GET'])
def get_all_urls():
    urls = Url.query.all()
    result = []
    for url in urls:
        url_data = {}
        url_data['id'] = url.id
        url_data['url'] = url.url
        url_data['date'] = url.date.timestamp()
        url_data['read_status'] = url.read_status
        result.append(url_data)
    return jsonify(result)

@fetchers.route('/urls/<int:url_id>', methods=['GET'])
def get_url_by_id(url_id):
    url = Url.query.filter_by(id=url_id).first()
    if url:
        url_data = {}
        url_data['id'] = url.id
        url_data['url'] = url.url
        url_data['date'] = url.date.timestamp()
        url_data['read_status'] = url.read_status
        return jsonify(url_data)
    else:
        return jsonify({'message': 'URL not found'}), 404

@fetchers.route('/rest_test', methods=['GET'])
def rest_test():
    return render_template('RESTtester.html')

@fetchers.route('/readlater', methods=['GET'])
def readlater():
    return render_template('readlater.html')

@fetchers.route('/last_modified', methods=['GET'])
def get_last_modified():
    try:
        info = Info.query.get(0)
        if info:
            data = {}
            data['last_modified'] = info.last_modified
            return jsonify(data)
        else:
            return jsonify({'message': 'DB has never been modified'}), 500
    except:
        return jsonify({'message': 'DB has never been modified'}), 500
    
#endregion

#region Define modifier routes
modifiers = Blueprint('modifiers',__name__, static_folder='static')
@modifiers.route('/', methods=['GET', 'POST'])
def index():
    return render_template('readlater.html')

@modifiers.after_request
def after_request(resp):
    update_last_updated()
    return resp

@modifiers.route('/add', methods=['POST'])
def add_url():
    try: 
        url = request.json['url']
        new_url = Url(url=url, date=datetime.now(), read_status=False)
        if(is_valid_url(new_url.url)):
            db.session.add(new_url)
            db.session.commit()
            return jsonify({'success': True})
        else:
            db.session.rollback()
            raise ValueError("{%s} is not valid" % new_url.url)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
    
@modifiers.route('/mark/<int:url_id>', methods=['POST'])
def mark_as_read(url_id):
    try:
        url = Url.query.get(url_id)
        url.read_status = not url.read_status
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@modifiers.route('/urls/<int:url_id>', methods=['DELETE'])
def delete_url(url_id):
    url = Url.query.filter_by(id=url_id).first()
    if url:
        db.session.delete(url)
        db.session.commit()
        return jsonify({'message': 'URL deleted successfully'})
    else:
        return jsonify({'message': 'URL not found'}), 404

@modifiers.route('/truncate', methods=['DELETE'])
def truncate_url():
    try:
        rows = db.session.query(Url).delete()
        db.session.commit()
        current_app.logger.info("%r deleted..." % rows)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        return jsonify({'message': 'Internal Server Error'}), 500
    return jsonify({'message': 'Table Truncated successfully'})
#endregion

# region Helper functions
def update_last_updated():
    # Check if update DB tbl has value, if add it
    try:
        info = Info.query.get(0)
        if not info:
            db.session.add(Info(id=0,last_modified=datetime.now()))
            db.session.commit()
        else:
            info.last_modified = datetime.now()
            db.session.commit()
    except Exception as e:
        print(str(e))

def is_valid_url(input):
    """
    Returns True if the input string is a valid URL, False otherwise.
    A valid URL is one  parsed by urlparse and has a recognised scheme and host+port
    """
    try:
        result = urlparse(input)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
#endregion

