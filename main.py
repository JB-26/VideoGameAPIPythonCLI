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
        print('Type the letters in the brackets to access the API')
        print('Main menu:\n(D)isplay games\n(F)ind game\n(U)pdate game\n(A)dd game\n(De)lete game\n(Q)uit')
        choice = input("Please enter your choice").upper()
        if choice == 'D':
            display_game(access_token)
        elif choice == 'F':
            find_game(access_token)
        elif choice == 'U':
            update_game(access_token)
        elif choice == 'A':
            add_game(access_token)
        elif choice == 'DE':
            delete_game(access_token)
        elif choice == 'Q':
            print('Goodbye!')
            break
        else:
            print('Invalid command - please try again!')


def decode_json(json_data):
    """
    :param json_data:
    :return:
    Decodes JSON response from API
    """
    # decode JSON
    json_response = json_data.json()
    games = json_response.get('Games')

    # iterate through response
    for i in range(len(games)):
        temp_dict = games[i]
        game = temp_dict['Game']
        for x, y in game.items():
            print(f'{x}:{y}')
        print('\n')


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
        headers_login = {
            'Content-Type': 'application/json'
        }

        print('Now logging into the Video Game API\nPlease wait (the API might be slow to respond at first)')
        r = requests.post(f'{apiUrl}/login', headers=headers_login, data=payload)
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
    decode_json(r)


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
        print(f'Unable to locate a game with the following search term - {search}')
    else:
        decode_json(r)


def update_game(access_token):
    """
    :return: Updates a game in the database
    """
    update_id = int(input('Enter the ID of the game you want to update'))
    update_field = input('Enter the field that you wish to update (i.e. Name, Genre, Platform').lower()
    update_value = input('Enter the value you want to update with')

    # construct payload for request
    payload = json.dumps({
        "id": update_id,
        "field": update_field,
        "value": update_value
    })

    # construct headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    print(f'Now updating - \nID: {update_id}\nField: {update_field}\nValue: {update_value}')
    r = requests.put(f'{apiUrl}/updateGame', headers=headers, data=payload)
    if r.status_code != 200:
        print('An error occurred - please try again!')
    else:
        print('Update complete!')
        json_response = r.json()
        result = json_response.get('Game updated:')
        result = result.get('Game')
        print('New updated entry:')
        for x in result:
            print(f'{x} {result[x]}')


def delete_game(access_token):
    """
    :return:
    Deletes a game from the database
    """
    delete_id = int(input('Enter the ID of the game in the database you want to delete'))
    # construct payload for request
    payload = json.dumps({
        "id": delete_id
    })

    # construct headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    r = requests.delete(f'{apiUrl}/deleteGame', headers=headers, data=payload)
    print('The following game has been deleted:')
    if r.status_code != 200:
        print('An error occurred - please try again!')
    else:
        print('Update complete!')
        json_response = r.json()
        result = json_response.get('The following has been deleted')
        result = result.get('Game')
        print('New updated entry:')
        for x in result:
            print(f'{x} {result[x]}')


def add_game(access_token):
    """
    :param access_token:
    :return: Adds a game to the database
    """

    # construct headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    print('Please enter the following details for the game you want to add:')
    add_name = input('Enter the name: ')
    add_platform = input('Enter the platform: ')
    add_publisher = input('Enter the publisher: ')
    add_genre = input('Enter the genre: ')
    add_year = int(input('Enter the year: '))

    # construct payload for request
    payload = json.dumps({
        "name": add_name,
        "platform": add_platform,
        "publisher": add_publisher,
        "genre": add_genre,
        "year": add_year
    })

    r = requests.post(f'{apiUrl}/addGame', headers=headers, data=payload)
    if r.status_code != 201:
        print('An error has occurred - please try again!')
    else:
        print('The following has been added:')
        print(f'Name: {add_name}')
        print(f'Platform: {add_platform}')
        print(f'Publisher: {add_publisher}')
        print(f'Genre: {add_genre}')
        print(f'Year: {add_year}')


if __name__ == '__main__':
    main()
