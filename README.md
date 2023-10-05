# coinpan-crawler

코인판 자유게시판 웹페이지 크롤러 & 대시보드

---

## Installation

해당 프로그램은 Makefile을 통해 간편하게 설치할 수 있습니다.

```bash
  make install
```

Make가 없는 경우, 별도로 설치가 필요합니다.
- [Make.exe install](https://gnuwin32.sourceforge.net/packages/make.htm)

---

## Crawling

크롤러를 실행하는 방법은 다음과 같습니다.


```bash
  make crawling
```

다음 명령어 실행시, 크롤링한 페이지를 입력하는 란이 터미널에 등장합니다.

해당 란에 숫자 입력 이후, 잠시 후에 csv 파일로 크롤링 데이터를 추출할 수 있습니다.

---

## dashboarding

크롤링한 데이터를 토대로 대시보드를 생성할 수 있습니다.

대시보드를 통해 확인할 수 있는 내용은 다음과 같습니다.

- 게시물 작성자 랭킹 차트
- 게시물 내 주로 등장한 단어 워드클라우드

다음 명령어를 통해 대시보드를 생성할 수 있습니다.

```bash
  make dashboard
```

다음 명령어 실행시, http://localhost:8000 로 대시보드가 생성됩니다.
단, 당일치 데이터가 생성된 경우에만 생성이 가능하며, 데이터가 존재하지 않을 경우, 대시보드는 생성되지 않습니다.

---

## Authors

- [@sorrychoe](https://www.github.com/sorrychoe)

## License

[MIT](https://choosealicense.com/licenses/mit/)

## you have some issue?

사용하다 문제 발생 시, github 상단 이슈란에 등록해주세요.
