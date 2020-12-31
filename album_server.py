from bottle import route
from bottle import run
from bottle import get, post, request
from bottle import HTTPError

import album  # импортируем созданный модуль album.py


@get("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = f"Альбомов {artist} не найдено"
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = f"####### Список альбомов {artist}: #######<br>"
        result += "<br>".join(album_names)
    return result


@post("/albums")
def creat_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Введен некорректный год альбома")

    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:
        result = f"Альбом #{new_album.id} сохранен"
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

