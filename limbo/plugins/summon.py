import requests
import sys
import re


token = 'xoxp-2543006699-3669524994-6723996225-a82588'
optimization_channel = 'C03KM8KEH'


def get_users():
    users_url = 'https://slack.com/api/users.list?token={}'.format(token)
    r = requests.get(users_url)
    return r.json().get('members')


def on_message(msg, server):
    body = msg.get('text', '').lower()
    print body
    reg = re.compile('^!summon\s(.*)?', re.IGNORECASE)
    match = reg.match(body)
    user = match.group(1).split()[0].strip('@').strip(':')
    email = '{}@appnexus.com'.format(user)
    if not match:
        return False

    users = get_users()
    try:
        user = filter(lambda x: x['profile'].get('email') == email, users)[0]
    except:
        return "Could not find user"

    user_id = user.get('id')
    invite_url = 'https://slack.com/api/channels.invite?token={0}&channel={1}&user={2}'.format(token, optimization_channel, user_id)
    r = requests.get(invite_url)
    if 'error' in r.json():
        print r.json()['error']
        return "Error summoning this user. Try again, novice summoner."

    name = user.get('real_name')
    return '{}, you have been summoned by the all-powerful goob.'.format(name)


if __name__ == "__main__":
    print on_message({'text': '!summon ' + sys.argv[1]}, None)