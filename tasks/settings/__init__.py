from .settings import *
if not DEBUG:
    try:
        from .prod import *
    except:
        pass
