from flask import jsonify, request
from . import api_blueprint
from backend.models import Group, ItemRequested, Item
from .auth import requires_auth, AuthError
from .. import db
from werkzeug.exceptions import abort, NotFound, MethodNotAllowed, BadRequest, \
    UnprocessableEntity

# Constant for pagination
ITEMS_PER_PAGE = 5


###### READ / GET Group and Item details - ANY USER (No login needed) ######

@api_blueprint.route('/groups')
def get_groups():
    """
    Retrieves all groups from the database, ordered by county,
    then city. Results are paginated in groups of 5. If a request argument
    for page number is not included, page will start at 1.

    :returns 200, list of groups and total number of groups if successful.
    404 if no groups found.
    """
    # returns all group records, ordered by county, then city
    try:
        groups_query = (Group.query.order_by(Group.county, Group.city)
                        .paginate(per_page=ITEMS_PER_PAGE,
                                  page=request.args.get('page', 1, type=int)))

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
        raise NotFound('Groups not found')

# Display details of a particular group and the items requested by that group
@api_blueprint.route('/groups/<int:id>')
def get_group_by_id(id):
    """
    Retrieves the specified group and items requested by that group.

    :param id: Group id

    :returns 200 and group; 404 if not found.
    """
    try:
        group = Group.query.get(id)
        formatted_group = group.format()

        return jsonify(
            {
                'success': True,
                'group': formatted_group,
            }
        )

    except Exception as e:
        print(e)
        raise NotFound('Group not found')


@api_blueprint.route('/group/search', methods=['GET', 'POST'])
def search_by_item():
    """
    Takes a search_term for an item name in the request body and
    returns groups with matching items requested, ordered by county then city.

    :returns
        200 and list of groups or 404 if no groups found
    """
    try:
        body = request.get_json()
        search_term = body.get('search_term')

        # Hoping to add additional functionality - to narrow results by
        # postcode entered and show results ordered by distance
        search_query = (Group.query.filter(Item.name
                                           .ilike('%' + search_term + '%'))
                        .order_by(Group.county, Group.city)).all()

        formatted_groups = [group.format() for group in search_query]

        return jsonify(
            {
                'success': True,
                'groups': formatted_groups,
            }
        )
    except Exception as e:
        print(e)
        raise NotFound('No groups found matching the search term')




#######  UPDATE/PATCH Group contact details - Logged in Admin ######

# Update a group's email.
@api_blueprint.route('/groups/<int:id>', methods=['PATCH'])
@requires_auth('patch:group_email')
def update_group_by_id(jwt, id):
    """
    Updates the email address of the specified group. Requires the
    email details to be supplied in the request body.

    :param jwt: JWT token must have patch:group_email permission
    :param id: Group Id

    :returns 200 and id of updated group, 404 if group not found, 422 if request
         is not valid.
    """

    try:
        # body should contain details to change email
        body = request.get_json()

        update_group = Group.query.get(id)

        try:
            # add further email validation here
            if body.get('email') == "":
                raise ValueError('Empty email')

            # update the email address
            update_group.email = body.get('email')

        except ValueError as e:
            print(e)
            raise UnprocessableEntity(e.args[0])

        # commit changes
        update_group.update()

        return jsonify(
            {
                'id': update_group.id,
                'success': True
            }
        )

    except Exception as e:
        print(e)
        raise NotFound('Group not found')

######  DELETE items - Logged in Group or Admin ######

# change this to delete a requested item
@api_blueprint.route('/group/<int:id>', methods=['DELETE'])
@requires_auth('delete:group_items')
def delete_requested_item_by_id(jwt, id):
    """
    Deletes the specified group's requested item. Requires the item's id in the
    request body.

    :param jwt: Jwt must have delete:group_items permission.
    :param id: Group Id

    :returns: 200 OK and deleted item_id if successful, 422 if request body is
    invalid or 404 if item id not found.
    """
    try:
        try:
            body = request.get_json()
            item_id = body.get('item_id')
            if item_id == "":
                raise ValueError('Empty item_id')

        except ValueError as value_error:
            print(value_error)
            raise BadRequest("item_id is required")

        # need both id's to retrieve the correct item_requested record
        item_requested = ItemRequested.query.get(group_id = id, item_id =
        item_id)

        # delete item and commit
        item_requested.delete()

        return jsonify(
            {
                'success': True,
                'deleted_item': item_id
            }
        )

    except Exception as e:
        print(e)
        raise NotFound('Item not found')

######  CREATE Group - for logged in ADMIN Role only ######
# Group will pass a request via form/email/contact us
# - admin will perform checks and create account details for Group

@api_blueprint.route('/group', methods=['POST'])
@requires_auth('post:group')
def create_item(jwt):
    """
    Create a new group. Requires Group data in the request body.

    :param jwt: Must have post:group permissions.

    :return: 201 if created, 422 if request body cannot be processed,
    400 if request is in any other way invalid.
    """
    try:
        body = request.get_json()
        try:
            new_group = Group(name=body.get('name'),
                              description=body.get('description'),
                              address=body.get('address'),
                              city=body.get('city'),
                              county=body.get('county'),
                              email=body.get('email'))

            # add more validation for empty strings
            # email validation?
            if new_group.address == "":
                raise ValueError("Empty String")

        except ValueError as e:
            print(e)
            raise UnprocessableEntity("Cannot create group with the request "
                                      "data")

        # add group and commit
        new_group.add()

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

    except Exception as e:
        print(e)
        raise BadRequest("Request is not valid")

###### CREATE item_requested - add item to group's requested items - logged in
# group only ######
@api_blueprint.route('/group/<int:id>', methods=['POST'])
@requires_auth('post:group_items')  # must have group owner role
def update_items(jwt, id):
    """
    Adds an item to the specified group. Requires an item_id in the request
    body.

    :param jwt: Jwt must have post:group_items permission.
    :param id: Group Id

    :returns:
        201 and item_id, 404 if item not found, 400 if bad request
    """
    try:
        body = request.get_json()

        item_id = body.get_or_404('item_id')

        item_requested = ItemRequested(group_id=id, item_id=item_id)

        # add item and commit
        item_requested.add()

        return jsonify(
            {
                'success': True,
                'group_id': id,
            }
        ), 201

    except Exception as e:
        print(e)
        raise BadRequest("Request is not valid")


################## ERROR HANDLING  ############################


@api_blueprint.app_errorhandler(NotFound)
def not_found(e):
    """
    Receives the not found error and propagates the response
    """
    return jsonify (
        {
            'success': False,
            "error": NotFound.code,
            "message": e.description,
        }), 404


@api_blueprint.errorhandler(BadRequest)
def bad_request(e):
    """
    Receives the bad request error and propagates the response
    """
    return jsonify({
        "success": False,
        "error": BadRequest.code,
        "message": e.description
    }), 400

@api_blueprint.errorhandler(UnprocessableEntity)
def unprocessable(e):
    """
    Receives the unprocessable error and propagates the response
    """
    return jsonify({
        "success": False,
        "error": UnprocessableEntity.code,
        "message": e.description
    }), 422

@api_blueprint.app_errorhandler(MethodNotAllowed)
def method_not_allowed(e):
    """
    Receives the raised Method Not Allowed error and propagates the response
    """
    return jsonify(
        {
            "success": False,
            "error": MethodNotAllowed.code,
            "message": e.description,
        })

@api_blueprint.errorhandler(AuthError)
def handle_auth_error(e):
    """
    Receives the raised authorization error and propagates the response
    """
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response