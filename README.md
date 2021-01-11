# 2021년도 컴퓨터공학부 졸업작품
## 설계 주제 : 청각 장애인을 위한 스마트 스피커 연동 어플(Smart speaker application for hearing impaired)
#### [팀명]
  + ToWorld
#### [팀 구성원]
  + 임지섭(팀장)
  + 박재희
  + 최상호
#### [설계 배경]
  + 언어 장애인 대상으로 한 어플은 있지만, 언어장애를 동반한 청각 장애인을 위한 앱은 개발되어 있지 않음
#### [설계 목표]
  + 음성을 텍스트화 시키고 진동을 통해 알림을 제공하며 사용자 맞춤형 입력이 가능한 스마트 스피커 연동 어플리케이션 개발을 목표
#### [개발 효과]
  + 언어 장애를 동반한 청각 장애인의 스마트 스피커 접근성 향상과 삶의 질 향상
#### [개발 환경]
##### 1. 언어
> Kotlin   
> Python
##### 2. 라이브러리
> TensorFlow   
> RNNoise
##### 3. O/S
> Android
##### 4. 개발 도구
> Android Studio
##### 5. 데이터베이스
> Google FireBase
##### 6. 개발 기기
> Android 폰   
> Google Home 스피커
-----------
## 음성 인식 시스템
### 기본 구조
+ 전처리   
> 사람의 달팽이관의 기능으로 음성 신호로부터 시간 및 주파수 영역의 특징을 추출하는 과정   
> 음성 신호의 주기성 및 동기성의 정보를 추출함   
+ 패턴 인식   
> 추출된 정보를 바탕으로 음소, 음절, 단어를 인식하는 역할   
> 템플릿 사전을 기반으로 다양한 방식으로 접근   
'''   
DTW - 동적 프로그래밍   
- 2개의 시계열 데이터의 유사도를 알아내는 알고리즘   
HMM - 확률 추출 과정   
- 시간의 흐름에 따른 패턴 인식에 유용   
Knowledge Base - 인공지능을 이용한 추론   
- 전문가 지식을 학습시키는 데이터베이스   
Neural Network - 패턴 분류   
- 두뇌의 뉴런 형태를 수학적으로 모델링   
'''   
+ 후처리   
> 패턴 인식 후 음소, 음절, 단어를 재구성하여 문장 복원(형태론, 의미론, 구문론 이용)   
'''   
형태론 - 단어를 형성하는 규칙(**주성분은 형태소**)   
의미론 - 이해와 해석관련(**주성분은 단어**)   
구문론 - 구, 절, 문장 형성 규칙(**주성분은 문장**)   
구문 규칙 모델 - 매 단어 다음에 올 수 있는 단어를 제한   
통계적 모델 - 매 단어 이전의 N개 단어가 발생할 확률을 고려해 문장 인식   
'''   
