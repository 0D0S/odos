# 0D0S

## 팀 소개

### 팀 구성

|   직책   | 이름  |        한마디         |
|:------:|:---:|:------------------:|
|   팀장   | 이수빈 | **당연히 뒷처리는 팀원의 몫** |
| 초기 개발자 | 고명준 | **팀장님이 알아서 해주실거야** |
|  바지사장  | 이원진 |     **퇴사 준비중**     |
|  대통령   | 정주영 |    **절 뽑아주십쇼**     |
|   실세   | 정다인 |     **막내 온 탑**     |

### 팀 규칙

- 자율출퇴근제
- 들어오는 건 자유지만 퇴사는 없음!
- 금지 단어: 팀장님, 역시

## Convention

### commit message

- 메세지는 [gitmoji homepage](https://gitmoji.dev/)나 [GITMOJI.md](GITMOJI.md) 참고

### formatting

- 코드는 [black](https://github.com/psf/black)으로 포매팅

### naming convention

|                               종류                                |         규칙          |            예시            |
|:---------------------------------------------------------------:|:-------------------:|:------------------------:|
|                             package                             |        스네이크         |                          |
|                             module                              |        스네이크         |    import module_name    |
|                              class                              | 파스칼(UpperCamelCase) |    class ClassName()     |
|                            exception                            | 파스칼(UpperCamelCase) |                          |
|                            function                             |        스네이크         |   def function_name()    |
|                            constant                             |      대문자 + 밑줄       | MODULE_CONSTANT_NAME = 0 |
| variable<br/>parameter<br/>locat variable<br/>instance variable |        스네이크         |    variable_name = 0     |
|                             method                              |        스네이크         |      method_name()       |

- 변수 종류
    - 내부 변수(internal): 맨 앞 밑줄 하나
        - _protected_attribute_name = 0
        - `from Module import *` 했을 때, 가져오지 않는다.
    - 숨은 변수(hidden): 맨 앞 밑줄 두 개
        - __hidden_attribute_name = 0
        - 클래스 속성들도 사용

- 자세한 건 [PEP8 Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions) 참고

## 프로젝트 설명

### 목적

- 하루 한 문제씩 푸는지 확인하고 독촉하기 위한 슬랙봇

### version

|       버전       |                          추가 기능                           |       삭제 기능        |
|:--------------:|:--------------------------------------------------------:|:------------------:|
|    ver1.0.0    | - 출퇴근 및 현재 위치 확인<br/>- 연속으로 안 푼 날짜 체크<br/>-연속으로 푼 날짜 체크  |                    |
| ver1.1.0(beta) | - 블랙홀 날짜 추가<br/>- UI 개편<br/>- 웹 크롤링으로 방법 변경<br/>- 코드 객체화 | - solved.ac api 삭제 |

### 추후 업데이트 예정

- 11사이를 위한 기능 고안 및 제작
- 앱
- 자동화

### 나오는 내용

![display.png](img/display.png)

- 이모지와 이름
- 백준 랭크
- 연속으로 풀지 않은 날짜 or 연속으로 푼 날짜
- 블랙홀 기간
- 출퇴근 여부

### csv 인덱스

| 이름 | intra id | baekjoon id |
|:--:|:--------:|:-----------:|

### 구성원

|                        42Seoul                         |                          Baekjoon                          |                           Github                           |                                        Tier                                        |
|:------------------------------------------------------:|:----------------------------------------------------------:|:----------------------------------------------------------:|:----------------------------------------------------------------------------------:|
|     [myko](https://profile.intra.42.fr/users/myko)     |    [kmj951015](https://solved.ac/ko/profile/kmj951015)     | [![github](img/github.svg)](https://github.com/Kdelphinus) |    ![kmj951015 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=kmj951015)    |
| [subinlee](https://profile.intra.42.fr/users/subinlee) |         [abyo](https://solved.ac/ko/profile/abyo)          |  [![github](img/github.svg)](https://github.com/subillie)  |         ![abyo 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=abyo)         |
| [hyobicho](https://profile.intra.42.fr/users/hyobicho) |     	[chodl201](https://solved.ac/ko/profile/chodl201)     |  [![github](img/github.svg)](https://github.com/hyobb109)  |     ![chodl201 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=chodl201)     |
|  [eunhcho](https://profile.intra.42.fr/users/eunhcho)  |     	[hi_eunho](https://solved.ac/ko/profile/hi_eunho)     | [![github](img/github.svg)](https://github.com/AnnyangEH)  |     ![hi_eunho 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=hi_eunho)     |
| [jaekkang](https://profile.intra.42.fr/users/jaekkang) | 	[rkdwornjs123](https://solved.ac/ko/profile/rkdwornjs123) |  [![github](img/github.svg)](https://github.com/jaekkang)  | ![rkdwornjs123 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=rkdwornjs123) |
|  [seulee2](https://profile.intra.42.fr/users/seulee2)  |       [sngsho](https://solved.ac/ko/profile/sngsho)        |   [![github](img/github.svg)](https://github.com/sngsho)   |       ![sngsho 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=sngsho)       |
| [juyojeon](https://profile.intra.42.fr/users/juyojeon) |      [wdd1016](https://solved.ac/ko/profile/wdd1016)       |  [![github](img/github.svg)](https://github.com/wdd1016)   |      ![wdd1016 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=wdd1016)      |
| [jiyeolee](https://profile.intra.42.fr/users/jiyeolee) |     [meiv0181](https://solved.ac/ko/profile/meiv0181)      |  [![github](img/github.svg)](https://github.com/pep-per)   |     ![meiv0181 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=meiv0181)     |
| [wonjilee](https://profile.intra.42.fr/users/wonjilee) |     [joon6924](https://solved.ac/ko/profile/joon6924)      | [![github](img/github.svg)](https://github.com/inwoo0115)  |     ![joon6924 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=joon6924)     |
|  [yunjcho](https://profile.intra.42.fr/users/yunjcho)  | [algorithm317](https://solved.ac/ko/profile/algorithm317)  | [![github](img/github.svg)](https://github.com/YunjooCho)  | ![algorithm317 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=algorithm317) |
| [jinholee](https://profile.intra.42.fr/users/jinholee) |    [leejh9779](https://solved.ac/ko/profile/leejh9779)     |      [![github](img/github.svg)](https://github.com)       |    ![leejh9779 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=leejh9779)    |
|  [gyuhong](https://profile.intra.42.fr/users/gyuhong)  |       [guunee](https://solved.ac/ko/profile/guunee)        |   [![github](img/github.svg)](https://github.com/guune)    |       ![guunee 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=guunee)       |
|   [hysung](https://profile.intra.42.fr/users/hysung)   |       [hj3603](https://solved.ac/ko/profile/hj3603)        |  [![github](img/github.svg)](https://github.com/vivivim)   |       ![hj3603 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=hj3603)       |
| [sungwook](https://profile.intra.42.fr/users/sungwook) |      [silenc3](https://solved.ac/ko/profile/silenc3)       | [![github](img/github.svg)](https://github.com/42sungwook) |      ![silenc3 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=silenc3)      |
| [daijeong](https://profile.intra.42.fr/users/daijeong) |   [Wilbur0306](https://solved.ac/ko/profile/Wilbur0306)    | [![github](img/github.svg)](https://github.com/Wilbur0306) |   ![Wilbur0306 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=Wilbur0306)   |
|  [danpark](https://profile.intra.42.fr/users/danpark)  |        [switb](https://solved.ac/ko/profile/switb)         | [![github](img/github.svg)](https://github.com/honeyl3ee)  |        ![switb 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=switb)        |
|  [hujeong](https://profile.intra.42.fr/users/hujeong)  |        [heeho](https://solved.ac/ko/profile/heeho)         |   [![github](img/github.svg)](https://github.com/heehoh)   |        ![heeho 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=heeho)        |
|  [hyeonjo](https://profile.intra.42.fr/users/hyeonjo)  |     [sosoid42](https://solved.ac/ko/profile/sosoid42)      |      [![github](img/github.svg)](https://github.com)       |     ![sosoid42 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=sosoid42)     |
|   [jelee2](https://profile.intra.42.fr/users/jelee2)   | [neutrinox4b1](https://solved.ac/ko/profile/neutrinox4b1)  |      [![github](img/github.svg)](https://github.com)       | ![neutrinox4b1 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=neutrinox4b1) |
|   [hahseo](https://profile.intra.42.fr/users/hahseo)   |          [h2o](https://solved.ac/ko/profile/h2o)           |    [![github](img/github.svg)](https://github.com/oh2o)    |          ![h2o 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=h2o)          |
|  [yejinam](https://profile.intra.42.fr/users/yejinam)  |   [saltwoodyj](https://solved.ac/ko/profile/saltwoodyj)    |      [![github](img/github.svg)](https://github.com)       |   ![saltwoodyj 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=saltwoodyj)   |
|  [suhbaek](https://profile.intra.42.fr/users/suhbaek)  |    [sbaek4908](https://solved.ac/ko/profile/sbaek4908)     |      [![github](img/github.svg)](https://github.com)       |    ![sbaek4908 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=sbaek4908)    |
| [seonmiki](https://profile.intra.42.fr/users/seonmiki) |       [sunsky](https://solved.ac/ko/profile/sunsky)        |      [![github](img/github.svg)](https://github.com)       |       ![sunsky 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=sunsky)       |
|   [eunson](https://profile.intra.42.fr/users/eunson)   |   [ebcode2021](https://solved.ac/ko/profile/ebcode2021)    |      [![github](img/github.svg)](https://github.com)       |   ![ebcode2021 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=ebcode2021)   |
|    [yoahn](https://profile.intra.42.fr/users/yoahn)    |   [dudtjs0920](https://solved.ac/ko/profile/dudtjs0920)    |  [![github](img/github.svg)](https://github.com/AYoungSn)  |   ![ebcode2021 백준](http://mazassumnida.wtf/api/v2/generate_badge?boj=dudtjs0920)   |
|      [tyi](https://profile.intra.42.fr/users/tyi)      |                                                            |      [![github](img/github.svg)](https://github.com)       |                                                                                    |

# 참고

- [42seoul, 42api](https://api.intra.42.fr/apidoc)
- [hivehelsinki의 42api-lib](https://github.com/hivehelsinki/42api-lib)
- [emoji copy](https://www.emojicopy.com/)
