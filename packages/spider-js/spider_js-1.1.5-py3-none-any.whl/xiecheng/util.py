import base64

def base64encode(text):
    assert isinstance(text,str)
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def base64decode(text):
    # print(text)
    assert isinstance(text, str)
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')


if __name__ == '__main__':
    print(base64encode('hello你好'))
    print(base64decode('aGVsbG/kvaDlpb0='))
