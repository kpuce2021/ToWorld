import os
import sys
from pydub import AudioSegment

filepath = 'D:/#2021_CAPSTONE/_DataSet/sound_data_original (m4a)/test_m4a2wav/'
filename = 'my_audio_file.m4a'

# convert m4a to wav
def m4a2wav(file_path):
    file_path_list = file_path.split('/')  # a/b/c/d [a,b,c,d]
    file_name = file_path_list[-1]  # d
    print("m4a2wav함수: file_name : {}".format(file_name))

    # download_blob('kpu2021mk3-220df.appspot.com', file_path, '/tmp/'+ file_name)  # 가상공간에 /tmp/file_name 생성
    # virtual_file = '/tmp/'+ file_name  # 가상공간에 생성된 파일 이름 변경

    # (path, file_extension) = os.path.splitext('/tmp/'+ file_name)
    (path, file_extension) = os.path.splitext(file_path)
    # /tmp/file_name, .m4a
    file_extension_final = file_extension.replace('.', '') # . 제거

    # track = AudioSegment.from_file('/tmp/'+ file_name, file_extension_final)
    track = AudioSegment.from_file(file_path, file_extension_final)
    wav_filename = file_name.replace(file_extension_final, 'wav')
    wav_path = filepath + wav_filename
    file_handle = track.export(wav_path,format='wav')

    # check용 upload
    # upload_blob('kpu2021mk3-220df.appspot.com', wav_path, 'check_wav_file.wav')

    # 반환
    return wav_path
m4a2wav(filepath+filename)