#데이터 전처리

yolov5에 학습시키기 위해 데이터를 전처리 해주었다.
각 파일은 다음과 같은 역할을 한다.

- xml2yolo: xml annotation 파일을 읽어 필요한 라벨에 대한 txt파일을 labels 디렉토리에 생성


- empty_delete: 이미지 파일과 txt파일을 비교해 이름이 같은 파일만 남기고 나머지는 삭제


- label_change_txt: 라벨 처리- 필요 없거나 추가해야 하는 라벨(.txt 파일 수정)


- data_ch: images디렉토리에 이미지 파일(.png, .jpg) 복사
