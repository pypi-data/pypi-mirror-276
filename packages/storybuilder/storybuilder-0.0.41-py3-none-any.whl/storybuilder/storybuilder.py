import json
import random
import os
import uuid
import re
import copy
import xml.etree.ElementTree as ET
from PIL import Image
from typing import Dict, Union

from .utility import *

from .storyprofiles import CHARACTER_FIGURE_ACCESSORY_KEYS, STORY_SCENARIO_STYLES
from .characterpostures import CHARACTER_FIGURES

DEFAULT_LANGUAGE="zh-CN"
LANGUAGE_ENG="en-US"
DEFAULT_NARRATOR="M"
VISIBLE_ACTORS=("boy", "girl", "eily")
INVISIBLE_ACTORS=("", "M", "F")
SCENARIO_ACTORS=("ending", "exam", "concentrak", "notes")
LOCAL_DEFAULT_ROOT="./test"

MText = Dict[str, str]

def isMText(text: Union[str, MText]):
    return isinstance(text, dict) and len(text) > 0

class Story:

    def test(self, localOutputPath=LOCAL_DEFAULT_ROOT, fileName="testStory.json", language=DEFAULT_LANGUAGE):
        directory = os.path.join(localOutputPath, self.storyId)
        if not os.path.exists(directory):
            os.makedirs(directory)

        language = DEFAULT_LANGUAGE if language == None else language
        scripts = self.exportScripts()
        if self._synthesizer != None:
            try:
                for script in scripts:
                    for voice in script["voices"]:
                        soundFileName = voice["sound"]
                        if isinstance(soundFileName, str) and len(soundFileName) > 0:
                            text = voice["subscript"][language] if isinstance(voice["subscript"], dict) else voice["subscript"]
                            alternativeText = None if "alternative" not in voice \
                                else (voice["alternative"][DEFAULT_LANGUAGE] \
                                    if isinstance(voice["alternative"], dict) \
                                    else voice["alternative"])
                            narrator = voice["narrator"]
                            text = text if alternativeText == None else alternativeText
                            self._synthesizer.synthesizeFile(
                                    narrator, remove_emojis(text), language, directory, os.path.basename(soundFileName)
                                )
                            localOutputFileName = os.path.join(directory, os.path.basename(soundFileName))
                            if self._cosUploader != None:
                                self._cosUploader.local2cos(localOutputFileName, self.storyId, self.audioPath)   
            except Exception as e:
                print(f"Story.test failed for {script}\n", e)

        with open(os.path.join(localOutputPath, fileName), "w") as file:
            json.dump(
                self.export(), file, ensure_ascii=False, indent=4, sort_keys=False
            )
    
    def export(self):
        voices = [{"sound": "/story/audios/OurMusicBox - 24 Hour Coverage - intro.mp3"}]
        events = []
        for page in self._pages:
            pageObject = page.export(voiceOffset=len(voices), pageId=float(len(events)))
            if pageObject != None and isinstance(pageObject, dict) \
                and "voices" in pageObject and "events" in pageObject:
                for entry in pageObject["voices"]:
                    entryObject = {}
                    for key in set(entry.keys()) & {"sound", "languages"}:
                        if entry[key] != None:
                            entryObject[key] = entry[key]
                    if len(entryObject) > 0:
                        voices.append(entryObject)
                events = events + pageObject["events"]

        return {"voices": voices, "events": events}

    def exportScripts(self):
        voices = []
        for i, page in enumerate(self._pages):
            pageObject = page.export(voiceOffset=len(voices))
            pageVoices = []
            for voice in pageObject["voices"]:
                if (isinstance(voice["subscript"], str) or isinstance(voice["subscript"], dict)) and len(voice["subscript"]) > 0:
                    pageVoices.append(voice)
            if len(pageVoices) > 0:
                voices = voices + [{"page": i, "voices": pageVoices}]

        return voices

    def exportAudios(self, localOutputPath=LOCAL_DEFAULT_ROOT, uploadToCos=True):
        directory = os.path.join(localOutputPath, self.storyId)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if self._synthesizer:
            voices = self.exportScripts()
            for page in voices:
                for i, voice in enumerate(page["voices"]):
                    if not isinstance(voice["sound"], str) or voice["sound"].startswith("/story/"): # Ignore if production audio
                        continue
                    try:
                        fileName = os.path.basename(voice["sound"])
                        character = voice["narrator"]
                        for language in voice["subscript"]:
                                subscript = (
                                    voice["alternative"][language]
                                    if ("alternative" in voice) and (language in voice["alternative"]) and (voice["alternative"][language] != None)
                                    else voice["subscript"][language]
                                )
                                print(f'Page {page["page"]}/Script {i}')
                                self._synthesizer.synthesizeFile(
                                    character, remove_emojis(subscript), language, directory, fileName
                                )
                                localOutputFileName = os.path.join(directory, fileName)

                                if self._cosUploader != None and uploadToCos:
                                    _ = self._cosUploader.local2cos(localOutputFileName, self.storyId, self.audioPath)
                    except Exception as e:
                        print(f"Synthesize & upload script failed for <{voice['subscript']}><{subscript}>\n", e)
                        continue

    def exportProduct(self, localOutputPath='./prod'):
        if self._cosUploader == None:
            print("Cos uploader is not available, exit.")
            return

        if not os.path.exists(localOutputPath):
            os.makedirs(localOutputPath)

        storyObject = self.export()
        
        # Copy audios to product path
        for i, voice in enumerate(storyObject["voices"]):
            storyObject["voices"][i]["sound"] = self._cosUploader.test2product(voice["sound"])

        # Copy images to product path
        for j, event in enumerate(storyObject["events"]):
            if "board" in event and isinstance(event["board"], dict):
                board = event["board"]
                if "content" in board and isinstance(board["content"], dict) \
                    and "image" in board["content"] and isinstance(board["content"]["image"], str) \
                    and len(board["content"]["image"]) > 0:
                    storyObject["events"][j]["board"]["content"]["image"] = self._cosUploader.test2product(board["content"]["image"])
                if "contentList" in board and isinstance(board["contentList"], list) \
                    and len(board["contentList"]) > 0:
                    for k, contentEntry in enumerate(board["contentList"]):
                        if "image" in contentEntry and isinstance(contentEntry["image"], str) \
                            and len(contentEntry["image"]) > 0:
                            storyObject["events"][j]["board"]["contentList"][k]["image"] = self._cosUploader.test2product(contentEntry["image"])

        productFileName = os.path.join(localOutputPath, self.title + ".product.json")
        with open(productFileName, "w") as file:
            json.dump(
                storyObject, file, ensure_ascii=False, indent=4, sort_keys=False
            )
        print(f"Story resource copied from test to production, product story generated as {productFileName}.")

    @staticmethod
    def buildStoryCollection(outputName, storyList):
        storyCollection = {"collection": []}
        for story in storyList:
            storyTitle = story[:len(story)-5] if story.endswith(".json") else story
            storyCollection["collection"].append(storyTitle)
        with open(outputName, "w") as file:
            json.dump(
                storyCollection, file, ensure_ascii=False, indent=4, sort_keys=False
            )

    @staticmethod
    def retrieveSvgSize(image_path):
        # Load the SVG file
        tree = ET.parse(image_path)
        root = tree.getroot()

        # Extract attributes from the <svg> tag
        width = root.get("width", 0)  # Get the width attribute
        height = root.get("height", 0)  # Get the height attribute
        viewBox = root.get("viewBox", "0, 0, 0, 0")  # Get the viewBox attribute

        split_pattern = r"[ ,]+"

        return [int(width), int(height)], [
            int(float(num)) for num in re.split(split_pattern, viewBox)
        ]

    @staticmethod
    def retrievePixelSize(image_path):
        # Open the image using the Python Imaging Library (PIL)
        image = Image.open(image_path)

        # Get the width and height of the image in pixels
        width, height = image.size

        # Return the width and height as a tuple
        return width, height

    @staticmethod
    def getImageSize(file_path):
        width = height = 0
        try:
            if ".svg" in file_path[-4:]:
                dim2, dim4 = Story.retrieveSvgSize(file_path)
                if dim2 == [0, 0]:
                    width = dim4[2]
                    height = dim4[3]
                else:
                    width = dim2[0]
                    height = dim2[1]
            elif (
                ".jpg" in file_path[-4:]
                or ".jpeg" in file_path[-5:]
                or ".png" in file_path[-4:]
                or ".gif" in file_path[-4:]
            ):
                width, height = Story.retrievePixelSize(file_path)
        except:
            print("Retrieve image size error for", file_path)
        return width, height
    
    @staticmethod
    def loadFromFile(fileName, locale=DEFAULT_LANGUAGE, **kwargs):
        story = None
        storyId = None
        try:
            with open(fileName, 'r') as f:
                object = json.load(f)
            voices = object["voices"]
            events = object["events"]
            storyId = kwargs["storyId"] if "storyId" in kwargs else storyId
            if len(voices) > 1:
                for i in range(1, len(voices)):
                    folder = voices[i].get("sound", "//").split("/")[-2]
                    if len(folder) == 36: # length of uuid.uuid4()
                        storyId = folder
            storyStyle = None
            validScene = None
            for i in range(len(events)):
                if events[i].get("scene", None) != None and len(events[i]["scene"]) > 0:
                    validScene = events[i]["scene"]
                    break
            for styleKey in STORY_SCENARIO_STYLES.keys():
                for key, value in STORY_SCENARIO_STYLES[styleKey]["scenarios"].items():
                    if value == validScene \
                        or (key == "notes" and value["scene"] == validScene):
                        storyStyle = styleKey
                        break
            defaultNarrator = None
            for event in events:
                if defaultNarrator != None:
                    break
                if "objects" in event and isinstance(event["objects"], list):
                    _, _, defaultNarrator, _, _, _ = get_actors(event["objects"])
            kwargs["narrator"] = defaultNarrator if defaultNarrator != None else DEFAULT_NARRATOR
            story = Story(title=os.path.basename(fileName).replace(".json", ""), 
                        storyId=storyId, 
                        style=storyStyle, 
                        locale=locale, 
                        **kwargs)

            pageScenario = None
            for event in events:
                # 获取页面类型
                if "board" in event \
                    and ((event["board"].get("type", None) != None and len(event["board"]["type"]) > 0) \
                         or (isinstance(event["board"].get("content", None), dict) \
                             and event["board"]["content"].get("type", None) != None)):
                    pageScenario = event["board"]["type"] if event["board"].get("type", None) != None else event["board"]["content"]["type"]
                else:
                    sceneObject = event.get("scene", None)
                    if isinstance(sceneObject, str) and len(sceneObject) > 0:
                        for key, value in STORY_SCENARIO_STYLES[storyStyle]["scenarios"].items():
                            if isinstance(value, str) and value == sceneObject:
                                pageScenario = key
                    elif "index" in sceneObject and sceneObject["index"] == STORY_SCENARIO_STYLES[storyStyle]["scenarios"]["concentrak"]["index"]:
                        pageScenario = "concentrak"
                    elif "bgColor" in sceneObject and len(sceneObject["bgColor"]) > 0:
                        pageScenario = "blackboard"
                pageScenario = "cover" if pageScenario == None else pageScenario # 没有样式匹配，设为CoverPage


                # 创建对应页面
                print(f"Loading page as {pageScenario}")
                # CoverPage
                if pageScenario == "cover":
                    story.createPage(
                        sceneType = pageScenario,
                        source = "",
                        voices = voices,
                        board = event["board"],
                        objects = event["objects"],
                        interactions = event["interactions"]
                        )
                # ClassroomPage
                elif pageScenario == "classroom":
                    story.createPage(
                        sceneType = pageScenario,
                        actor = "",
                        voices = copy.deepcopy(voices),
                        board = event["board"],
                        objects = event["objects"],
                        interactions = event["interactions"]
                        )
                # BlackboardPage
                elif pageScenario == "blackboard":
                    story.createPage(
                        sceneType = pageScenario,
                        source = "",
                        voices = copy.deepcopy(voices),
                        board = event["board"],
                        objects = event["objects"],
                        interactions = event["interactions"]
                        )

                # ConcentrakPage
                elif pageScenario == "concentrak":
                    story.createPage(
                        sceneType = pageScenario,
                        text = "",
                        voices = copy.deepcopy(voices),
                        board = event["board"],
                        objects = event["objects"],
                        interactions = event["interactions"]
                        )
                # ExamPage
                elif pageScenario == "exam":
                    story.createPage(
                        sceneType = pageScenario,
                        actor = "", 
                        voices = copy.deepcopy(voices),
                        board = event["board"],
                        objects = event["objects"],
                        interactions = event["interactions"]
                    )

                # NotesPage
                elif pageScenario == "notes":
                    story.createPage(
                        sceneType = pageScenario,
                        actor = "", 
                        voices = copy.deepcopy(voices),
                        board = event["board"],
                        objects = event["objects"],
                        interactions = event["interactions"]
                    )

                else:
                    pass            
            
        except Exception as e:
            print("Load story from file exception:\n", e)
            return None
            
        return story

    def __init__(self, title, storyId=None, style="shinkai_makoto", **kwargs):
        self.title = title
        self.storyId = storyId if storyId != None else uuid.uuid4()
        self.styles = STORY_SCENARIO_STYLES[style]
        self.locale = kwargs["locale"] if "locale" in kwargs else DEFAULT_LANGUAGE
        self.narrator = kwargs["narrator"] if "narrator" in kwargs else DEFAULT_NARRATOR
        self._pages = []
        self.posterPath = 'test/posters/'
        self.audioPath = 'test/audios/'

        self._cosUploader = kwargs["uploader"] if "uploader" in kwargs else None
        self._synthesizer = kwargs["synthesizer"] if "synthesizer" in kwargs else None

        self._defaultCharacters = CHARACTER_FIGURES

        print(f"Create a new story title: {title}, Id:", self.storyId)

    def getAudioPath(self, fileName):
        return os.path.join("/", self.audioPath, self.storyId, fileName)

    def getUserPostureId(
        self, actor, postures, keyScenario="stand", excludeAccessories=True
    ):
        if type(postures) is int:
            return postures
        if type(postures) is list and type(postures[0]) is int:
            return postures[0]
        if self._defaultCharacters == None:
            return 0

        currentActorFigures = self._defaultCharacters[actor]
        availableFigures = []
        for j, figure in enumerate(currentActorFigures):
            skip = False
            if excludeAccessories:
                for accessory in CHARACTER_FIGURE_ACCESSORY_KEYS:
                    if accessory in figure:
                        skip = True
            if skip:
                continue
            if keyScenario in figure and all(keyWord in figure for keyWord in postures):
                availableFigures.append({"index": j, "figure": figure})
        if len(availableFigures) > 0:
            return random.choice(availableFigures)["index"]
        else:
            return 0

    def _NewPage(self, sceneType, **kwargs):
        try:
            scene = sceneType.lower()
        except Exception as e:
            print(f"problematic sceneType in type {type(sceneType)}: {sceneType}")
        newPage = None
        if scene == "classroom":
            if "actor" not in kwargs:
                raise Exception(f'argument "actor" is required')
            newPage = ClassroomPage(self, **kwargs)
        elif scene == "exam":
            if "actor" not in kwargs:
                raise Exception(f'argument "actor" is required')
            newPage = ExamPage(self, **kwargs)
        elif scene == "concentrak":
            if "text" not in kwargs:
                raise Exception(f'argument "text" is required')
            newPage = ConcentrakPage(self, **kwargs)
        elif scene == "blackboard":
            if "source" not in kwargs:
                raise Exception(f'argument "source" is required')
            newPage = BlackboardPage(self, **kwargs)
        elif scene == "cover":
            if "source" not in kwargs:
                raise Exception(f'argument "source" is required')
            newPage = CoverPage(self, **kwargs)
        elif scene == "notes":
            if "actor" not in kwargs:
                raise Exception(f'argument "actor" is required')
            newPage = NotesPage(self, **kwargs)
        else:
            print(f"Invalid scenario type {sceneType}, must be one of ('exam', 'notes', 'cover', 'blackboard', 'concentrak', 'classroom')")

        return newPage        

    def createPage(self, sceneType, **kwargs):
        newPage = self._NewPage(sceneType, **kwargs)

        if newPage != None:
            self._pages.append(newPage)

        return newPage

    def createPageAtPos(self, pos, sceneType, **kwargs):
        if pos >= 0 and pos < len(self._pages):
            newPage = self._NewPage(sceneType, **kwargs)
            if newPage != None:
                self._pages.insert(pos, newPage)
        else:
            print("Input pos is out of boundary.")
            newPage = None

        return newPage
    
    def removePageAtPos(self, pos):
        if pos >= 0  and pos < len(self._pages):
            self._pages.pop(pos)

    def getPage(self, pos):
        return self._pages[pos] if (pos >= 0  and pos < len(self._pages)) else None

class Page:
    def __init__(self, type, storyInstance):
        self.story = storyInstance
        self.narrator = storyInstance.narrator
        self.locale = storyInstance.locale
        self.type = type
        self.scene = {}
        self.board = {}
        self.objects = []
        self.interactions = []
        self.subscripts = []
        self.narrations = []
        self.actor = ""

    def _getUserId(self, actor):
        userId = -1
        for i, object in enumerate(self.objects):
            if object["name"].lower() == actor.lower():
                userId = i

        if userId == -1:
            self.objects.append({"name": actor})
            userId = len(self.objects) - 1
        return userId

    def test(self, localOutputPath=LOCAL_DEFAULT_ROOT, fileName="testPage.json", language=DEFAULT_LANGUAGE):
        directory = os.path.join(localOutputPath, self.story.storyId)
        if not os.path.exists(directory):
            os.makedirs(directory)

        language = DEFAULT_LANGUAGE if language == None else language
        scripts = self.exportScripts()
        if self.story._synthesizer != None:
            try:
                for script in scripts:
                    soundFileName = script["sound"]
                    if isinstance(soundFileName, str) and len(soundFileName) > 0:
                        text = script["subscript"][language] if isinstance(script["subscript"], dict) else script["subscript"]
                        alternativeText = None if "alternative" not in script else \
                            (script["alternative"][language] \
                                if isinstance(script["alternative"], dict) \
                                else script["alternative"])
                        narrator = script["narrator"]
                        text = alternativeText if isinstance(alternativeText, str) else text
                        self.story._synthesizer.synthesizeFile(
                                narrator, remove_emojis(text), language, directory, os.path.basename(soundFileName)
                            )
                        localOutputFileName = os.path.join(directory, os.path.basename(soundFileName))

                        if self.story._cosUploader != None:
                            self.story._cosUploader.local2cos(localOutputFileName, self.story.storyId, self.story.audioPath)
            except Exception as e:
                print(f"Page.test failed for {script}\n", e)

        with open(os.path.join(localOutputPath, fileName), "w") as file:
            json.dump(
                self.export(), file, ensure_ascii=False, indent=4, sort_keys=False
            )

    def updateScript(self, pos, text=None, actor=None, alternativeText=None):
        if self.type in ("blackboard", "concentrak", "cover", "classroom"):
            self.updateNarration(pos, text=text, narrator=actor, alternativeText=alternativeText)

    def export(self, voiceOffset, pageId):
        raise NotImplementedError("Subclasses must implement export()")

    def exportScripts(self):
        return self.export()["voices"]

##### 问答页面 #####
class ExamPage(Page):
    def __init__(self, storyInstance, actor, postures=["smilesay"], audio=None, **kwargs):
        super().__init__("exam", storyInstance)
        self.scene = self.story.styles["scenarios"]["exam"]
        self.defaultObject = "exam"
        self.questionSubscripts = [{}]
        self.questionInteractions = []

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.board = kwargs["board"]
            if "content" in self.board and isinstance(self.board["content"], dict):
                boardContent = self.board["content"]
                if "options" in boardContent:
                    for option in (boardContent["options"] if isinstance(boardContent["options"], list) else boardContent["options"][DEFAULT_LANGUAGE]):
                        if has_chinese_char(option):
                            self.subscripts.append(
                                {
                                    "sound": None,
                                    "subscript": option,
                                    "narrator": None
                                }
                            )
            self.objects = kwargs["objects"]
            self.questionInteractions = kwargs["interactions"]
            self.actor, _, _, _, _, _ = get_actors(self.objects)
            for i, interaction in enumerate(self.questionInteractions):
                if isinstance(interaction, dict):
                    if "content" in interaction and \
                        "onResult" in interaction and (interaction["onResult"][0] if isinstance(interaction["onResult"], list) else interaction["onResult"]) == -2:
                        content = interaction["content"]
                        if isinstance(content, dict) and "voice" in content:
                            value = content["voice"]
                            self.questionSubscripts[0]["sound"] = self.soundFile = voices[value]["sound"]
                            self.questionSubscripts[0]["subscript"] = self.board["content"]["question"] if ("content" in self.board and isinstance(self.board["content"], dict) and "question" in self.board["content"]) else ""
                            self.questionSubscripts[0]["narrator"] = self.actor
                            self.questionSubscripts[0]["languages"] = voices[value]["languages"] if "languages" in voices[value] else None
                            self.questionInteractions[i]["content"]["voice"] = 0
                    elif "onResult" in interaction:
                        value = (interaction["onResult"][0] if isinstance(interaction["onResult"], list) else interaction["onResult"])
                        if value > -1:
                            self.correctAnswerId = value
                        if "content" in interaction and isinstance(interaction["content"].get("text", None), str):
                            self.subscripts.append(
                                {
                                    "sound": None,
                                    "subscript": interaction["content"]["text"],
                                    "narrator": None
                                }
                            )
                    elif "type" in interaction and interaction["type"] == "motion" and "figure" in interaction:
                        postures = interaction["figure"]

        else:
            self.actor = actor
            self.soundFile = self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio)
            posture_list = (
                [postures]
                if (isinstance(postures, str) or isinstance(postures, int))
                else postures
            )
            self.interactions.append(
                {
                    "start": "",
                    "duration": "",
                    "position": self.story.styles["positions"]["right-bottom"],
                    "transform": "scale(1.5, 1.5)",
                    "figure": self.story.getUserPostureId(
                        actor, posture_list, keyScenario="half"
                    ),
                    "type": "motion",
                    "actor": self._getUserId(self.actor),
                }
            )

    def setQuestion(self, question, options, answers=None, **kwargs):
        assert isinstance(question, str) or isinstance(question, dict)

        hasChinese = False
        for option in (options if isinstance(options, list) else options[DEFAULT_LANGUAGE]):
            if has_chinese_char(option):
                self.subscripts.append(
                    {
                        "sound": None,
                        "subscript": option,
                        "narrator": None
                    }
                )
                hasChinese = True

        answer_list = None
        if hasChinese:
            if isinstance(answers, dict):
                answer_list = {}
                for locale in answers.keys():
                    answer_list[locale] = [answers[locale]] if not isinstance(answers[locale], list) else answers[locale]
            else:
                answer_list = {DEFAULT_LANGUAGE: [answers] if not isinstance(answers, list) else answers}
            options = options if isinstance(options, dict) else {DEFAULT_LANGUAGE: options}
        else:
            answer_list = [] if answers == None else ([answers] if not isinstance(answers, list) else answers)
            options = options if isinstance(options, list) else options[DEFAULT_LANGUAGE]

        self.board = {
            "content": {
                "fontSize": kwargs["fontSize"] if "fontSize" in kwargs else 20,
                "fontColor": kwargs["fontColor"] if "fontColor" in kwargs else "white",
                "question": question if isinstance(question, dict) else {self.locale: question},
                "options": options,
                "answer": answer_list,
                "colsPerRow": kwargs["colsPerRow"] if "colsPerRow" in kwargs else 1,
            },
            "type": "exam",
            "rect": kwargs["rect"] if "rect" in kwargs else [0, 0, 1, 1],
        }

        self.correctAnswerId = 0
        language = next(iter(options), None) if isinstance(options, dict) else None
        if (isinstance(answer_list, list) and len(answer_list) > 0) or (isinstance(answer_list, dict) and len(answer_list[language]) > 0):
            for i, option in enumerate(options[language] if isinstance(options, dict) else options):
                for entry in (answer_list[language] if (isinstance(options, dict) and isinstance(answer_list, dict)) else answer_list):
                    if entry == option:
                        self.correctAnswerId += 2**i

        self.questionInteractions = []

        # 添加初始化问题语音
        inputSubscript = {
            "sound": self.soundFile,
            "subscript": question if isinstance(question, dict) else {self.locale: question},
            "narrator": self.actor
        }

        # 如果新内容与原内容不同。则需先生成test内容，下一步再更新production上内容
        if self.questionSubscripts[0].get("subscript", None) != (question if isinstance(question, dict) else {self.locale: question}):
            self.questionSubscripts[0]["subscript"] = (question if isinstance(question, dict) else {self.locale: question})
            if isinstance(self.questionSubscripts[0].get("sound", None), str) and (self.questionSubscripts[0]["sound"]) > 0:
                self.questionSubscripts[0]["sound"] = switch_to_test_path(self.questionSubscripts[0]["sound"])
            else:
                self.questionSubscripts[0]["sound"] = self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3")
            self.questionSubscripts[0]["narrator"] = self.actor
            self.questionSubscripts[0].pop("languages", None)

        # 初始化页面行为 onResult: -2
        self.questionInteractions.append(
            {
                "start": "",
                "duration": "",
                "onResult": -2,
                "content": {
                    "popup": 4,
                    "voice": 0,
                    "text": "",
                },
                "actor": self._getUserId(self.defaultObject),
                "type": "talk",
            }
        )

        # 错误答案提示行为 onResult: -1
        self.questionInteractions.append(
            {
                "start": "",
                "duration": "",
                "onResult": -1,
                "content": {
                    "popup": 4,
                    "voice": -1,
                    "text": {DEFAULT_LANGUAGE: "再想想", LANGUAGE_ENG: "Try again"} if "alwaysTruePrompt" not in kwargs
                        else kwargs["alwaysTruePrompt"] if isinstance(kwargs["alwaysTruePrompt"], dict)
                        else {self.locale: kwargs["alwaysTruePrompt"]},
                },
                "actor": self._getUserId(self.defaultObject),
                "type": "talk",
            }
        )

        # 正确答案行为 onResult: 由所有正确答案id计算所得
        if self.correctAnswerId > 0:
            self.questionInteractions.append(
                {
                    "start": "",
                    "duration": "",
                    "onResult": self.correctAnswerId,
                    "content": {"popup": 2, "text": ""},
                    "actor": self._getUserId(self.defaultObject),
                    "type": "talk",
                }
            )

    def setFontSize(self, size):
        if "content" in self.board and isinstance(self.board["content"], dict):
            self.board["content"]["fontSize"] = size

    def setColsPerRow(self, colsPerRow):
        if "content" in self.board and isinstance(self.board["content"], dict):
            self.board["content"]["colsPerRow"] = colsPerRow

    def setRect(self, rect):
        if isinstance(self.board, dict):
            self.board["rect"] = rect

    def setFontColor(self, color):
        if "content" in self.board and isinstance(self.board["content"], dict):
            self.board["content"]["fontColor"] = color

    def addImage(self, source, rect=[0, 0, 1, 1], autoFit=True, uploadToCos=True, caption=None):
        assert len(rect) >= 4 and type(rect) is list
        width, height = Story.getImageSize(next(iter(source.values()), None) if isinstance(source, dict) else source)
        assert width > 0 and height > 0
        assert rect[2] > 0 and rect[3] > 0

        if autoFit:
            # image is wider in ratio
            if width / height > (rect[2] if rect[2] > 1.0 else rect[2]*960) / (rect[3] if rect[3] > 1.0 else rect[3]*540):
                height = round((rect[2] if rect[2] > 1.0 else rect[2]*960) * height / width / (1.0 if rect[3] > 1.0 else 540.0), 3)
                width = rect[2] * 1.0
            # vice versa, rect is wider in ratio
            else:
                width = round((rect[3] if rect[3] > 1.0 else rect[3]*540) * width / height / (1.0 if rect[2] > 1.0 else 960.0), 3)
                height = rect[3] * 1.0
            rect[2] = width
            rect[3] = height

        if "contentList" not in self.board:
            self.board["contentList"] = []
        if  self.story._cosUploader != None and uploadToCos:
            if isinstance(source, dict):
                for key in source:
                    source[key] = self.story._cosUploader.local2cos(source[key], self.story.storyId, self.story.posterPath)
            else:
                source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)
        self.board["contentList"].append(
            {
                "image": source,
                "rect": rect,
                "caption": ""
            }
        )
        if caption != None and len(caption) > 0:
            self.board["contentList"][-1]["caption"] = caption if isinstance(caption, dict) else {self.locale: caption}

    def updateImage(self, pos, source, rect=[0, 0, 1, 1], autoFit=True, uploadToCos=True, caption=None):
        if pos < len(self.board["contentList"]) and pos >= 0:
            assert len(rect) >= 4 and type(rect) is list
            width, height = Story.getImageSize(next(iter(source.values()), None) if isinstance(source, dict) else source)
            assert width > 0 and height > 0
            assert rect[2] > 0 and rect[3] > 0

            if autoFit:
                # image is wider in ratio
                if width / height > (rect[2] if rect[2] > 1.0 else rect[2]*960) / (rect[3] if rect[3] > 1.0 else rect[3]*540):
                    height = round((rect[2] if rect[2] > 1.0 else rect[2]*960) * height / width / (1.0 if rect[3] > 1.0 else 540.0), 3)
                    width = rect[2] * 1.0
                # vice versa, rect is wider in ratio
                else:
                    width = round((rect[3] if rect[3] > 1.0 else rect[3]*540) * width / height / (1.0 if rect[2] > 1.0 else 960.0), 3)
                    height = rect[3] * 1.0
                rect[2] = width
                rect[3] = height

            if  self.story._cosUploader != None and uploadToCos:
                if isinstance(source, dict):
                    for key in source:
                        source[key] = self.story._cosUploader.local2cos(source[key], self.story.storyId, self.story.posterPath)
                else:
                    source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)

            self.board["contentList"][pos] = {
                    "image": update_object(self.board["contentList"][pos]["image"], source, self.locale),
                    "rect": rect,
                    "caption": ""
                }
            
            if caption != None and len(caption) > 0:
                self.board["contentList"][pos]["caption"] = caption if isinstance(caption, dict) else {self.locale: caption}

    def removeImage(self, pos):
        if pos < len(self.board["contentList"]) and pos >= 0:
            self.board["contentList"].pop(pos)

    def export(self, voiceOffset=0, pageId=0.0):
        outInteractions = copy.deepcopy(self.interactions + self.questionInteractions)
        tempSubscripts = copy.deepcopy(self.subscripts + self.questionSubscripts)
        outSubscripts = []
        for subscript in [d for d in tempSubscripts if any(value is not None for value in d.values())]:
            outSubscripts.append(subscript)

        for i, interaction in enumerate(outInteractions):
            if isinstance(interaction, dict) and "content" in interaction:
                content = interaction["content"]
                if isinstance(content, dict) and "voice" in content:
                    value = content["voice"]
                    if value > -1:
                        outInteractions[i]["content"]["voice"] = value + voiceOffset

        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene if isinstance(self.scene, str) else copy.deepcopy(self.scene),
                    "board": copy.deepcopy(self.board),
                    "objects": copy.deepcopy(self.objects),
                    "interactions": outInteractions,
                }
            ],
        }

##### 总结页面 #####
class NotesPage(Page):
    def __init__(self, storyInstance, actor, postures=["smilesay"], endingEffect=True, audio=None, **kwargs):
        super().__init__("notes", storyInstance)
        self.scene = self.story.styles["scenarios"]["notes"]["scene"]
        self.board = self.story.styles["scenarios"]["notes"]["board"]
        self.bullets = []
        self.defaultObject = "notes"

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.board = kwargs["board"]
            self.objects = kwargs["objects"]
            self.interactions = kwargs["interactions"]
            self.actor, actorId, _, _, defaultObject, _ = get_actors(self.objects)
            self.defaultObject = defaultObject if defaultObject != None else self.defaultObject
            html = self.board["content"].get("html", None)
            self.soundFile = self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio)
            self.soundFileLanguages = None
            self.endingEffect = False
            if isinstance(html, dict):
                bullets = {}
                for key in html.keys():
                    bullets[key] = get_bullets_from_html(html[key])
                for i in range(len(bullets[DEFAULT_LANGUAGE])):
                    self.bullets.append({key: bullets[key][i] for key in bullets.keys()})
            elif isinstance(html, str):
                self.bullets = get_bullets_from_html(html)
            endingPos = -1
            for i, interaction in enumerate(self.interactions):
                if isinstance(interaction, dict):
                    if "content" in interaction:
                        content = interaction["content"]
                        if isinstance(content, dict) and "voice" in content:
                            value = content["voice"]
                            if value == 0:
                                self.endingEffect = True
                                endingPos = i
                            elif value > 0:
                                self.soundFile = voices[value]["sound"]
                                self.soundFileLanguages = voices[value]["languages"] if "languages" in voices[value] else None
                                self.interactions[i]["content"]["voice"] = 0
                    elif "type" in interaction and "figure" in interaction:
                        value = interaction["figure"]
                        if interaction["type"] == "motion":
                            postures = value
                        elif interaction["type"] == "talk":
                            if interaction["actor"] == actorId and value > -1: 
                                postures = value
            if endingPos > -1:
                self.interactions.pop(endingPos)

            # Remove content from board, leave template only
            if isinstance(self.board["content"]["html"], dict):
                key = self.board["content"]["html"].keys()[0]
                self.board["content"]["html"] = self.board["content"]["html"][key]
                pattern = r"<ul>(.*?)</ul>"
                text = self.board["content"]["html"]\
                    .replace("</ul><ul>", "")\
                    .replace("</li><li>", "")\
                    .replace("<li>", "")\
                    .replace("</li>", "")
                matches = re.findall(pattern, text, flags=re.DOTALL)
                for match in matches:
                    text = text.replace(match, "{}")
                self.board["content"]["html"] = text

        else:
            self.actor = actor
            self.soundFile = self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio)
            self.endingEffect = endingEffect
            self.soundFileLanguages = kwargs["languages"] if ("languages" in kwargs and isinstance(kwargs["languages"], list)) else None

            posture_list = (
                [postures]
                if (isinstance(postures, str) or isinstance(postures, int))
                else postures
            )
            self.interactions.insert(
                0,
                {
                    "start": "",
                    "duration": "",
                    "position": self.story.styles["positions"]["right-bottom"],
                    "transform": "scale(1.5, 1.5)",
                    "figure": self.story.getUserPostureId(
                        actor, posture_list, keyScenario="half"
                    ),
                    "type": "motion",
                    "actor": self._getUserId(actor),
                },
            )

        self.endingInteraction = {
            "start": "",
            "duration": "",
            "content": {"text": "", "voice": 0},
            "type": "talk",
            "actor": self._getUserId(self.defaultObject),
        }

    def addBullet(self, text):
        self.bullets.append(text if isinstance(text, dict) else {self.locale: text})
        self.soundFileLanguages = None
        if isinstance(self.soundFile, str):
            self.soundFile = switch_to_test_path(self.soundFile)

    def updateBullet(self, pos, text):
        if pos < len(self.bullets) and pos >= 0:
            self.bullets[pos] = update_object(self.bullets[pos], text, self.locale)
        self.soundFileLanguages = None
        if isinstance(self.soundFile, str):
            self.soundFile = switch_to_test_path(self.soundFile)

    def removeBullet(self, pos):
        if pos < len(self.bullets) and pos >= 0:
            self.bullets.pop(pos)
        self.soundFileLanguages = None
        if isinstance(self.soundFile, str):
            self.soundFile = switch_to_test_path(self.soundFile)

    def setEndingEffect(self, on: bool):
        self.endingEffect = on

    def export(self, voiceOffset=0, pageId=0.0):
        bullets_strings = {}
        bullets_subscripts = {}
        for bullet in self.bullets:
            if isinstance(bullet, dict):
                for key in bullet.keys():
                    bullets_strings[key] = f"<li>{bullet[key]}</li>" \
                        if (key not in bullets_strings or bullets_strings[key] == None) \
                        else bullets_strings[key] + f"<li>{bullet[key]}</li>"
                    bullets_subscripts[key] = bullet[key] \
                        if (key not in bullets_subscripts or bullets_subscripts[key] == None) \
                        else bullets_subscripts[key] + "<break time=\"1500ms\"/>" + bullet[key]
            else:
                if self.locale not in bullets_strings:
                    bullets_strings[self.locale] = ""
                if self.locale not in bullets_subscripts:
                    bullets_subscripts[self.locale] = ""
                bullets_strings[self.locale] = f"<li>{bullet}</li>" \
                    if bullets_strings[self.locale] in (None, "") \
                    else bullets_strings[self.locale] + f"<li>{bullet}</li>"
                bullets_subscripts[self.locale] = bullet \
                    if bullets_subscripts[self.locale] in (None, "") \
                    else bullets_subscripts[self.locale] + "<break time=\"1500ms\"/>" + bullet

        outBoard = copy.deepcopy(self.board)
        formatString = outBoard["content"]["html"]
        outBoard["content"]["html"] = {}
        for key in bullets_strings:
            outBoard["content"]["html"][key] = formatString.format(bullets_strings[key])

        tempSubscripts = copy.deepcopy(self.subscripts)
        tempSubscripts.append(
            {
                "sound": self.soundFile,
                "subscript": bullets_subscripts,
                "narrator": self.actor,
            }
        )
        if isinstance(self.soundFileLanguages, list):
            tempSubscripts[-1]["languages"] = self.soundFileLanguages
        outSubscripts = []
        for subscript in [d for d in tempSubscripts if any(value is not None for value in d.values())]:
            outSubscripts.append(subscript)

        outInteractions = copy.deepcopy(self.interactions)
        outInteractions.insert(
            len(outInteractions) - 1,
            {
                "start": "",
                "duration": "",
                "content": {"popup": 4, "voice": len(outSubscripts) - 1, "text": ""},
                "type": "talk",
                "actor": self._getUserId(self.defaultObject),
            },
        )
        for i, interaction in enumerate(outInteractions):
            if isinstance(interaction, dict) and "content" in interaction:
                content = interaction["content"]
                if isinstance(content, dict) and "voice" in content:
                    if content["voice"] > -1:
                        outInteractions[i]["content"]["voice"] += voiceOffset

        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene if isinstance(self.scene, str) else copy.deepcopy(self.scene),
                    "board": outBoard,
                    "objects": copy.deepcopy(self.objects),
                    "interactions": outInteractions + [copy.deepcopy(self.endingInteraction)] \
                        if self.endingEffect \
                        else outInteractions
                }
            ],
        }


##### 概念页面 #####
class ConcentrakPage(Page):
    def __init__(self, storyInstance, text, **kwargs):
        super().__init__("concentrak", storyInstance)
        self.scene = self.story.styles["scenarios"]["concentrak"]
        self.defaultObject = "concentrak"

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.objects = kwargs["objects"]
            self.board = kwargs["board"]
            self.interactions = kwargs["interactions"]
            validSubscriptsOffset = 0
            for i, interaction in enumerate(self.interactions):
                if isinstance(interaction, dict):
                    if "content" in interaction:
                        content = interaction["content"]
                        if isinstance(content, dict):
                            if "popup" in content and "text" in content:
                                text = content["text"]
                                if content["popup"] == 6:
                                    self.subscripts.append(
                                        {
                                            "sound": None,
                                            "subscript": text,
                                            "narrator": None
                                        }
                                    )
                                    validSubscriptsOffset += 1
                                elif content["popup"] == 4 and "voice" in content and content["voice"] > 0:
                                    voice = content["voice"]
                                    if "type" in interaction and interaction["type"] == "talk" and "actor" in interaction:
                                        actor = interaction["actor"]
                                        self.subscripts.append(
                                            {
                                                "sound": voices[voice]["sound"],
                                                "subscript": text,
                                                "narrator": self.objects[actor]["name"]
                                            }
                                        )
                                        if "languages" in voices[voice] and isinstance(voices[voice]["languages"], list):
                                            self.subscripts[-1]["languages"] = voices[voice]["languages"]
                                        self.interactions[i]["content"]["voice"] = len(self.subscripts) - 1 - validSubscriptsOffset
        else:
            self.interactions.append(
                {
                    "start": "",
                    "duration": "",
                    "actor": self._getUserId(self.defaultObject),
                    "content": {"popup": 6, "text": text if isinstance(text, dict) else {self.locale: text}},
                }
            )
        self.offset = len(self.interactions)

    def addNarration(self, text, narrator=None, alternativeText=None, audio=None, **kwargs):
        if alternativeText != None:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio),
                    "subscript": text if isinstance(text, dict) else {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": {self.locale: alternativeText},
                }
            )
            if "languages" in kwargs and isinstance(kwargs["languages"], list):
                self.subscripts[-1]["languages"] = kwargs["languages"]           
        else:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio),
                    "subscript": text if isinstance(text, dict) else {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
            if "languages" in kwargs and isinstance(kwargs["languages"], list):
                self.subscripts[-1]["languages"] = kwargs["languages"]           
        self.interactions.append(
            {
                "start": "",
                "duration": "auto",
                "content": {
                    "popup": 4,
                    "voice": len(self.subscripts) - 1,
                    "text": text if isinstance(text, dict) else {self.locale: text},
                },
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def updateNarration(self, pos, text, narrator=None, alternativeText=None):
        if pos < len(self.subscripts) and pos >= 0:
            self.subscripts[pos]["subscript"] = update_object(self.subscripts[pos]["subscript"], text, self.locale)
            self.interactions[pos+self.offset]["content"]["text"] = update_object(self.interactions[pos+self.offset]["content"]["text"], text, self.locale)
            if alternativeText != None:
                self.subscripts[pos]["alternative"] = update_object(self.subscripts[pos]["alternative"], alternativeText, self.locale)
            self.subscripts[pos]["sound"] = switch_to_test_path(self.subscripts[pos]["sound"])
            
            if narrator != None:
                self.subscripts[pos]["narrator"] = narrator
                self.interactions[pos+self.offset]["actor"] = self._getUserId(narrator)
            self.subscripts[pos].pop("languages", None)

    def removeNarration(self, pos):
        if pos < len(self.subscripts) and pos >= 0:
            self.subscripts.pop(pos)
            self.interactions.pop(pos+self.offset)
            if pos+self.offset < len(self.interactions):
                for i, interaction in enumerate(self.interactions[pos+self.offset:]):
                    self.interactions[i]["content"]["voice"] = interaction["content"]["voice"] - 1

    def export(self, voiceOffset=0, pageId=0.0):
        outInteractions = copy.deepcopy(self.interactions)
        for i, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[i]["content"]["voice"] += voiceOffset

        tempSubscripts = copy.deepcopy(self.subscripts)
        outSubscripts = []
        for subscript in [d for d in tempSubscripts if any(value is not None for value in d.values())]:
            outSubscripts.append(subscript)

        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene if isinstance(self.scene, str) else copy.deepcopy(self.scene),
                    "board": copy.deepcopy(self.board),
                    "objects": copy.deepcopy(self.objects),
                    "interactions": outInteractions,
                }
            ],
        }


##### 黑板页面 #####
class BoardPage(Page):
    def __init__(self, pageType, storyInstance, source, rect=[0, 0, 1, 1], uploadToCos=True, **kwargs):
        assert len(rect) >= 4 and type(rect) is list
        assert pageType in ("cover", "blackboard")
        super().__init__(pageType, storyInstance)
        self.scene = self.story.styles["scenarios"][pageType]
        self.narrator = self.story.narrator
        self.narratorId = -1

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.objects = kwargs["objects"]
            self.board = kwargs["board"]
            self.interactions = kwargs["interactions"]
            self.actor, self.actorId, self.narrator, self.narratorId, _, _ = get_actors(self.objects)
            for i, interaction in enumerate(self.interactions):
                if isinstance(interaction, dict):
                    if "content" in interaction:
                        content = interaction["content"]
                        if isinstance(content, dict) and "popup" in content and content["popup"] == 4 and "text" in content and "voice" in content:
                            text = content["text"]
                            voice = content["voice"]
                            if "type" in interaction and interaction["type"] == "talk" and "actor" in interaction and voice > 0:
                                self.subscripts.append(
                                    {
                                        "sound": voices[voice]["sound"],
                                        "subscript": text,
                                        "narrator": self.narrator if self.narrator != None else self.actor if self.actor != None else self.story.narrator
                                    }
                                )
                                if "languages" in voices[voice] and isinstance(voices[voice]["languages"], list):
                                    self.subscripts[-1]["languages"] = voices[voice]["languages"]                  
                                self.interactions[i]["content"]["voice"] = len(self.subscripts) - 1              

        else:
            if self.story._cosUploader != None and uploadToCos:
                if isinstance(source, dict):
                    for key in source.keys():
                        source[key] = self.story._cosUploader.local2cos(source[key], self.story.storyId, self.story.posterPath)
                else:
                    source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)

            self.board = {"content": {"image": source}, "rect": rect}

    def addNarration(self, text, narrator=None, alternativeText=None, audio=None, **kwargs):
        if alternativeText != None:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio),
                    "subscript": text if isinstance(text, dict) else {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": {self.locale: alternativeText},
                }
            )
            if "languages" in kwargs and isinstance(kwargs["languages"], list):
                self.subscripts[-1]["languages"] = kwargs["languages"]           
        else:
            self.subscripts.append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio),
                    "subscript": text if isinstance(text, dict) else {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
            if "languages" in kwargs and isinstance(kwargs["languages"], list):
                self.subscripts[-1]["languages"] = kwargs["languages"]           
        self.interactions.append(
            {
                "start": "",
                "duration": "auto",
                "content": {
                    "popup": 4,
                    "voice": len(self.subscripts) - 1,
                    "text": text if isinstance(text, dict) else {self.locale: text},
                },
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def updateNarration(self, pos, text, narrator=None, alternativeText=None):
        if pos < len(self.subscripts) and pos >= 0:
            self.subscripts[pos]["subscript"] = update_object(self.subscripts[pos]["subscript"], text, self.locale)
            self.interactions[pos]["content"]["text"] = update_object(self.interactions[pos]["content"]["text"], text, self.locale)
            self.subscripts[pos]["sound"] = switch_to_test_path(self.subscripts[pos]["sound"])
            if alternativeText != None:
                self.subscripts[pos]["alternative"] = update_object(self.subscripts[pos]["alternative"], alternativeText, self.locale)
            if narrator != None:
                self.subscripts[pos]["narrator"] = narrator
                self.interactions[pos]["actor"] = self._getUserId(narrator)
            self.subscripts[pos].pop("languages", None)

    def removeNarration(self, pos):
        if pos < len(self.subscripts) and pos >= 0:
            self.subscripts.pop(pos)
            self.interactions.pop(pos)
            if pos < len(self.interactions):
                for i, interaction in enumerate(self.interactions[pos:]):
                    self.interactions[i]["content"]["voice"] = interaction["content"]["voice"] - 1

    def updateImage(self, source=None, rect=None, autoFit=False, uploadToCos=True):
        if source != None:
            width, height = Story.getImageSize(next(iter(source.values()), None) if isinstance(source, dict) else source)
            assert width > 0 and height > 0
            if  self.story._cosUploader != None and uploadToCos:
                if isinstance(source, dict):
                    for key in source.keys():
                        source[key] = self.story._cosUploader.local2cos(source[key], self.story.storyId, self.story.posterPath)
                else:
                    source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)
                
            self.board["content"]["image"] = update_object(self.board["content"]["image"], source, self.locale)
            if rect != None:
                assert rect[2] > 0 and rect[3] > 0

                if autoFit:
                    # image is wider in ratio
                    if width / height > (rect[2] if rect[2] > 1.0 else rect[2]*960) / (rect[3] if rect[3] > 1.0 else rect[3]*540):
                        height = round((rect[2] if rect[2] > 1.0 else rect[2]*960) * height / width / (1.0 if rect[3] > 1.0 else 540.0), 3)
                        width = rect[2] * 1.0
                    # vice versa, rect is wider in ratio
                    else:
                        width = round((rect[3] if rect[3] > 1.0 else rect[3]*540) * width / height / (1.0 if rect[2] > 1.0 else 960.0), 3)
                        height = rect[3] * 1.0
                    rect[2] = width
                    rect[3] = height
                self.board["rect"] = rect

    def export(self, voiceOffset=0, pageId=0.0):
        outInteractions = copy.deepcopy(self.interactions)
        for i, interaction in enumerate(outInteractions):
            if isinstance(interaction, dict) and "content" in interaction:
                content = interaction["content"]
                if isinstance(content, dict) and "voice" in content:
                    value = content.get("voice", -1)
                    if value > -1:
                        outInteractions[i]["content"]["voice"] = value + voiceOffset

        tempSubscripts = copy.deepcopy(self.subscripts)
        outSubscripts = []
        for subscript in [d for d in tempSubscripts if any(value is not None for value in d.values())]:
            outSubscripts.append(subscript)

        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene if isinstance(self.scene, str) else copy.deepcopy(self.scene),
                    "board": copy.deepcopy(self.board),
                    "objects": copy.deepcopy(self.objects),
                    "interactions": outInteractions,
                }
            ],
        }


##### 黑板页面 #####
class BlackboardPage(BoardPage):
    def __init__(self, storyInstance, source, rect=[0, 0, 1, 1], uploadToCos=True, **kwargs):
        pageType = "blackboard"
        super().__init__(pageType, storyInstance, source, rect, uploadToCos, **kwargs)


##### 封面页面 #####
class CoverPage(BoardPage):
    def __init__(self, storyInstance, source, rect=[0, 0, 1, 1], uploadToCos=True, **kwargs):
        pageType = "cover"
        super().__init__(pageType, storyInstance, source, rect, uploadToCos, **kwargs)


##### 教室页面 #####
class ClassroomPage(Page):
    def __init__(self, storyInstance, actor, postures=["smilesay"], **kwargs):
        super().__init__("classroom", storyInstance)
        self.scene = self.story.styles["scenarios"]["classroom"]
        self.narrations = {"subscripts": [], "interactions": []}
        self.hasImage = False

        if all(key in kwargs for key in ("voices", "board", "objects", "interactions")):
            voices = kwargs["voices"]
            self.objects = kwargs["objects"]
            self.board = kwargs["board"]
            if "rect" in self.board and isinstance(self.board["rect"], list):
                self.hasImage = True
            for i, interaction in enumerate(kwargs["interactions"]):
                if isinstance(interaction, dict):
                    if (("onResult" in interaction and (interaction["onResult"][0] if isinstance(interaction["onResult"], list) else interaction["onResult"]) == 1) \
                        or ("onPoster" in interaction and (interaction["onPoster"][0] if isinstance(interaction["onPoster"], list) else interaction["onPoster"]) == 1)) \
                        and "type" in interaction and interaction["type"] == "talk" and "actor" in interaction and "content" in interaction:
                        actor = interaction["actor"]
                        content = interaction["content"]
                        if isinstance(content, dict) and "text" in content and "voice" in content and content["voice"] > 0:
                            text = content["text"]
                            voice = content["voice"]
                            self.narrations["subscripts"].append(
                                {
                                    "sound": voices[voice]["sound"],
                                    "subscript": text,
                                    "narrator": self.objects[actor]["name"]
                                }
                            )
                            if "languages" in voices[voice] and isinstance(voices[voice]["languages"], list):
                                self.narrations["subscripts"][-1]["languages"] = voices[voice]["languages"]
                            interaction["content"]["voice"] = len(self.narrations["subscripts"]) - 1
                            self.narrations["interactions"].append(interaction)
                    elif "type" in interaction and interaction["type"] == "talk" and "actor" in interaction and "content" in interaction:
                        actor = interaction["actor"]                        
                        content = interaction["content"]
                        if isinstance(content, dict) and "text" in content and "voice" in content and content["voice"] > 0:
                            text = content["text"]
                            voice = content["voice"]   
                            self.interactions.append(interaction)
                            self.subscripts.append({
                                "sound": voices[voice]["sound"],
                                "subscript": text,
                                "narrator": self.objects[actor]["name"]
                            })
                            if "languages" in voices[voice] and isinstance(voices[voice]["languages"], list):
                                self.subscripts[0]["languages"] = voices[voice]["languages"]
                            self.interactions[-1]["content"]["voice"] = len(self.subscripts) - 1
        else:
            posture_list = (
                [postures]
                if (isinstance(postures, str) or isinstance(postures, int))
                else postures
            )
            self.subscripts.append({
                "sound": "",
                "subscript": None,
                "narrator": actor,
            }),
            self.interactions.append({
            
                "start": "",
                "duration": "",
                "content": {
                    "popup": self.story.styles["popup"],
                    "voice": 0,
                    "text": {self.locale: ""},
                },
                "figure": self.story.getUserPostureId(
                    actor, posture_list, keyScenario="-stand-"
                ),
                "position": self.story.styles["positions"][
                    "left" if actor == "boy" else "right"
                ],
                "transform": f'scale({self.story.styles["scale"]}, {self.story.styles["scale"]})',
                "type": "talk",
                "actor": self._getUserId(actor),
            })
            self.actor = actor

    def setDialog(self, text, alternativeText=None, **kwargs):
        self.subscripts[0]["subscript"] = text if isinstance(text, dict) else {self.locale: text}
        if isinstance(self.subscripts[0]["sound"], str) and len(self.subscripts[0]["sound"]) > 0:
            self.subscripts[0]["sound"] = switch_to_test_path(self.subscripts[0]["sound"])
        else:
            self.subscripts[0]["sound"] = self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3")
        if "languages" in kwargs and isinstance(kwargs["languages"], list):
            self.subscripts[0]["languages"] = kwargs["languages"]
        else:
            self.subscripts[0].pop("languages", None)     
        if alternativeText != None:
            self.subscripts[0]["alternativeText"] = alternativeText if isinstance(alternativeText, dict) else {self.locale: alternativeText}
        self.interactions[0]["content"]["text"] = text if isinstance(text, dict) else {self.locale: text}

    def setImage(self, source, rect=[0.2, 0.2, 400, 400], autoFit=True, uploadToCos=True, **kwargs):
        assert len(rect) >= 4 and type(rect) is list
        width, height = Story.getImageSize(next(iter(source.values()), None) if isinstance(source, dict) else source)
        assert width > 0 and height > 0
        assert rect[2] > 0 and rect[3] > 0

        if autoFit:
            # image is wider in ratio
            if width / height > (rect[2] if rect[2] > 1.0 else rect[2]*960) / (rect[3] if rect[3] > 1.0 else rect[3]*540):
                height = round((rect[2] if rect[2] > 1.0 else rect[2]*960) * height / width / (1.0 if rect[3] > 1.0 else 540.0), 3)
                width = rect[2] * 1.0
            # vice versa, rect is wider in ratio
            else:
                width = round((rect[3] if rect[3] > 1.0 else rect[3]*540) * width / height / (1.0 if rect[2] > 1.0 else 960.0), 3)
                height = rect[3] * 1.0
            rect[2] = width
            rect[3] = height

            if self.actor == "boy":
                if rect[2] > 1.0:
                    rect[0] = round(((1 - rect[0]) if rect[0] <= 1.0 else rect[0]/960.0) - rect[2]/960.0, 3)
                elif rect[2] < 1.0:
                    rect[0] = ((1 - rect[0]) if rect[0] <= 1.0 else rect[0]/960.0) - rect[2]

        if self.story._cosUploader != None and uploadToCos:
            if isinstance(source, dict):
                for key in source.keys():
                    source[key] = self.story._cosUploader.local2cos(source[key], self.story.storyId, self.story.posterPath)
            else:
                source = self.story._cosUploader.local2cos(source, self.story.storyId, self.story.posterPath)

        self.board = {
            "content": {
                "caption": kwargs["caption"] if "caption" in kwargs else "",
                "fontSize": kwargs["fontSize"] if "fontSize" in kwargs else "24px",
                "fontColor": kwargs["fontColor"] if "fontColor" in kwargs else "white",
                "image": source,
                "magnify": True,
                "border": self.story.styles["frame"],
            },
            "rect": rect,
        }
        self.hasImage = True

    def setVideo(self, source, autoFit=True, rect=[0.1, 0.1, 640, 360], **kwargs):
        assert len(rect) >= 4 and type(rect) is list

        if autoFit and self.actor == "boy":
            if rect[2] > 1.0:
                rect[0] = round(0.9 - rect[2]/0.9, 3)
            elif rect[2] < 1.0:
                rect[0] = 0.9 - rect[2]

        self.board = {
            "content": {
                "caption": kwargs["caption"] if "caption" in kwargs else "",
                "fontSize": kwargs["fontSize"] if "fontSize" in kwargs else "24px",
                "fontColor": kwargs["fontColor"] if "fontColor" in kwargs else "white",
                "src": source,
                "border": self.story.styles["frame"],
            },
            "rect": rect,
        }
        if "videoType" in kwargs:
            self.board["content"]["videoType"] = kwargs["videoType"].lower()
        self.hasImage = True

    def addNarration(self, text, narrator=None, alternativeText=None, audio=None, **kwargs):
        if alternativeText != None:
            self.narrations["subscripts"].append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio),
                    "subscript": text if isinstance(text, dict) else {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                    "alternative": alternativeText if isinstance(alternativeText, dict) else {self.locale: alternativeText},
                }
            )
            if "languages" in kwargs and isinstance(kwargs["languages"], list):
                self.subscripts[-1]["languages"] = kwargs["languages"]           
        else:
            self.narrations["subscripts"].append(
                {
                    "sound": self.story.getAudioPath(f"voice-{uuid.uuid4()}.mp3" if audio == None else audio),
                    "subscript": text if isinstance(text, dict) else {self.locale: text},
                    "narrator": narrator if narrator != None else self.narrator,
                }
            )
            if "languages" in kwargs and isinstance(kwargs["languages"], list):
                self.subscripts[-1]["languages"] = kwargs["languages"]           
        self.narrations["interactions"].append(
            {
                "start": "",
                "duration": "auto",
                "content": {
                    "popup": 4,
                    "voice": len(self.narrations["subscripts"]) - 1,
                    "text": text if isinstance(text, dict) else {self.locale: text},
                },
                "onPoster": 1,
                "actor": self._getUserId(
                    narrator if narrator != None else self.narrator
                ),
                "type": "talk",
            }
        )

    def updateDialog(self, text=None, alternativeText=None):
        if text != None:
            self.subscripts[0]["subscript"] = update_object(self.subscripts[0]["subscript"], text, self.locale)
        if alternativeText != None:
            self.subscripts[0]["alternative"] = update_object(self.subscripts[0]["alternative"] \
                                                                if "alternative" in self.subscripts[0] \
                                                                else {}, \
                                                                alternativeText, self.locale)
        self.subscripts[0]["sound"] = switch_to_test_path(self.subscripts[0]["sound"])
        self.subscripts[0].pop("languages", None)

    def updateNarration(self, pos, text, narrator=None, alternativeText=None):
        if pos < len(self.narrations["subscripts"]) and pos >= 0:
            self.narrations["subscripts"][pos]["subscript"] = update_object(self.narrations["subscripts"][pos]["subscript"], text, self.locale)
            self.narrations["interactions"][pos]["content"]["text"] = update_object(self.narrations["interactions"][pos]["content"]["text"], text, self.locale)
            if alternativeText != None:
                self.narrations["subscripts"][pos]["alternative"] = update_object(self.narrations["subscripts"][pos]["alternative"], alternativeText, self.locale)
            
            if narrator != None:
                self.narrations["subscripts"][pos]["narrator"] = narrator
                self.narrations["interactions"][pos]["actor"] = self._getUserId(narrator)
            self.narrations["subscripts"][pos]["sound"] = switch_to_test_path(self.narrations["subscripts"][pos]["sound"])
            self.narrations["subscripts"][pos].pop("languages", None)

    def removeNarration(self, pos):
        if pos < len(self.narrations["subscripts"]) and pos > 0:
            self.narrations["subscripts"].pop(pos)
            self.narrations["interactions"].pop(pos)
            if pos < len(self.narrations["interactions"]):
                for i, interaction in enumerate(self.narrations["interactions"][pos:]):
                    self.narrations["interactions"][i]["content"]["voice"] = interaction["content"]["voice"] - 1

    def export(self, voiceOffset=0, pageId=0.0):
        tempSubscripts = copy.deepcopy(self.subscripts)
        outInteractions = copy.deepcopy(self.interactions)
        outNarrations = copy.deepcopy(self.narrations)

        if self.hasImage:
            for i, interaction in enumerate(outInteractions):
                if interaction["type"] != "motion":
                    outInteractions[i]["duration"] = "auto"
                    outInteractions[i]["content"]["popup"] = 4

        narrationOffset = len(tempSubscripts)
        tempSubscripts = tempSubscripts + outNarrations["subscripts"]

        outSubscripts = []
        for subscript in [d for d in tempSubscripts if any(value is not None for value in d.values())]:
            outSubscripts.append(subscript)

        for i, interaction in enumerate(outNarrations["interactions"]):
            outNarrations["interactions"][i]["content"]["voice"] = outNarrations["interactions"][i]["content"]["voice"] + narrationOffset
            outInteractions.append(outNarrations["interactions"][i])

        for j, interaction in enumerate(outInteractions):
            if (
                "content" in interaction
                and interaction["content"].get("voice", -1) >= 0
            ):
                outInteractions[j]["content"]["voice"] = outInteractions[j]["content"]["voice"] + voiceOffset
        return {
            "voices": outSubscripts,
            "events": [
                {
                    "id": pageId,
                    "scene": self.scene if isinstance(self.scene, str) else copy.deepcopy(self.scene),
                    "board": copy.deepcopy(self.board),
                    "objects": copy.deepcopy(self.objects),
                    "interactions": outInteractions,
                }
            ],
        }
