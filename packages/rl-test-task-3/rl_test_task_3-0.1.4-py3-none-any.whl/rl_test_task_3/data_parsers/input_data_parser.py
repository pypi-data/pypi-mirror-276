class InputDataParser:
    __id: int = 0

    def get_parsed_data(self, data: str) -> dict[int, str]:
        parsed_data: dict[int, str] = {}

        lines: list[str] = data.split('\n')

        for line in lines:
            key, value = self.__get_parts(line)
            parsed_data[key] = value

        return parsed_data

    def __get_parts(self, line: str) -> tuple[int, str]:
        key: int = self.__id
        value: str = line

        self.__id = self.__id + 1

        return (key, value)
