from flask import jsonify, request, abort
from flask_sqlalchemy import query

from . import api_blueprint
from backend.models import Group, ItemRequested, Item
from .. import db


ITEMS_PER_PAGE = 10

def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items

################### GET #####################################

# Display all groups, order by county, then city
@api_blueprint.route('/group')
def get_groups():
    # returns a list of groups in db
    query = Group.query.order_by(Group.county, Group.city).all()


    groups = paginate(request, query)

    if len(groups) == 0:
        abort(404)

    else:
        return jsonify(
            {
                'success': True,
                'groups': groups,
                'total_groups': len(query)
            }
        )

# Display details of a particular group and the items requested by that group
@api_blueprint.route('/group/<group_id>')
def get_group_by_id(group_id):
    group = Group.query.get_or_404(group_id)
    formatted_group = group.format()

    return jsonify(
        {
            'success': True,
            'group': formatted_group,
        }
    )

###################### LOGGED IN GROUP - update Items Needed #############################

# Patch Group by adding a new item to group's items_requested field
@api_blueprint.route('/group/<group_id>', methods=['PATCH'])
def update_group_by_id(group_id):
    group = Group.query.get_or_404(group_id)

    # body should contain details to create a new item
    body = request.get_json()

    # Add a method in here that first creates a new item and posts it
    # Get the item_id from the newly created item
    try:
        if 'item_id' in body:
            item_requested = ItemRequested(item_id = body.get('item_id'), group_id = group_id)

            db.session.add(item_requested)
            db.session.commit()

        return jsonify(
            {
                'id': group.id,
                'success': True
            }
        )
    except:
        abort(400)


# change this to delete a requested item
@api_blueprint.route('/group/<group_id>/<item_id>', methods=['DELETE'])
def delete_requested_item_by_id(group_id, item_id):


    # retrieve item requested
    item_requested = ItemRequested(item_id = item_id, group_id = group_id)


    db.session.delete(item_requested)
    db.session.commit()
    db.session.close()



    return jsonify(
        {
            'success': True,
            'deleted_item': item_id
        }
    )


######################  Create Group - for ADMIN Role  ###################

@api_blueprint.route('/group', methods=['POST'])
def create_item():
    body = request.get_json()
    try:
        new_group = Group(name=body.get('name'), description=body.get('description'),
                          address=body.get('address'), city=body.get('city'),
                          county=body.get('county'), email=body.get('email'))

        db.session.add(new_group)
        db.session.commit()

        selection = Group.query.all()
        current_groups = paginate(request, selection)

        return jsonify(
            {
                'success': True,
                'created': new_group.id,
                'groups': current_groups,
                'total_groups': len(current_groups)
            }
        )
    except:
        abort(422)


################## ERROR HANDLING  ############################
# refactor

@api_blueprint.app_errorhandler(404)
def not_found(e):
    return jsonify(
        {
            "success": False,
            "error": 404,
            "message": "Not Found",
        }
    ), 404

@api_blueprint.app_errorhandler(400)
def bad_request(e):
    return jsonify(
        {
            "success": False,
            "error": 400,
            "message": "Bad Request",
        }
    ), 400

@api_blueprint.app_errorhandler(422)
def unprocessable_entity(e):
    return jsonify(
        {
            "success": False,
            "error": 422,
            "message": "Unprocessable entity",
        }
    ), 422
