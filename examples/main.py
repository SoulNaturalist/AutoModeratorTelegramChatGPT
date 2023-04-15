import openai
from googletrans import Translator
from aiogram import Bot, Dispatcher, executor, types

"""
Main easiyer way to automoderation
"""

class AutoModeration:
  translator = Translator()

  def __init__(self, openai_token: str, ban_words: list, ban: bool, language: str) -> None:
    self.openai_token = openai_token
    self.ban_words = ban_words
    self.ban = ban
    self.language = language

  def gen_context_msg_gpt(self) -> str:
    if self.ban_words:
      return """Hi, read this message\n{0} and if it contains at least one word of their list - {1}\nAlso, do you think this message is spam?, say yes or no"""
    else:
      return """Determine whether this message is spam or not, if yes, write yes in the answer"""
  def send_question_chatgpt(self, msg: str) -> bool:
    pre_message = self.gen_context_msg_gpt(self).format(msg, self.ban_words)
    if self.language == "ru":
      content_to_chatgpt = self.translator.translate(pre_message, src="ru", dest="en").text
      messages = [{"role": "user", "content": content_to_chatgpt}]
      chatgpt_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
      return "Да" in chatgpt_response
    else:
      messages = [{"role": "user", "content": pre_message}]
      chatgpt_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
      return "Yes" in chatgpt_response

class TelegramBot:
  def __init__(self, telegram_token) -> None:
    self.telegram_token = telegram_token
  def start(self):
    bot = Bot(token=self.telegram_token)
    dp = Dispatcher(bot)
    
    @dp.message_handler(chat_type=types.ChatType.PRIVATE)
    async def spam_handler(msg: types.Message):
      moderation_class = AutoModeration("openai_token", ["bruh"], True, "ru")
      is_spam = moderation_class.send_question_chatgpt(msg.text)
      if is_spam and moderation_class.ban:
        #Deleted the message and ban user if ban is True
        pass
      elif is_spam:
        #Deleted the message
        pass
    executor.start_polling(dp)


if __name__ == "__main__":
  TelegramBot("token").start()

