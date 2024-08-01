# -*- Encoding:UTF-8 -*-
import pyttsx3
import openai
import random
import speech_recognition as sr


# 使用默认麦克风
recognizer = sr.Recognizer()
microphone = sr.Microphone()
# 初始化tts引擎
engine = pyttsx3.init()
# 设置发音人的语音
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)
openai.api_key = ""
openai.api_base = ""

# 持续识别语音，直到用户输入退出指令
while True:
    with microphone as source:
        print("请开始说话...")
        audio = recognizer.listen(source)

    try:
        # 将音频转换为文字
        print('语音识别中...')
        text = recognizer.recognize_google(audio, language='zh-CN')
        print(f"你说了：{text}")
        # 要转换的文本
        if '嘿小娜' == text:
            responses = ['您好，有什么可以帮您的吗？', '在呢！有什么吩咐？', '需要我做些什么？']
            response = random.choice(responses)
            # 将文本转换为语音
            engine.say(response)
            # 播放声音
            engine.runAndWait()
        elif '嘿小娜' in text and '再见' not in text:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system",
                           "content": "你是一个私人的电脑语音助手，名字叫小娜，你将以尊敬的语气回答你主人提出的问题。请注意，输入给你的文本是麦克风语音转化成的汉语文本，没有标点符号，你需要根据语境进行标点符号位置的判断从而理解语义，并回答相应的问题。需要注意的是，你回答的文字应当在50个汉字以内。"},
                          {"role": "user", "content": text}]
            )
            response = chat_completion.choices[0].message.content
            # 将文本转换为语音
            engine.say(response)
            # 播放声音
            engine.runAndWait()
        if '嘿小娜' in text and '再见' in text:
            engine.say('下次见！')
            # 播放声音
            engine.runAndWait()
            break
    except sr.UnknownValueError:
        print("未识别出触发词")
    except sr.RequestError as e:
        print(f"识别服务出错； {e}")


