def extract_seller_id(url):
    splitted = url.split('?')
    splitted = splitted[0]
    splitted = url.split('/')
    return splitted[2]
