"""
Manage the phone number of a google directory for a specific user

@author: Mathieu R.
@date: 14/11/2012
"""

import gdata.apps.client
import gdata.contacts.client
import pprint
import argparse

DOMAIN = "XXX"
EMAIL = "XXX"
PASSWORD = "XXX"

def get_client(domain, email, password):
    gd_client = gdata.contacts.client.ContactsClient(
            source='GoogleInc-ContactsPython',
            domain=domain)
    gd_client.ClientLogin(email, password, gd_client.source)
    return gd_client

def get_profile(gd_client, nickname, domain):
    url = "https://www.google.com/m8/feeds/profiles/domain/%s/full/%s" \
        % (domain, nickname)
    return gd_client.GetProfile(url)

def delete_phone(nickname, domain, email, password):
    client = get_client(domain, email, password)
    profile = get_profile(client, nickname, domain)
    profile.phone_number = []
    client.Update(profile)

def update_phone(nickname, domain, email, password, phone):
    client = get_client(domain, email, password)
    profile = get_profile(client, nickname, domain)
    my_phone_number = gdata.data.PhoneNumber(
            text=phone,
            rel=gdata.data.WORK_REL,
            primay='true')
    profile.phone_number = [ my_phone_number ]
    client.Update(profile)

def get_phone(nickname, domain, email, password):
    client = get_client(domain, email, password)
    profile = get_profile(client, nickname, domain)
    if profile.phone_number:
        return profile.phone_number[0].text
    else:
        return None


def main():

    parser = argparse.ArgumentParser(
            description='Manage the phone number \
                    of a google directory for a specific user')
    parser.add_argument('login', metavar='login', type=str, nargs=1,
            help='The user login without domain like m.roche')
    parser.add_argument('--update', '-u',
            metavar="PHONE_NUMBER", dest='phone',
            action='store',
            help='Add or update the phone number of the user')
    parser.add_argument('--delete', '-d',
            action='store_true',
            help='Delete the phone number of the user')
    args = parser.parse_args()

    email = EMAIL
    password = PASSWORD
    domain = DOMAIN

    nickname = args.login[0]
    phone = args.phone
    delete = args.delete
    print nickname
    print phone
    print delete

    if (delete):
        delete_phone(nickname, domain, email, password)

    if (phone):
        update_phone(nickname, domain, email, password, phone)

    pprint.pprint(get_phone(
        nickname,
        domain,
        email,
        password))

if __name__ == "__main__":
    main()
