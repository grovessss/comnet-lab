import numpy as np
import os
from demo import RequestApi
import jiagu
import time
from textrank4zh import TextRank4Keyword, TextRank4Sentence


video_path = '访谈类测试视频.mp4'
output_path = 'output1.mp4'
APP_ID = '9ee34da4'
SECRET_KEY = 'd23bf17205de4a0dc7819bb827fdc5fb'
text_list_path = 'text_list1.txt'


# 提取音频
os.system('ffmpeg -i '+ video_path +' -vn audio.wav')


# 语音识别
if os.path.exists(text_list_path) is False:
    assert(False)
    api = RequestApi(appid=APP_ID, secret_key=SECRET_KEY, upload_file_path='audio.wav')
    res = api.all_api_request()
    text_list = eval(res['data'])
    fw = open(text_list_path, 'w')
    fw.write(str(text_list))
    fw.close()
else:
    fr = open(text_list_path, 'r')
    text_list = eval(fr.readlines()[0])

begin_timepoints = [int(text['bg']) for text in text_list]
end_timepoints = [int(text['ed']) for text in text_list]
speakers = [int(text['speaker']) for text in text_list]

text_accum_len = [0]
for text in text_list[:-1]:
    text_accum_len.append(text_accum_len[-1] + len(text['onebest']))

alltext = "".join([text['onebest'] for text in text_list])


# 文本摘要
tr4s = TextRank4Sentence(delimiters=['。','！','？','…','，'])
tr4s.analyze(text=alltext, lower=True, source = 'all_filters')
summarize = tr4s.get_key_sentences()

begins = np.array([])
ends = np.array([])
for summ in summarize:
    char_idx = alltext.index(summ['sentence'])
    text_idx_bg = np.max(np.argwhere(np.array(text_accum_len)<=char_idx))
    while text_idx_bg > 0 and ((begin_timepoints[text_idx_bg]-end_timepoints[text_idx_bg-1]) < 50):
        text_idx_bg = text_idx_bg - 1
    begins = np.append(begins, begin_timepoints[text_idx_bg])
    text_idx_ed = np.max(np.argwhere(np.array(text_accum_len)<=char_idx+len(summ['sentence'])))
    while text_idx_ed < len(text_list) and (begin_timepoints[text_idx_ed+1]-end_timepoints[text_idx_ed]) < 50:
        text_idx_ed = text_idx_ed + 1
    ends = np.append(ends, end_timepoints[text_idx_ed])

_, ret_index = np.unique(begins, return_index=True)
ends = ends[ret_index]
begins = begins[ret_index]

# print('output length(s): %d' % sum(ends-begins))


# 裁剪和合并视频
for i in range(len(begins)):
    ss = '00:' + time.strftime('%M:%S', time.localtime(int(begins[i]/1000))) + '.' + str(int(begins[i]%1000))
    to = '00:' + time.strftime('%M:%S', time.localtime(int(ends[i]/1000))) + '.' + str(int(ends[i]%1000))
    os.system('ffmpeg -i '+ video_path +' -ss ' + ss + ' -to ' + str(to) + ' cut%d'%i + '.mp4')

fw = open('list.txt', 'w')
fw.write("".join(['file ' + 'cut%d'%i + '.mp4\n' for i in range(len(begins))]))
fw.close()

os.system('ffmpeg -f concat -i list.txt -c copy ' + output_path)

os.system('rm list.txt audio.wav ' + ''.join([' cut%d'%i + '.mp4' for i in range(len(begins))]))
