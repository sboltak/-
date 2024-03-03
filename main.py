from flask import Flask, request

import scrapper

from scrapper import getDataset

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Boltak S.V.</h1>'


@app.route('/dataset/<group_id>')
def dataset(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getDataset(group_id,action_update)

@app.route('/sex/<group_id>')
def sex(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getSex(group_id, action_update)

@app.route('/closed/<group_id>')
def closed(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getClosed(group_id, action_update)

@app.route('/country/<group_id>')
def country(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getCountry(group_id, action_update)

@app.route('/city/<group_id>')
def city(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getCity(group_id, action_update)

@app.route('/surname/<group_id>')
def surname(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getSurname(group_id, action_update)

@app.route('/name/<group_id>')
def name(group_id):
    action = request.args.get('action')
    action_update = False
    if action == 'update':
        action_update = True
    return scrapper.getName(group_id, action_update)


if __name__ == '__main__':
    app.run(debug=True)