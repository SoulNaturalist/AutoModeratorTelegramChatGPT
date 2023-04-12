"""
Main easiyer way to automoderation
"""

class AutoModeration:
  def __init__(self, openai_token: str, ban_words: list, delete: bool, ban: bool) -> None:
    self.openai_token = openai_token
    self.ban_words = ban_words
    self.delete = delete
    self.ban = ban
  def gen_context_msg_gpt(self) -> str:
    if self.ban_words:
      return """Hi, read this message\n{0} and if it contains at least one word of their list - {1}\nAlso, do you think this message is spam?, say yes or no"""
    else:
      return """Determine whether this message is spam or not, if yes, write yes in the answer"""
