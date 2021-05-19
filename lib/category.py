class Category:

    def __init__(self, index: int, name: str, accepted: bool):
        self.__id = index
        self.__name = name
        self.__accepted = accepted

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_accepted(self) -> bool:
        return self.__accepted


class CategoryCollection:

    def __init__(self):
        self.__categories = []

    def push(self, category: Category) -> None:
        self.__categories.append(category)

    def get(self, index: int) -> Category:
        for c in self.__categories:
            if c.id == index:
                return c
        return Category(0, '', False)

    @staticmethod
    def from_model(labels_file: str, include: list = ()):
        collection = CategoryCollection()
        with open(labels_file, 'r') as labels:
            for index, val in enumerate(labels):
                if index == 0:
                    continue
                cls = val[:-1]
                if cls == '???':
                    continue
                accepted = len(include) > 0 and cls not in include
                category = Category(index - 1, cls, accepted)
                collection.push(category)

        return collection
