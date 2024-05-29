import re

VISIBLE_ACTORS=("boy", "girl", "eily")
INVISIBLE_ACTORS=("", "M", "F")
SCENARIO_ACTORS=("ending", "exam", "concentrak", "notes")

def remove_emojis(text):
    emojiPattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F926-\U0001F991"
                    "]+", flags = re.UNICODE)
    return re.sub(emojiPattern, '', text)

def has_chinese_char(text):
  """Checks if a string contains at least one Chinese character.

  Args:
      text: The string to be checked.

  Returns:
      True if the string contains at least one Chinese character, False otherwise.
  """
  # Check if any character in the string falls within the Unicode range of Chinese characters
  return any(u'\u4e00' <= char <= u'\u9fff' for char in text)

def update_object(original, update, default_locale=None):
    """Updates the original object from the update object.

    Args:
        original: The object to be updated.
        update: The object containing updates.

    Returns:
        A new object with the updates applied.
    """
    if isinstance(update, dict):
        return {
            **(original \
                if isinstance(original, dict) \
                else {default_locale: original}), \
            **{key: update[key] for key in update}
        }
    elif isinstance(original, dict) and default_locale != None:
        original[default_locale] = update
    else:
        original = update
    return original

def get_actors(objects):
    assert isinstance(objects, list)
    actor = None
    narrator = None
    defaultObject = None
    actorId = -1
    narratorId = -1
    defaultObjectId = -1
    for i, object in enumerate(objects):
        if object.get("name", None) in VISIBLE_ACTORS:
            actor = object["name"]
            actorId = i
        elif object.get("name", None) in INVISIBLE_ACTORS:
            narrator = object["name"]
            narratorId = i
        else:
            defaultObject = object.get("name", None)
            defaultObjectId = i
    return actor, actorId, narrator, narratorId, defaultObject, defaultObjectId

def get_image_from_board(boardObject):
    image = None
    rect = None
    caption = None
    if "content" in boardObject:
        rect = boardObject["rect"]
        image = boardObject["content"].get("image", None)
        video = boardObject["content"].get("src", None)
        videoType = boardObject["content"].get("videoType", None)
        caption = boardObject["content"].get("caption", None)
    return rect, image, video, videoType, caption

def get_html_from_board(boardObject):
    html = None
    rect = boardObject.get("rect", None)
    if "content" in boardObject:
        html = boardObject["content"].get("html", None)
    return rect, html

def get_question_from_board(boardObject):
    question = None
    options = None
    answer = None
    rect = None
    colsPerRow = 1
    fontSize = 20
    fontColor = "white"
    rect = boardObject.get("rect", rect)
    if "content" in boardObject:
        question = boardObject["content"].get("question", question)
        options = boardObject["content"].get("options", options)
        answer = boardObject["content"].get("answer", answer)
        colsPerRow = boardObject["content"].get("colsPerRow", colsPerRow)
        fontSize = boardObject["content"].get("fontSize", fontSize)
        fontColor = boardObject["content"].get("fontColor", fontColor)
    return rect, question, options, answer, colsPerRow, fontSize, fontColor

def get_contentList_from_board(boardObject):
    contentList = []
    if "contentList" in boardObject:
        pass

def get_subscript_from_interaction(interactionObject):
    actor = -1
    voice = -1
    figure = -1
    text = None
    duration = ""
    if "content" in interactionObject:
        text = interactionObject["content"].get("text", text)
        voice = interactionObject["content"].get("voice", voice)
        actor = interactionObject.get("actor", actor)
        figure = interactionObject.get("figure", figure)
        duration = interactionObject.get("duration", duration)
    return actor, figure, text, voice, duration

def get_bullets_from_html(html):
    import re
    # Define a pattern to match the content within list items (ul or li tags)
    pattern = r"<(ul|li)>(.*?)</(ul|li)>"

    # Extract content from html using findall
    matches = re.findall(pattern, html, flags=re.DOTALL)

    extracted = []
    if matches:
        # Remove tags using re.sub
        extracted = [re.sub(r"<[^>]+>", "", match[1]) for match in matches]
    return extracted

def switch_to_test_path(path):
    if path.startswith("/story/"):
        return "/test/" + path[len("/story/"):]
    else:
        return path


