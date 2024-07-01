from urllib.parse import urlparse, parse_qs
from ingresso_nuker.config import API_URL, CITY, EVENT, HEADERS, PARAMS
from ingresso_nuker.utils import get_session, make_request, requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngressoNuker:
    def __init__(self):
        self.session = get_session()

    def fetch_sessions(self):
        url = f'https://api-content.ingresso.com/v0/sessions/city/{CITY}/event/{EVENT}/partnership/home/groupBy/sessionType'
        response = make_request(self.session, url, PARAMS, HEADERS)
        return response.json()

    def get_checkout_url_and_time(self, theater):
        for session in theater['sessionTypes'][0]['sessions']:
            yield session['siteURL'], session['time']

    def extract_session_id(self, checkout_url):
        parsed_url = urlparse(checkout_url)
        return parse_qs(parsed_url.query)['sessionId'][0]

    def create_cart(self):
        url = f'{API_URL}/carts/?origin=Mobile&newCheckout=true'
        response = make_request(self.session, url, None, HEADERS, method='post')
        return response.json()['id']

    def add_session_to_cart(self, cart_id, session_id):
        url = f'{API_URL}/carts/{cart_id}/sessions/{session_id}'
        response = make_request(self.session, url, {'partnership': 'home'}, HEADERS, method='post', json_data={'headers': None})
        return response.json()

    def get_section_id(self, session_response):
        return session_response['sessions'][0]['sections'][0]['id']

    def fetch_seats(self, session_id, section_id):
        url = f'{API_URL}/sessions/{session_id}/sections/{section_id}/seats'
        response = make_request(self.session, url, PARAMS, HEADERS)
        return response.json()

    def select_seats(self, seats_response):
        seats = []
        # you can only purchase a maximum of 8 tickets at a time
        for line in seats_response['lines']:

            if len(seats) >= 8: break

            for seat in line['seats']:
                if 'Available' not in seat['status']: continue
                
                if len(seats) >= 8: break

                seats.append(seat)
        return seats

    def add_seats_to_cart(self, cart_id, session_id, section_id, seats):
        url = f'{API_URL}/carts/{cart_id}/sessions/{session_id}/sections/{section_id}/seats'
        make_request(self.session, url, None, HEADERS, method='post', json_data={'seats': seats})

def main():
    nuker = IngressoNuker()
    response = nuker.fetch_sessions()
    theater = response[0]['theaters'][0]
    
    for checkout_url, time in nuker.get_checkout_url_and_time(theater):
        logger.info(f'checkout url: {checkout_url} | session time: {time}')
        session_id = nuker.extract_session_id(checkout_url)

        while True:
            try:
                cart_id = nuker.create_cart()
                session_response = nuker.add_session_to_cart(cart_id, session_id)
                section_id = nuker.get_section_id(session_response)
                seats_response = nuker.fetch_seats(session_id, section_id)
                seats = nuker.select_seats(seats_response)

                if not seats:
                    logger.info('no available seats, bye.')
                    break

                nuker.add_seats_to_cart(cart_id, session_id, section_id, seats)
            except requests.RequestException as e:
                logger.error(f'an error occurred: {e}')
                break

if __name__ == '__main__':
    main()