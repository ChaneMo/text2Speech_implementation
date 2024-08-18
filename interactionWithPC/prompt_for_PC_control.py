import pyttsx3
import openai
import speech_recognition as sr
from automation.open_chrome import open_website
from automation.web_address import web_dic
from automation.open_search import open_search

# 使用默认麦克风
recognizer = sr.Recognizer()
microphone = sr.Microphone()
# 初始化tts引擎
engine = pyttsx3.init()
# 设置发音人的语音
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)
openai.api_key = "Your api key"
openai.api_base = "Your api base"

while True:
    with microphone as source:
        print("请开始说话...")
        audio = recognizer.listen(source)

    try:
        # 将音频转换为文字
        print('语音识别中...')
        text = recognizer.recognize_google(audio, language='zh-CN')
        print(f"你说了：{text}")
        if '小娜' not in text:
            continue
        # 要转换的文本
        prompt = (f"你是一个强大的私人电脑管家，名字叫小娜。你可以使用谷歌浏览器打开用户指定的网站（B站、百度、谷歌中的其中一个），也可以使用谷歌浏览器搜索用户指定的内容。"
                  f"用户给你的指令将以三个井号符合进行分隔，你需要根据用户的需求返回对应的回答格式。如果用户需要你打开指定的网站，你需要返回‘打开网站|网站名称’的答复格式；"
                  f"如果用户需要你帮助他搜索指定内容，你需要返回‘搜索|待搜索内容’的答复格式；如果用户输入的指令既不是打开指定网站也不是搜索指定内容，则你需要以尊敬的态度回复用户的对话，"
                  f"返回答复的格式为‘问答|你的回复’，需要注意的是，你回复的文字应当在50个汉字以内。以下是用户的指令：###{text}###，请务必返回指定格式的答复。"
                  f"另外，如果用户与你说再见，则你只需要需要返回‘退出程序|你的告别语’即可。")
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        response = chat_completion.choices[0].message.content
        print(response)
        response = response.strip('(')
        response = response.strip(')')
        response = response.strip('（')
        response = response.strip('）')
        response = response.strip("'")
        print(response)
        order_type, answer = response.split('|')[0], response.split('|')[1]
        if '问答' in order_type:
            # 将文本转换为语音
            engine.say(answer)
            # 播放声音
            engine.runAndWait()
        elif '打开网站' in order_type:
            if answer not in web_dic:
                answer = '谷歌'
            address = web_dic[answer]
            open_website(address)
        elif '搜索' in order_type:
            browser = 'https://www.google.com'
            open_search(browser, answer)
        elif '退出程序' in order_type:
            # 将文本转换为语音
            engine.say(answer)
            # 播放声音
            engine.runAndWait()
            break
    except sr.UnknownValueError:
        print("未识别出触发词")
    except sr.RequestError as e:
        print(f"识别服务出错； {e}")
