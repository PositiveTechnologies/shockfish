import logging
import shockfish.protectors as Protectors
from shockfish.events import Attack, AttackException

logger = logging.getLogger("engine")

class Engine:

    def __init__(self, protectors, config):
        self.config = config
        self.protectors = [Protectors.ZeroProtector]
        self.protectors.extend(protectors)
        self.protectors = sorted(self.protectors, key=lambda protector: protector._priority)

    def process(self, request):
        for protector in self.protectors:
            config = self.config.protectors.get(protector.__name__)
            protector_obj = protector(request, config)
            protector_obj.run()


class EngineFactory:

    @staticmethod
    def buildEngine(flows, config):
        loaded = []
        all_protectors = config.protectors
        
        for name,options in all_protectors.items():
            if options == "off":
                logger.debug(name  + " protector is disabled")
                continue
            else:
                if hasattr(Protectors, name):
                    protector = getattr(Protectors, name)
                    if protector._type in flows:
                        loaded.append(protector)
                        logger.debug(name  + " protector is loaded ")

        return Engine(loaded, config)

