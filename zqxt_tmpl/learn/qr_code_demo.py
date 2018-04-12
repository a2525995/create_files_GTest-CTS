import qrcode


def create(URL,Path):
    img = qrcode.make(URL)
    with open(Path+'qrcode.png','wb')as f:
        img.save(f)