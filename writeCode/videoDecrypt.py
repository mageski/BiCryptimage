
from .videoStegano.videoDecode import VideoDecode
from .saveService.Externalservice import SaveReadService

class VideoDecrypt:
    @classmethod
    def decrypt(cls, imageIn, password, location):
        try:
            frames, fps = SaveReadService.TakeVide(imageIn, True)
        except:
            return "error with video file can't take frame"
        try:
            vid2 = VideoDecode(frames)
        except:
            return "error with transform frame into image class "
        err = vid2.extract(password, location)
        return err
