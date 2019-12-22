from ycloud import auth
from ycloud import components


class API:
    def __init__(self, auth: auth):
        self.auth = auth
        t = self.inheritors(components.Component)
        self.__dict__.update(t)

    def inheritors(self, className):
        subclasses = {}
        parentClassList = [className]
        while parentClassList:
            parent = parentClassList.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses[child.COMPONENT_NAME] = child(self.auth)
                    parentClassList.append(child)
        return subclasses
