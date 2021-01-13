'''
@Author: Pawn
@Date: 2020-08-19
@Description: example for module TTS
@FilePath: example_tts_file.py
'''
import log
from audio import TTS

# 设置日志输出级别
log.basicConfig(level=log.INFO)   
tts_Log = log.getLogger("TTS")

#  参数1：device （0：话筒，1：耳机，2：喇叭）
tts = TTS(1)

# 获取当前播放音量大小
volume_num = tts.getVolume()
tts_Log.info("Current TTS volume is %d" %volume_num)

# 设置音量为6
volume_num = 6   
tts.setVolume(volume_num)
#  参数1：优先级 (0-4)
#  参数2：打断模式，0表示不允许被打断，1表示允许被打断
#  参数3：模式 （1：UNICODE16(Size end conversion)  2：UTF-8  3：UNICODE16(Don't convert)）
#  参数4：数据字符串 （待播放字符串）
tts.play(1, 1, 2, 'QuecPython') # 执行播放
 
tts.close()   # 关闭TTS功能