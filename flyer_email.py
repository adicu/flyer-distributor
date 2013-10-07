
import simplejson
import requests
from sys import argv
from sys import exit
from os import environ

import make_email

MANDRILL_KEY    = environ['MANDRILL_KEY']
MANDRILL_EMAIL  = environ['MANDRILL_EMAIL']
MANDRILL_HOST   = environ['MANDRILL_HOST']
MANDRILL_PORT   = environ['MANDRILL_PORT']

MANDRILL_URL    = 'https://mandrillapp.com/api/1.0'
MANDRILL_MESSAGE_PATH   = '/messages/send.json'


def check_params():
    if len(argv) < 3:
        print ("@param 1: tab seperated values (assignment, person, email(+additional (person, email) tuples))" +
               "\n@param 2->n: pdf flyers")
        exit(1)


def get_assignments():
    with open(argv[1]) as f:
        assignments = simplejson.loads(f.read())['data']
    return assignments


def get_pdfs():
    pdf_names = argv[2::]
    # make sure pdf's were entered
    if not len(pdf_names):
        print 'Please pass in your flyer PDFs!'
        exit(1)

    # load all pdfs and encode them
    pdf = []
    for flyer in pdf_names:
        new_pdf = {
            "name": flyer.replace('../',''),
            "mimetype": "application/pdf"
        }
        # base 64 encode
        with open(flyer, 'rb') as pdf_file:
            new_pdf['content'] = pdf_file.read().encode('base64')
        pdf.append(new_pdf)

    return pdf


def send_emails(assignments, pdfs):
    #print assignments
    for item in assignments:
        params = {
            'key' : MANDRILL_KEY,
            'message': {
                'text' : make_email.flyer(item, 'Nate'),
                'subject' : "Flyers for this week",
                "from_email": MANDRILL_EMAIL,
                "from_name": 'Nate Brennand',
                "to": item['people'],
                "important": True,
                "tracks_opens": True,
                "attachments": pdfs
            }
        }
        response = requests.post(
            MANDRILL_URL+MANDRILL_MESSAGE_PATH,
            data = simplejson.dumps(params)
        )
        print response.status_code
        print response.text


if __name__ == '__main__':
    check_params()
    assignments = get_assignments()
    pdfs = get_pdfs()
    send_emails(assignments, pdfs)

