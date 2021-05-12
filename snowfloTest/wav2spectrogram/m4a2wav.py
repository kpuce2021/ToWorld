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
from pydub import AudioSegment

formats_to_convert = ['.m4a']

for (dirpath, dirnames, filenames) in os.walk('D:/audio_files'):
    for filename in filenames:
        if filename.endswith(tuple(formats_to_convert)):
            print('dirpath',dirpath)
            print('filenames',filenames)

            filepath = dirpath + '\\' + filename
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


