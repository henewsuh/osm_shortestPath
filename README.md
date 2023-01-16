## OSMnx 라이브러리를 사용해 가장 가까운 지하철역까지의 거리를 계산하는 코드 
#### - 단순 직선 거리가 아닌 '도로 네트워크 상의 최단거리



### 1. 코드 실행 방법
    - 해당 repo 전체를 '폴더'로 다운로드 함. 
    - 모든 경로는 상대 경로로 작성되어 있으므로 main.py를 F5로 실행하면 됨. 
### 2. Data 폴더 설명 
    - Gangnam-gu_streets.shp : 도로명주소 데이터 중 강남구에 해당하는 도로만 추출한 것. (EPSG: 5179)
       - 데이터소스 : http://data.nsdi.go.kr/dataset/12902
    - Gangnam-gu_subway.shp : 도로명주소 데이터 중 강남구에 해당하는 도로만 추출한 것. (EPSG: 5179)
       - 데이터소스 : Seoul Open Data Portal Services
    - result.shp : 코드 산출물, dist2sub 컬럼에 가장 가까운 지하철역까지의 거리가 계산되어 있음 (in meters) 
     
     
