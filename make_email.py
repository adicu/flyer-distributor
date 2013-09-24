

def flyer(assign, sender_name):
    with open('templates/flyer.txt') as f:
        text = f.read()

    recipients = [person['name'] for person in assign['people']]
    name_string = ' & '.join(recipients)
    place = assign['location']

    return text.format(
        names = name_string,
        location = place,
        sender = sender_name
    )


