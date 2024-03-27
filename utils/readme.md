## data parsing

- AI hub dataset에서 Yolov5 모델에 학습시키기 위한 data parsing: Alring_preprocessing.py
  
1. xml annotation 파일을 읽어 필요한 라벨에 대한 txt파일을 labels 디렉토리에 생성
2. 이미지 파일과 txt파일을 비교해 이름이 같은 파일만 남기고 나머지는 삭제
3. 라벨 처리- 필요 없거나 추가해야 하는 라벨(.txt 파일 수정)
4. images디렉토리에 이미지 파일(.png, .jpg) 복사
