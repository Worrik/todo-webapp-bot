from aiogram.types.message_entity import MessageEntity
from aiogram.utils.text_decorations import HtmlDecoration


class HtmlDecorationTodo(HtmlDecoration):
    def apply_entity(self, entity: MessageEntity, text: str) -> str:
        if entity.type == "url":
            return self.link(text, text)
        if entity.type == "mention":
            return self.link(text, f"https://t.me/{text[1:]}")
        if entity.type == "phone_number":
            return self.link(text, f"tel:{text}")
        return super().apply_entity(entity, text)


html_decoration = HtmlDecorationTodo()
