import datetime
import re


def _strptime(str):  # 1970-01-01T00:00:00Z
    return datetime.datetime.strptime(str, "%Y-%m-%dT%H:%M:%SZ")


def _strpduration(str: str):  # P1DT6H47M23S
    longtime = 0
    shorttime = 0
    if "D" in str:
        day = int(str[1])
        longtime = day * 24 * 60 * 60
    if "T" in str:
        timeduration = str.split("T")[-1]
        timeformat = ""
        for i in ("H", "M", "S"):
            if i in timeduration:
                timeformat += f"%{i*2}"
        # datetime.datetime.strptime(timeduration, timeformat).timestamp() : python bug
        shorttime = int(
            (datetime.datetime.strptime(timeduration, timeformat) - datetime.datetime(1900, 1, 1)).total_seconds()
        )
    return longtime + shorttime


def _intornone(str):
    if str is None or str == "":
        return None
    else:
        return int(str)


def _boolornone(str):
    if str is None:
        return None
    else:
        if str == "true":
            return True
        elif str == "false":
            return False


def _strpcategory(categories: list):
    return list(map(lambda x: x.split("https://en.wikipedia.org/wiki/")[-1], categories))


def _isLive(str: str):
    if str == "live":
        return True
    elif str == "none":
        return False
    print(str)


def preprocessVideoData(data):
    return {
        "id": data["id"],
        "duration": _strpduration(data["contentDetails"].get("duration")),
        "caption": _boolornone(data["contentDetails"].get("caption")),
        "publishedAt": _strptime(data["snippet"].get("publishedAt")),
        "channelId": data["snippet"].get("channelId"),
        "title": data["snippet"].get("title"),
        "description": data["snippet"].get("description"),
        "channelTitle": data["snippet"].get("channelTitle"),
        "tags": data["snippet"].get("tags"),
        "categoryId": _intornone(data["snippet"].get("categoryId")),
        "liveBroadcastContent": _isLive(data["snippet"].get("liveBroadcastContent")),
        "defaultAudioLanguage": data["snippet"].get("defaultAudioLanguage"),
        "defaultLanguage": data["snippet"].get("defaultLanguage"),
        "viewCount": _intornone(data["statistics"].get("viewCount")),
        "commentCount": _intornone(data["statistics"].get("commentCount")),
        "likeCount": _intornone(data["statistics"].get("likeCount")),
        "favoriteCount": _intornone(data["statistics"].get("favoriteCount")),
        "madeForKids": data["status"].get("madeForKids"),
        "uploadStatus": data["status"].get("uploadStatus"),
        "topicCategories": _strpcategory(data.get("topicDetails", {}).get("topicCategories", [])),
    }


def isKoreanVideo(data: dict):
    hangul = re.compile("[가-힣]+")
    for value in data.values():
        result = hangul.findall(str(value))
        if result:
            return True
    return False
