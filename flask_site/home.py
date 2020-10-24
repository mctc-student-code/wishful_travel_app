from states import state_list
from API.wiki_api import get_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_location_coordinates, get_directions
from flask import Blueprint, render_template, request
from flask_site.db import get_db
from helper_functions import restaurant_formatter, direction_formatting, address_getter

# Blueprint is used by __init__.py to import the page renderings into the app
# Also used to set up the url
bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        # request.form is a type of dict mapping
        city = request.form['city'].title()
        state = request.form['state']
        db = get_db()
        error = None

        if not city:
            error = 'City is required'
        elif not state:
            error = 'State is required'

        if error is None:
            #TODO exception handling for data returned from wiki api
            #TODO call to db to check for previous entry before consulting the api
            #TODO when no data is found from wiki api, 'extract' is the only thing returned.
            #TODO urls for restaurants are available in the yelp json data. If there is time consider working links in.
            page_id, page_data = get_city_info(city, state)

            if page_id == 'KeyError':
                return render_template('home/search.html', states=state_list, posts=f'The API was not able to retrieve information \
                    on {city}, {state}.\nPlease check your spelling.'.split())
            elif page_id == 'ConnectionError':
                return render_template('home/search.html', states=state_list, posts=f'A network issue has occurred, \
                    please check your connection.'.split())
            else:
                session_url = get_page_url(page_id)
                posts = get_restaurants_for_location(f'{city},{state}')
                res_list = restaurant_formatter(posts)
                general = get_general_location_coordinates(state,city)
                # address = address_getter(posts)
                end = get_location_coordinates(address_getter(posts),state,general)
                route = get_directions(end)
                directions = direction_formatting(route)
                #TODO the following conditional doesn't work
                if page_id is not False and posts is not None and end is not None:
                    # perfect world rendering. Runs when data is returned correctly.
                    return render_template('home/search.html', states=state_list, posts=page_data.split(), city_name=city, state_name=f', {state}',
                                        hyperlink=session_url, hypertitle='More Info', food=res_list,
                                        res_banner='Top Rated Restaurants', dir_banner='Driving Directions', routes=directions)

                else:
                    # rendering of page when an error occurs in one of the api calls. reports error message to user
                    return render_template('home/search.html', states=state_list, posts=f'{page_data}'.split())

    # works as the base rendering for the page. Only shows the sumbission fields.
    return render_template('home/search.html', states=state_list)
