# RequestWeb

RequestWeb is a Python library for requesting a website and getting data from the website and response as an HTML code. It provides additional features like favicon generation from URL, extracting the title of the webpage, obtaining SSL information about the website, and supporting JavaScript-enabled websites to get data.

## Features

- Request a website and get the data as html code
- Generate favicon from URL
- Extract title from the webpage
- Obtain SSL information about the website
- Support JavaScript-enabled websites to get data

## Installation

```sh
pip install requestweb

```

## 1 Get HTML Code

```python
import requestweb

html = requestweb.load_url('https://www.python.org/')
 if html:
     print(html)
```

```OUTPUT
<html>
<head>
<title>pythonDomain</title>
<meta charset="utf-8"/>
<meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style type="text/css"></style>
</head>
<body data-new-gr-c-s-check-loaded="14.1039.0" data-gr-ext-installed="">
<div>
<h1>Example Domain</h1>
<p>This domain is for use in illustrative examples in documents.</p>
<p> <a href="https://nullfunctions.weebly.com/">Learn More...</a> </p>
</div>
</body>
</html>
```

## 2 Get Title

```python
import requestweb

title = requestweb.getTitle('https://www.python.org/')
if title:
    print(title)
```

```OUTPUT
Title:-Python
```
## 3 Get Favicon

```python
import requestweb

fav = requestweb.getFavicon('https://www.python.org/')
if fav:
    print(fav)

```

```OUTPUT
Favicon:-data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACOElEQVQ4jWWTTUhVQRTHf/e+a+/1RCghSqNN0KYWbVq1aCFIm5AKHtQ2cFOUazdB0CKIiHZKmxbSxkUkiFFEkRGmpW0tIrNMBTU/3r0zb+bM3Bbv3rzqwGFg5vc/5z8fJ2DX6Hnw9pk0zDnvTLvYBmIM0lDaKv3448D1fkADLufD3Qm8k4uj/d3tTizOWrxYvHeVNPA3gWNApcjvSeCs5fydEZzY7bA23+4AqkU+Auh5+P62t/a4WBUYnQwZVY9ExyVnDOG+ci1Nfc6XgdKOBJcffXjtxHalXsB7AqAUtUC5CkEJJ7bIk87XFr2Ntej6/fKpd/dC711X06rZaTuLfIjaGgMskhA6VYnQN4DOKAd9QeQL505Tr52O30w/6R9cme7uRhRIQuhVO9AR7RBbi66vjy1MjDxdmHm1DgiQAmZ+vPvkwVbpwylwCUgCsD8S09BebMWJRW2sDE8O9g1t/rx1pbVy4lLoVOU/LDF5dUThRWsgCJ3IXG79z9TL5/Gvvt62qr8a+qI4KYgTcJokSacAEzodD4gx2onl9/ToerXiLmwLCqKCGGBmVr8AtoLsZ3UAR4FGunhtMoeXl/4Ol7xKm04UOAXAtznz5Wzv2gTwIwIMsARsAmmx2uEDroYIOAtiCc4sdQF1QGX8agj4bGEVWPM20U2rhTj9FZ+mOnuRReB7Nid7eqG+uVGzOv7sTaxzJ3aic3b8k7oLWCDJClogDXYnyO7kEHAEaANaMpdbWdVlmi0NwD8Bv6//isUl3wAAAABJRU5ErkJggg==
```

## 4 Get SSL Info

```python
import requestweb

ssl = requestweb.get_ssl_details('https://www.python.org/')
if ssl:
    print(ssl)

```

```OUTPUT

{'safe': True, 'expires': datetime.datetime(2025, 6, 10, 12, 50, 10), 'issuer': 'GlobalSign Atlas R3 DV TLS CA 2024 Q2'}

```
