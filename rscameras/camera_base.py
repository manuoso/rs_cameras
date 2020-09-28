import os
import json

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))

class TypeExcept(Exception):
    pass

####################################################################################################
class Camera_Base():
    def __init__(self, config = None):
        if config is not None:
            self.config = config
        else:
            self.config = REPO_ROOT + "/config.json"
        
        self.__configure()

    # ----------------------------------------------------------------------------------------------------
    def __configure(self):
        with open(self.config) as f:
            self.data = json.load(f)

####################################################################################################
if __name__ == '__main__':  # Test
    camera = Camera_Base()
