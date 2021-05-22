# Convert all file extensions to m4a (if required)
'''
import os, sys

folder = 'D:/DDataSet/today_weather/' # D:\DDataSet\living_light_on

for filename in os.listdir(folder):
    infilename = os.path.join(folder,filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.tmp','.m4a')
    output = os.rename(infilename, newname)
'''

# 폴더이름: D드라이브 DDataSet

import os
import argparse
import traceback
from pydub import AudioSegment  # ffmpeg 를 설정해야 함.

formats_to_convert = ['.m4a']

for (dirpath, dirnames, filenames) in os.walk('D:/#2021_CAPSTONE/_DataSet/sound_data/naerrow'):  # 상위 폴더
    # https://codechacha.com/ko/python-walk-files/
    # os.walk : for 로 어떤 경로의 모든 하위 폴더와 파일을 탐색
    for filename in filenames:
        if filename.endswith(tuple(formats_to_convert)):  # tuple -> ('.m4a')
            # .m4a로 끝나면
            print('dirpath',dirpath)
            print('filenames',filenames)

#           filepath = dirpath + '\\' + filename  # 기존
            filepath = dirpath + '/' + filename
            (path, file_extension) = os.path.splitext(filepath)
            file_extension_final = file_extension.replace('.', '')

            print('path',path)
            try:
                print('filepath',filepath)
                print('file_extension_final',file_extension_final)
                track = AudioSegment.from_file(filepath, file_extension_final)
                wav_filename = filename.replace(file_extension_final, 'wav')
                wav_path = dirpath + '/' + wav_filename
                print('CONVERTING: ' + str(filepath))
                file_handle = track.export(wav_path, format='wav')
                os.remove(filepath)
            except:
                print(traceback.print_exc())


