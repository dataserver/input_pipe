import os

from utils.langutils import save_fetch

cfg = globals()["config"]
drv = globals()["drivers"]
print(drv)

os.system("vlc --play-and-exit --intf dummy /home/werpu/PycharmProjects/" +
          "input_pipe/src/test/resources/Mudchute_cow_1.ogg")
