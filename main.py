import requests
import json

# variable for URL to API
apiUrl = "https://mighty-cliffs-81365.herokuapp.com/"


def main():
    """
    Main method
    """

    print('Welcome to the Video Game API CLI (written in Python)')
    access_token = login()
    print(f"Logged in successfully! Your token is: {access_token}")
    while True:
        print('Type the letter in the brackets to access the API')
        print('Main menu:\n(D)isplay games\n(F)ind game\n(U)pdate game\n(A)dd game\n(D)elete game\n(Q)uit')
        choice = input("Please enter your choice").upper()
        if choice == 'D':
            display_game(access_token)
        elif choice == 'F':
            find_game(access_token)
        elif choice == 'U':
            print('Update')
        elif choice == 'A':
            print('Add')
        elif choice == 'D':
            print('Delete')
        elif choice == 'Q':
            print('Goodbye!')
            break
        else:
            print('Invalid command - please try again!')


def login():
    """
    :return:
    The JWT Token from the API to enable access to end points
    """
    while True:
        print("Please enter credentials:")
        username = input('Enter the username')
        password = input('Enter the password')

        # construct payload for request
        payload = json.dumps({
            "username": username,
            "password": password
        })

        # construct headers
        headers = {
            'Content-Type': 'application/json'
        }

        print('Now logging into the Video Game API\nPlease wait (the API might be slow to respond at first)')
        r = requests.post(f'{apiUrl}/login', headers=headers, data=payload)
        if r.status_code != 200:
            print('Error with logging in - please try again!')
            pass
        else:
            # grab access token from response
            json_response = r.json()
            access_token = json_response['access_token']
            return access_token


def display_game(access_token):
    """
    :return:
    All games in the API
    """
    print('Fetching games from the API...')

    # construct headers
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    r = requests.get(f'{apiUrl}/displayGames', headers=headers)
    # decode JSON
    json_response = r.json()
    games = json_response.get('Games')

    # iterate through response
    for i in range(len(games)):
        temp_dict = games[i]
        game = temp_dict['Game']
        for x, y in game.items():
            print(f'{x}:{y}')
        print('\n')


def find_game(access_token):
    print('Please enter a search term')
    search = input('Enter input')
    print(f'Now searching for {search}....')

    # construct headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # construct payload for request
    payload = json.dumps({
        "name": search
    })

    r = requests.get(f'{apiUrl}/findGame', headers=headers, data=payload)
    if r.status_code != 200:
        print('No matches found!')
    else:
        # decode JSON
        json_response = r.json()
        games = json_response.get('Games')

        for i in range(len(games)):
            temp_dict = games[i]
            game = temp_dict['Game']
            for x, y in game.items():
                print(f'{x}:{y}')
            print('\n')


if __name__ == '__main__':
    main()
