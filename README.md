## Team Members
- FE : 박지연, 유샘솔, 이지은
- BE : 강현수, 김치오, 양한아, 조혜윤

## 프로젝트 기간
- 2021.02.15 ~ 2021.02.26

## 기술 스택

- Python
- Django
- AQueryTool
- MySQL
- CORS Header
- Bcrpyt
- PyJWT
- AWS EC2, AWS RDS
- Git
- Naver Cloud Platform API

## API Endpoint
- ![Image](https://drive.google.com/file/d/1EZPfNki7tQ602wFUYmc486-1cgKmohvf/view?usp=sharing)

## 기능 구현

##### 모델링

- AQueryTool을 사용하여 DB모델링
- ![Image](https://drive.google.com/file/d/1846m-SGEYwf3ajg-6LyBX0QlmJjd-cq6/view?usp=sharing)

##### 회원가입 & 로그인

- 회원 가입 시 SMS 인증으로 네이버 클라우드 플랫폼에서 제공하는 SMS 발신 API를 사용
- bcrypt를 이용하여 비밀번호 암호화
- 로그인 시 JWT 토큰 발급
- login decorator를 만들어서 인가 확인

##### Shop(상품 리스트, 상품 상세)

- 전체 카테고리의 상품 리스트, 카테고리 별 상품 리스트
- 상품 상세 페이지
- 연관 상품 나열

##### 장바구니

- 상품 리스트 페이지 또는 상품 상세 페이지에서 특정 상품을 바로 장바구니에 담기
- 장바구니 페이지
- 장바구니에 담긴 특정 상품의 수량, 사이즈 변경
- 장바구니에 담긴 특정 상품 삭제

##### 결제

- 결제 페이지
- 결제 처리 및 상품 재고 변경

##### 설문조사 및 제품 추천

- 사용자의 답변에 맞는 제품 추천

##### 리뷰

- 주문 한 건에 대한 리뷰 작성
- 리뷰 페이지
