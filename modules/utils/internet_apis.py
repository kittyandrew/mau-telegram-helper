from PyBinglate import BingTranslator, LANGUAGES
from google.cloud.vision import types
from apiclient.discovery import build
from google.cloud import translate
from google.cloud import vision
import config as c
import requests
import random
import html


class YouTubeAPI:


    youtubeAPI = build('youtube', 'v3', developerKey=c.YOUTUBE_API_KEY)

    def __init__(self):
        pass

    @classmethod
    def searh_into_hyperlink(cls, name, name_auto_correct=False):
        result = cls.search_video(name)
        if result[0]:
            if name_auto_correct:
                link_text = f'<a href="{result[1]}">{result[2]}</a>'
            else:
                link_text = f'<a href="{result[1]}">{name}</a>'
        else:
            link_text = f"Failed ({result[1]})"
        return link_text

    @classmethod
    def search_video(cls, name):
        try:
            x = cls.youtubeAPI.search().list(q=name, part="snippet", type='video', maxResults=50).execute()['items']
            video_id = x[0]["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            title = x[0]["snippet"]["title"]
        except Exception as e:
            if type(e) == IndexError:
                return False, "Не найдено видео по вашему запросу!", None
            print(f"ERROR: {e} \\\\")
            return False, "YouTube search request went unsuccesful", None
        return True, url, title


class InstagramAPI:

    main_url = "https://www.instagram.com"

    def __init__(self):
        pass

    @classmethod
    def search_profile_into_hyperlink(cls, name):
        result = cls.search_profile(name)
        if result[0] == 'no such profile':
            return result[0], None
        elif result[0]:
            url_text = f'<a href="{result[1]}">{name}</a>'
            return True, url_text
        else:
            return False, None


    @classmethod
    def search_profile(cls, name):
        url = f"{cls.main_url}/{name}"

        try:
            x = requests.get(url)
            if x.ok:
                return True, url
            else:
                return 'no such profile', "Error - could find profile with this username."
        except Exception as e:
            print(e)
            return False, "Error while searching for instagram profile."


class GoogleAPI:

    def __init__(self):
        pass

    @classmethod
    def google_translate(cls, text, target='en'):
        try:
            google_tr = translate.Client(credentials=c.google_creds)
            GOOGLE_LANGUAGES = google_tr.get_languages(target_language=target)
            trans = google_tr.translate(text, target_language=target)
            tr_text = trans['translatedText']
            tr_text = html.unescape(tr_text)
            x = trans['detectedSourceLanguage']
            for lang in GOOGLE_LANGUAGES:
                if lang['language'] == x:
                    language = lang['name']
                    break
            try:
                language = f"{language[0].upper()}{language[1:]}"
            except:
                raise MyGoogleAPIError("There is no such language.. // What?")

            result = f"{language}:\n{tr_text}"
            return result

        except Exception as e:
            raise MyGoogleAPIError(f"Google Translation API Error ({e})")


    @classmethod
    def user_friendly_response(cls, img_in_bytes):
        result_list = cls.analyze_photo(img_in_bytes)
        x = len(result_list)
        if x == 0:
            result = "Couldn't recognize anything.."
        elif x > 0:
            result = f"Recognized: {', '.join(result_list)}."
        else:
            raise MyGoogleAPIError(f"GoogleAPI.user_friendly couldn't find correct respond sample.")

        return result


    @classmethod
    def analyze_photo(cls, img_in_bytes):
        vision_client = cls.get_client()
        image = types.Image(content=img_in_bytes)
        response = vision_client.label_detection(image=image)
        labels = response.label_annotations
        result = []
        for label in labels:
            result.append(label.description)
        return result

    @classmethod
    def get_client(cls):
        try:
            # credentials=c.google_creds
            # TODO: .from_service_account_file()
            client = vision.ImageAnnotatorClient()
            return client
        except Exception as e:
            print(e)
            raise e



class MyBingTranslator:

    def __init__(self):
        pass

    @classmethod
    def translate(cls, text, lang='en', tell_input_lang=False):
        try:
            tr = BingTranslator()
            try:
                translation = tr.translate(text, lang, raw=tell_input_lang)
            except:
                translation = tr.translate(text, 'en', raw=tell_input_lang)
            if tell_input_lang:
                from_lang = translation[0]['detectedLanguage']['language']
                from_lang = LANGUAGES[from_lang]
                from_lang = tr.translate(from_lang, lang)
                from_lang = f'{from_lang[0].upper()}{from_lang[1:]}'

                tr_text = translation[0]['translations'][0]['text']
                tr_text = html.unescape(tr_text)
                translation_and_lang = f"{from_lang}:\n{tr_text}"
                return translation_and_lang
            else:
                tr_text = html.unescape(tr_text)
                return translation
        except Exception as e:
            print(e)
            raise MyBingError(f"BingTranslator failed with error >>> {e}")

# Custom errors
class MyBingError(Exception):
    pass

class MyGoogleAPIError(Exception):
    pass
