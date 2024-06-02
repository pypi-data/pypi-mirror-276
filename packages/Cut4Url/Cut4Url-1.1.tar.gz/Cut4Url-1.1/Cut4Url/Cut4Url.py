import requests

class Short:
    def __init__(self):
        pass

    def clck(self, url):
        response = requests.get(f"https://clck.ru/--?url={url}")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return Exception(f"Error shortening URL: {url}")

    def ulvis(self, url):
        response = requests.get(f"https://ulvis.net/api.php?url={url}")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return Exception(f"Error shortening URL: {url}")
            
    def isgd(self, url):
        response = requests.get(f"https://is.gd/create.php?format=simple&url={url}")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return Exception(f"Error shortening URL: {url}")
            
    def acesse(self, url):
        headers = {'content-type': 'application/json'}
        json_data = {'url': url}
        response = requests.post('https://api.encurtador.dev/encurtamentos', headers=headers, json=json_data)
        if response.status_code == 200:
            return response.json()["urlEncurtada"]
        else:
            return Exception(f"Error shortening URL: {url}")

    def cleanuri(self, url):
        data = {'url': url}
        response = requests.post('https://cleanuri.com/api/v1/shorten', data=data)
        if response.status_code == 200:
            return response.json()["result_url"]
        else:
            return Exception(f"Error shortening URL: {url}")
