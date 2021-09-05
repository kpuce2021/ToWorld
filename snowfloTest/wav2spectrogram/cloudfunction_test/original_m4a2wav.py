import os
import argparse
import traceback
from pydub import AudioSegment

# 바꿀 format 설정
formats_to_convert = ['.m4a']

# file_directory - 파일을 가진 상위 디렉토리
file_directory = 'C:/Users/jaehee/Desktop/음성녹음파일(박재희)_복사/뭉게짐/굿모닝'

# 변환
for (dirpath, dirnames, filenames) in os.walk(file_directory):  # 상위 폴더
    # https://codechacha.com/ko/python-walk-files/
    # os.walk : for 로 어떤 경로의 모든 하위 폴더와 파일을 탐색
    for filename in filenames:
        if filename.endswith(tuple(formats_to_convert)):  # tuple -> ('.m4a')
            # .m4a로 끝나면
            print('dirpath: ', dirpath)
            print('filename: ', filename)

            # filepath 설정 = [상위 폴더]/[파일 이름]
            filepath = dirpath + '/' + filename
            # 확장자 분리  # filepath.m4a --> ['filepath','.m4a']
            (path, file_extension) = os.path.splitext(filepath)
            # 확장자 . 삭제  # .m4a --> m4a
            file_extension_final = file_extension.replace('.', '')

            print('path', path)

            try:
                print('filepath', filepath)
                print('file_extension_final', file_extension_final)
                track = AudioSegment.from_file(filepath, file_extension_final)
                wav_filename = filename.replace(file_extension_final, 'wav')
                wav_path = dirpath + '/' + wav_filename
                print('CONVERTING: ' + str(filepath))
                print('\n')
                file_handle = track.export(wav_path, format='wav')
                os.remove(filepath)
            except:
                print(traceback.print_exc())
