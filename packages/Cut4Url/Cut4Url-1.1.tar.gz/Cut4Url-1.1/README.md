# My library for shortening links

A simple library for shortening links

## Installation

**You can install this library using pip**:
```
pip install Cut4Url
```
## How to use
```
from Cut4Url import Cut4Url

shortener = Cut4Url.Short()

shortened_url = shortener.clck("https://google.com")
print("Clck:", shortened_url)

shortened_url = shortener.ulvis("https://google.com")
print("Ulvis:", shortened_url)

shortened_url = shortener.isgd("https://google.com")
print("Is.gd:", shortened_url)

shortened_url = shortener.acesse("https://google.com")
print("Acesse:", shortened_url)

shortened_url = shortener.cleanuri("https://google.com")
print("CleanURI:", shortened_url)

```