
class Notification:
    def __init__(self, components: list[dict], percentage: int | float):
        self.components: list = components
        self.__percentage_difference: str = f"{percentage}%"
        self.__message_text: str = f"You might want take a look a the following stock news\n\n \
        ---Stock Market Updates--- \n\n Apple stocks raised by: {self.__percentage_difference} \n\n"
        self.__create_text()

    def __create_text(self):
        for component in self.components:
            self.__message_text += component["title"] + "\n"
            self.__message_text += component["description"] + "\n"
            self.__message_text += component["url"] + "\n\n"

    def get_text(self):
        return self.__message_text

