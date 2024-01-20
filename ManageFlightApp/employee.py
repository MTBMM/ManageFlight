from flask import render_template,\
    request, session, jsonify, url_for, redirect, send_file
from ManageFlightApp import UtilsEmployee, utils, app, keys
# from twilio.rest import Client
from io import BytesIO
from reportlab.pdfgen import canvas
import stripe


def index_employee():
    return render_template("employee/index.html")


def submit_airplane():
    messg = ""
    if request.method == "POST":

        airports = {}
        for i in range(1, session["airplane"]["quantity_airport"] + 1):
            id = str(i)
            airport = request.form["airport" + str(i)]
            time_delay_min = request.form["time_delay_min" + str(i)]
            time_delay_max = request.form["time_delay_max" + str(i)]
            arr_date = request.form["arr_date" + str(i)]
            airports[id] = {
                "airport": airport,
                "time_delay_min": time_delay_min,
                "time_delay_max": time_delay_max,
                "arr_date":  arr_date
            }

        try:

            UtilsEmployee.update_flight(airports=airports,  airplane=session["airplane"])
            messg = "thành công"

        except:
            messg = "Không thành công"

    return render_template("employee/info_airplane.html", messg=messg, quantity=session["airplane"]["quantity_airport"])




def create_schedule():
    err_msg = ""
    if request.method == "POST":
        departure = request.form["from"]
        arrival = request.form["to"]
        time_de = request.form["date_departure"]
        time_arr = request.form["date_arrival"]
        rate1 = request.form["rate1"]
        rate2 = request.form["rate2"]
        quantity_airport = request.form["quantity_airport"]
        session["airplane"] = {
            "departure": departure,
            "arrival": arrival,
            "time_de": time_de,
            "time_arr":  time_arr,
            "rate1": int(rate1),
            "rate2": int(rate2),
            "quantity_airport":  int(quantity_airport)
        }
        # import pdb
        # pdb.set_trace()
        return redirect(url_for('submit_airplane'))

    return render_template("employee/schedule.html",
                           airport=utils.get_all_airport_names())


def employee_buy_ticket():

    flights = UtilsEmployee.get_list_flight()
    return render_template("employee/BuyTicket.html", flights=flights)


def list_buy_ticket():
    list_book_ticket = UtilsEmployee.customer_booked_ticket()

    return render_template("employee/ListBookTicket.html", list_book_ticket=list_book_ticket)


def load_detail_flight():

    # import pdb
    # pdb.set_trace()

    return render_template("employee/list-schedule.html", list_flight=UtilsEmployee.get_list_flight(),
                           airport=utils.get_all_airport_names(),
                           ticket_class=UtilsEmployee.get_class())

messg = ""

@app.context_processor
def common_reponse():
    return {
        'airport': utils.get_all_airport_names(),
        'messg': messg
    }


def flight_detail():
    flight_id = request.args.get("flight_id")
    list_flight = UtilsEmployee.get_detail_flight(flight_id=flight_id)
    # # if flight_id:
    flight_detail = UtilsEmployee.get_detail_flight(flight_id=int(flight_id))
    return render_template("employee/flight-detail.html", flight_detail=flight_detail,
                           stops=UtilsEmployee.get_stops())


def user_information():
    flight_id = request.args.get("f")
    list_flight = UtilsEmployee.get_detail_flight(flight_id=int(flight_id))
    list_airport = UtilsEmployee.get_airport()
    for airport in list_airport:
        if airport.id == list_flight.Route.departure_id:
            departure = airport.name
        if airport.id == list_flight.Route.arrival_id:
            arrival = airport.name

    info = {
        "flight_id": list_flight.Flight.id,
        "departure": departure,
        "arrival": arrival,
        "price": list_flight.TicketPrice.price,
        "departure_time": list_flight.Flight.departure_time,
        "arrival_time": list_flight.Flight.arrival_time,
        "class": list_flight.TicketPrice.ticket_class.name,
        "id_class": list_flight.TicketPrice.ticket_class.id
    }
    session["info"] = info

    return render_template("employee/UserInformation.html")


def enter_info():

    if request.method == "POST":
        name = request.form["fullname"]
        birthdate = request.form["birthdate"]
        phone = request.form["phone"]
        identify = request.form["identify"]
        info_user = {
            "name": name,
            "birthdate": birthdate,
            "phone": phone,
            "identify": identify,
            "departure": session["info"]["departure"],
            "arrival": session["info"]["arrival"],
            "price": session["info"]["price"],
            "departure_time": session["info"]["departure_time"],
            "arrival_time": session["info"]["arrival_time"],
            "class": session["info"]["class"],
            "flight_id": session["info"]["flight_id"],
            "id_class": session["info"]["id_class"]
        }
        session["info"] = info_user

    return render_template("employee/payment.html")

user_data = []

def payment():

    if request.method == "POST":
        try:
            UtilsEmployee.save_ticket(session.get("info"))
                    # client = Client(keys.account_sid, keys.auth_token)
                    # client.messages.create(
                    #     body="this is a sample message",
                    #     from_=keys.twilio_number,
                    #      to=keys.my_number)
            messg = "Success!!"

            user_data.append({
                        "departure": session["info"]["departure"],
                        "arrival": session["info"]["arrival"],
                        "price": session["info"]["price"],
                        "departure_time": session["info"]["departure_time"],
                        "arrival_time": session["info"]["arrival_time"],
                        "class": session["info"]["class"],
                        "flight_id": session["info"]["flight_id"],
                        "id_class": session["info"]["id_class"]
                    })


                    # import pdb
                    # pdb.set_trace()
            del session["info"]

            return render_template("employee/payment.html",  messg= messg)

        except Exception as ex:
            messg = "Not Success!!"
            return render_template("employee/payment.html",  messg= messg)



def export_ticket():
    pdf_file = generate_pdf_file()
    return send_file(pdf_file, as_attachment=True, download_name='Ticket.pdf')


def generate_pdf_file():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Create a PDF document
    p.drawString(100, 750, "Ticket")

    y = 700
    for user in user_data:
        p.drawString(100, y, f"departure: {user['departure']}")
        p.drawString(100, y - 20, f"arrival: {user['arrival']}")
        p.drawString(100, y - 40, f"price: {user['price']}")
        y -= 60

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


stripe_keys = {
    "secret_key": "sk_test_51O8JTWAinse2iCe4RYF94et3W6kCV1qmyVKtRa76ehMxWhziMPkSWfsVnHyB3cCMpeVpy3VrydwVWR5VONGgIpgM007PfrYs9v",
    "publishable_key": "pk_test_51O8JTWAinse2iCe44j6W9QiJkRYJN2svgQPiFCYuUsE69LPiWHghEtd5rQxXyOsTLmvZgZ4wHEp4IbLdywLJG3is00HSIIsOo4",
    "endpoint_secret": "whsec_da47e8ca5f6706fe92bd7fb8650e41f63c847d02393b46c471e1c987d1174e7f"
}

stripe.api_key = stripe_keys["secret_key"]


@app.route("/config")
def get_publishable_key():
    return jsonify({"publicKey": stripe_keys["publishable_key"]})


@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:

        payment_intent = stripe.PaymentIntent.create(
            amount=1099,
            currency='eur',
            automatic_payment_methods={'enabled': True}
        )
        return jsonify({'clientSecret': payment_intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': e.user_message}})


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://localhost:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "T-shirt",
                    "quantity": 1,
                    "currency": "usd",
                    "amount": "2000",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/my-route', methods=['POST'])
def my_route():
    import pdb
    pdb.set_trace()
    return jsonify({'request': request.json})


@app.route("/webhook", methods=['POST'])
def stripe_webhook():


    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        handle_checkout_session(session)

    return 'Success', 200


def handle_checkout_session(session):
    print("Payment was successful.")
    # TODO: run some custom code here




