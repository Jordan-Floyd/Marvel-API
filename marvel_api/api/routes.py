from flask import Blueprint, request, jsonify
from marvel_api.helpers import token_required
from marvel_api.models import Hero, db, hero_schema, heros_schema

api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/heros', methods = ['POST'])
@token_required

def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    superpower = request.json['superpower']
    human_alien = request.json['human_alien']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')
    
    hero = Hero(name, description, superpower, human_alien, user_token = token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)



@api.route('/heros', methods = ['GET'])
@token_required

def get_heros(current_user_token):
    owner = current_user_token.token
    hero = Hero.query.filter_by(user_token = owner).all()
    response = heros_schema.dump(hero)
    return jsonify(response)



@api.route('/heros/<id>', methods = ['GET'])
@token_required

def get_hero(current_user_token, id):
    hero = Hero.query.get(id)
    if hero:
        print(f'This is the Marvel Character: {hero.name}')
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That Character does not exist'})



@api.route('/heros/<id>', methods = ['POST', 'PUT'])
@token_required

def update_hero(current_user_token, id):
    hero = Hero.query.get(id)
    print(hero)
    if hero:
        hero.name = request.json['name']
        hero.description = request.json['description']
        hero.superpower = request.json['superpower']
        hero.human_alien = request.json['human_alien']
        hero.user_token = current_user_token.token

        db.session.commit()
        response = hero_schema.dump(hero)

        return jsonify(response)
    else:
        return jsonify ({'Error': 'That Character does not exist'})



@api.route('/heros/<id>', methods = ['DELETE'])
@token_required

def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    if hero:
        db.session.delete(hero)
        db.session.commit()
        return jsonify({'Success': f'Hero ID #{hero.id} has been deleted'})
    else:
        return jsonify({'Error': 'That Character does not exist'})