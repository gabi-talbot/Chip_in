from crypt import methods

from flask import jsonify, request, abort
from flask_sqlalchemy import query

from . import api_blueprint
from backend.models import Group, ItemRequested, Item
from .. import db

# Constant for pagination
ITEMS_PER_PAGE = 5


###### READ / GET Group and Item details - ANY USER (No login needed) ######


@api_blueprint.route('/group')
def get_groups():
    """
    Retrieves all groups from the database, ordered by county,
    then city. Results are paginated in groups of 5. If a request argument
    for page number is not included page will start at 1.

    Returns:
        List of groups or 404 if not found.
    """
    # returns all group records, ordered by county, then city
    try:
        groups_query = (Group.query.order_by(Group.county, Group.city)
                 .paginate(per_page=ITEMS_PER_PAGE, page=request.args.get(
            'page', 1, type=int)))

        # format items in paginate object
        groups = [group.format() for group in groups_query.items]

        return jsonify(
            {
                'success': True,
                'groups': groups,
                'total_groups': groups_query.total,
            }
        )
    except Exception as e:
        print(e)
        abort(404)

# Display details of a particular group and the items requested by that group
@api_blueprint.route('/group/<int:id>')
def get_group_by_id(id):
    """
    Retrieves a group from the database using the query parameter 'id'.

    Returns:
        Group object or 404 if not found.
    """

    group = Group.query.get_or_404(id)

    try:
        formatted_group = group.format()

        return jsonify(
            {
                'success': True,
                'group': formatted_group,
            }
        )
    except Exception as e:
        print(e)
        abort(404)

# search for a group by search term
@api_blueprint.route('/group/search', methods=['GET', 'POST'])
def search_by_area():
    """
    Takes a search_term for an item name in the request body and
    returns groups with matching items requested, ordered by county then city.

    Returns:
        Returns a list of groups or 404 if no groups found
    """
    try:
        body = request.get_json()
        search_term = body.get('search_term')


        # plan to change this to search for items requested based on a postcode
        # supplied by the json body - show results ordered by distance
        search_query = (Group.query.filter_by(Group.items_requested.item.name
                        .ilike('%' + search_term + '%'))
                        .order_by(Group.county, Group.city)
                        .all())

        if len(search_query) == 0:
            abort(404)

        formatted_groups = [group.format() for group in search_query]

        return jsonify(
            {
                'success': True,
                'groups': formatted_groups,
            }
        )
    except Exception as e:
        print(e)
        abort(422)




#######  UPDATE/PATCH Group contact details - Logged in Group or Admin ######

# Patch group's email (maybe add tel number if time)
@api_blueprint.route('/group/<int:id>', methods=['PATCH'])
def update_group_by_id(id):
    """
    Updates a group's email by query parameter 'id'. Requires the
    email details to be supplied in the request body.

    Returns:
         Id of updated group, 404 if group not found, 422 if request field is
        not valid.
    """

    try:
        # body should contain details to change email
        body = request.get_json()

        update_group = Group.query.get_or_404(id)

        try:
            update_group.email = body.get('email')

            # add further email validation here
            if update_group.email == "":
                raise ValueError('Empty email')
        except ValueError as e:
            print(e)
            abort(422)

        db.session.commit()

        return jsonify(
            {
                'id': update_group.id,
                'success': True
            }
        )
    # Also add server error here? - 500
    except Exception as e:
        abort(400)

######  DELETE items - Logged in Group or Admin ######

# change this to delete a requested item
@api_blueprint.route('/group/<int: id>', methods=['DELETE'])
def delete_requested_item_by_id(id):
    """

    :param id:
    :return:
    """
    try:
        try:
            body = request.get_json()
            item_id = body.get('item_id')
            if item_id == "":
                raise ValueError('Empty item_id')
        except ValueError as value_error:
            print(value_error)

        # need both id's to retrieve the correct item_requested record
        item_requested = ItemRequested.query.get_or_404(group_id = id,
                                                        item_id = item_id)

        db.session.delete(item_requested)
        db.session.commit()
        db.session.close()


        return jsonify(
            {
                'success': True,
                'deleted_item': item_id
            }
        )
    except Exception as e:
        print(e)
        abort(500)

######  CREATE Group - for logged in ADMIN Role only ######
# Group will pass a request via form/email/contact us
# - admin will perform checks and create account details for Group

######### May change this to just create item for logged in group and have the
# other ROLE as just user
@api_blueprint.route('/group', methods=['POST'])
def create_item():
    body = request.get_json()
    try:
        try:
            new_group = Group(name=body.get('name'),
                              description=body.get('description'),
                              address=body.get('address'),
                              city=body.get('city'),
                              county=body.get('county'),
                              email=body.get('email'))

            # add more validation empty string here, as needed
            # email validation?
            if new_group.address == "":
                raise ValueError("Empty String")

        except ValueError as e:
            print(e)
            abort(422)

        db.session.add(new_group)
        db.session.commit()

        query = Group.query.paginate(per_page=ITEMS_PER_PAGE,
                                         page=request.args.get(
                                            'page', 1, type=int))

        groups =[group.format for group in query.items]

        return jsonify(
            {
                'success': True,
                'created': new_group.id,
                'groups': groups,
                'total_groups': query.total,
            }
        ), 201
    # repetition?
    except ValueError as value_error:
        print(value_error)
        abort(422)
        # Server error?
    except Exception as e:
        print(e)
        abort(500)

###### CREATE item_requested - add item to group's requested items - logged in
# group only ######
@api_blueprint.route('/group/<int:id>', methods=['POST'])
def update_items(id):
    try:
        body = request.get_json()

        item_id = body.get('item_id')

        item_requested = ItemRequested(group_id=id, item_id=item_id)
        db.session.add(item_requested)
        db.session.commit()
        db.session.close()

        return jsonify(
            {
                'success': True,
                'group_id': id,
            }
        )
    except Exception as e:
        print(e)
        abort(404)


################## ERROR HANDLING  ############################
# refactor - see WERKZEUG DOCS

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
