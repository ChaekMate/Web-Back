import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import date
from app.core.database import SessionLocal
from app.models.book import Book


def clear_books(db):
    """기존 도서 데이터 삭제"""
    db.query(Book).delete()
    db.commit()
    print("✅ 기존 도서 데이터 삭제 완료")


def create_mock_books():
    """Mock 도서 데이터 생성"""
    books = [
        # ========== 인기 도서 15권 ==========
        Book(
            title="트렌드 코리아 2025",
            author="김난도 외",
            publisher="미래의창",
            isbn="9788934986898",
            cover_image="https://image.aladin.co.kr/product/33544/62/cover500/k082939136_1.jpg",
            description="2025년 대한민국 트렌드를 예측하는 필독서",
            price=18000,
            rating=4.5,
            review_count=1234,
            theme="work",
            category="경제/경영",
            is_popular=True,
            published_date=date(2024, 10, 15),
            page_count=432
        ),
        Book(
            title="역행자",
            author="자청",
            publisher="웅진지식하우스",
            isbn="9788901260921",
            cover_image="https://image.aladin.co.kr/product/29066/25/cover500/k422835564_1.jpg",
            description="돈, 시간, 운명으로부터 완전한 자유를 얻는 7단계 인생 공략집",
            price=17800,
            rating=4.7,
            review_count=3421,
            theme="growth",
            category="자기계발",
            is_popular=True,
            published_date=date(2022, 6, 1),
            page_count=332
        ),
        Book(
            title="불편한 편의점",
            author="김호연",
            publisher="나무옆의자",
            isbn="9791167960382",
            cover_image="https://image.aladin.co.kr/product/27695/48/cover500/k392835893_1.jpg",
            description="따뜻한 위로와 공감을 전하는 힐링 소설",
            price=14000,
            rating=4.8,
            review_count=5678,
            theme="healing",
            category="소설",
            is_popular=True,
            published_date=date(2021, 4, 20),
            page_count=352
        ),
        Book(
            title="아몬드",
            author="손원평",
            publisher="창비",
            isbn="9788936434267",
            cover_image="https://image.aladin.co.kr/product/16892/60/cover500/k932535690_1.jpg",
            description="감정을 느끼지 못하는 소년의 성장 이야기",
            price=13800,
            rating=4.6,
            review_count=4567,
            theme="healing",
            category="소설",
            is_popular=True,
            published_date=date(2017, 3, 31),
            page_count=268
        ),
        Book(
            title="달러구트 꿈 백화점",
            author="이미예",
            publisher="팩토리나인",
            isbn="9791165341909",
            cover_image="https://image.aladin.co.kr/product/25494/58/cover500/k592636959_1.jpg",
            description="잠들어야만 입장 가능한 꿈 백화점 이야기",
            price=14000,
            rating=4.5,
            review_count=3890,
            theme="healing",
            category="소설",
            is_popular=True,
            published_date=date(2020, 7, 1),
            page_count=300
        ),
        Book(
            title="원씽",
            author="게리 켈러, 제이 파파산",
            publisher="비즈니스북스",
            isbn="9788963190013",
            cover_image="https://image.aladin.co.kr/product/2936/64/cover500/k152434271_1.jpg",
            description="복잡한 세상을 이기는 단순함의 힘",
            price=13800,
            rating=4.4,
            review_count=2345,
            theme="work",
            category="자기계발",
            is_popular=True,
            published_date=date(2013, 8, 5),
            page_count=256
        ),
        Book(
            title="나는 나로 살기로 했다",
            author="김수현",
            publisher="마음의숲",
            isbn="9791160340204",
            cover_image="https://image.aladin.co.kr/product/11907/60/cover500/k232535273_1.jpg",
            description="세상과 타협하지 않고 나로 사는 법",
            price=14500,
            rating=4.3,
            review_count=3210,
            theme="growth",
            category="에세이",
            is_popular=True,
            published_date=date(2016, 10, 10),
            page_count=260
        ),
        Book(
            title="멈추면, 비로소 보이는 것들",
            author="혜민",
            publisher="쌤앤파커스",
            isbn="9788965702092",
            cover_image="https://image.aladin.co.kr/product/2328/59/cover500/8965702097_2.jpg",
            description="바쁜 일상에서 벗어나 마음을 돌아보는 시간",
            price=13000,
            rating=4.2,
            review_count=4321,
            theme="healing",
            category="에세이",
            is_popular=True,
            published_date=date(2012, 11, 28),
            page_count=292
        ),
        Book(
            title="데일 카네기 인간관계론",
            author="데일 카네기",
            publisher="현대지성",
            isbn="9791139708691",
            cover_image="https://image.aladin.co.kr/product/26494/7/cover500/k102736317_1.jpg",
            description="사람의 마음을 얻는 불변의 법칙",
            price=11000,
            rating=4.6,
            review_count=2890,
            theme="work",
            category="자기계발",
            is_popular=True,
            published_date=date(2019, 1, 3),
            page_count=352
        ),
        Book(
            title="미드나잇 라이브러리",
            author="매트 헤이그",
            publisher="인플루엔셜",
            isbn="9791191056174",
            cover_image="https://image.aladin.co.kr/product/26494/67/cover500/k672636456_1.jpg",
            description="삶과 죽음 사이, 무한한 가능성의 도서관",
            price=15800,
            rating=4.7,
            review_count=5432,
            theme="healing",
            category="소설",
            is_popular=True,
            published_date=date(2021, 3, 25),
            page_count=408
        ),
        Book(
            title="82년생 김지영",
            author="조남주",
            publisher="민음사",
            isbn="9788937473722",
            cover_image="https://image.aladin.co.kr/product/9863/43/cover500/k662434852_1.jpg",
            description="평범한 여성의 인생을 통해 본 한국 사회",
            price=13800,
            rating=4.4,
            review_count=6789,
            theme="growth",
            category="소설",
            is_popular=True,
            published_date=date(2016, 10, 14),
            page_count=192
        ),
        Book(
            title="습관의 힘",
            author="찰스 두히그",
            publisher="갤리온",
            isbn="9788901145280",
            cover_image="https://image.aladin.co.kr/product/2012/93/cover500/8901145286_2.jpg",
            description="인생을 바꾸는 습관의 비밀",
            price=16000,
            rating=4.5,
            review_count=3456,
            theme="growth",
            category="자기계발",
            is_popular=True,
            published_date=date(2012, 10, 1),
            page_count=432
        ),
        Book(
            title="참을 수 없는 존재의 가벼움",
            author="밀란 쿤데라",
            publisher="민음사",
            isbn="9788937462429",
            cover_image="https://image.aladin.co.kr/product/60/73/cover500/8937462427_2.jpg",
            description="인생의 무게와 가벼움에 대한 철학적 성찰",
            price=14000,
            rating=4.3,
            review_count=2345,
            theme="healing",
            category="소설",
            is_popular=True,
            published_date=date(2009, 7, 20),
            page_count=460
        ),
        Book(
            title="어떻게 살 것인가",
            author="유시민",
            publisher="생각의길",
            isbn="9788965137467",
            cover_image="https://image.aladin.co.kr/product/8742/32/cover500/k322534730_1.jpg",
            description="역사와 삶에 대한 성찰",
            price=15000,
            rating=4.4,
            review_count=4567,
            theme="growth",
            category="인문",
            is_popular=True,
            published_date=date(2016, 7, 22),
            page_count=340
        ),
        Book(
            title="코스모스",
            author="칼 세이건",
            publisher="사이언스북스",
            isbn="9788983711892",
            cover_image="https://image.aladin.co.kr/product/526/13/cover500/8983711892_2.jpg",
            description="우주와 인간에 대한 경이로운 탐험",
            price=17000,
            rating=4.8,
            review_count=3210,
            theme="growth",
            category="과학",
            is_popular=True,
            published_date=date(2006, 12, 20),
            page_count=576
        ),
        
        # ========== 업무 테마 15권 (work) ==========
        Book(
            title="딥 워크",
            author="칼 뉴포트",
            publisher="민음사",
            isbn="9788937485565",
            cover_image="https://image.aladin.co.kr/product/9595/63/cover500/k222534853_1.jpg",
            description="집중력을 되찾는 네 가지 원칙",
            price=16000,
            rating=4.7,
            review_count=2890,
            theme="work",
            category="자기계발",
            published_date=date(2017, 1, 31),
            page_count=328
        ),
        Book(
            title="아침형 인간",
            author="할 엘로드",
            publisher="한빛비즈",
            isbn="9791157841974",
            cover_image="https://image.aladin.co.kr/product/8742/94/cover500/k012534737_1.jpg",
            description="기적의 모닝 루틴 6가지",
            price=14000,
            rating=4.4,
            review_count=3456,
            theme="work",
            category="자기계발",
            published_date=date(2016, 6, 8),
            page_count=268
        ),
        Book(
            title="에센셜리즘",
            author="그렉 맥커운",
            publisher="알에이치코리아",
            isbn="9788925555194",
            cover_image="https://image.aladin.co.kr/product/6074/3/cover500/k202534551_1.jpg",
            description="본질을 추구하는 삶",
            price=14500,
            rating=4.5,
            review_count=2345,
            theme="work",
            category="자기계발",
            published_date=date(2015, 4, 1),
            page_count=284
        ),
        Book(
            title="타이탄의 도구들",
            author="팀 페리스",
            publisher="토네이도",
            isbn="9791158510800",
            cover_image="https://image.aladin.co.kr/product/11907/59/cover500/k922534974_1.jpg",
            description="세계 정상급 인물들의 습관과 도구",
            price=22000,
            rating=4.3,
            review_count=1890,
            theme="work",
            category="자기계발",
            published_date=date(2017, 5, 30),
            page_count=688
        ),
        Book(
            title="1등의 습관",
            author="정영대",
            publisher="알키",
            isbn="9788997578962",
            cover_image="https://image.aladin.co.kr/product/5494/73/cover500/k822534661_1.jpg",
            description="성공하는 사람들의 7가지 습관",
            price=13500,
            rating=4.2,
            review_count=2567,
            theme="work",
            category="자기계발",
            published_date=date(2015, 1, 20),
            page_count=248
        ),
        Book(
            title="프로그래머의 뇌",
            author="펠리너 허르만스",
            publisher="한빛미디어",
            isbn="9791162245316",
            cover_image="https://image.aladin.co.kr/product/28392/80/cover500/k342839280_1.jpg",
            description="코드를 더 잘 읽고 이해하는 방법",
            price=22000,
            rating=4.6,
            review_count=987,
            theme="work",
            category="IT",
            published_date=date(2022, 3, 3),
            page_count=304
        ),
        Book(
            title="클린 코드",
            author="로버트 C. 마틴",
            publisher="인사이트",
            isbn="9788966260959",
            cover_image="https://image.aladin.co.kr/product/4638/86/cover500/8966260950_2.jpg",
            description="애자일 소프트웨어 장인 정신",
            price=33000,
            rating=4.7,
            review_count=3210,
            theme="work",
            category="IT",
            published_date=date(2013, 12, 24),
            page_count=584
        ),
        Book(
            title="개발자의 글쓰기",
            author="김철수",
            publisher="위키북스",
            isbn="9791158391744",
            cover_image="https://image.aladin.co.kr/product/16892/59/cover500/k742534892_1.jpg",
            description="변수명, 함수명, 주석 작성의 기술",
            price=16000,
            rating=4.4,
            review_count=1234,
            theme="work",
            category="IT",
            published_date=date(2019, 10, 2),
            page_count=244
        ),
        Book(
            title="스크럼",
            author="제프 서덜랜드",
            publisher="김영사",
            isbn="9788934956303",
            cover_image="https://image.aladin.co.kr/product/5494/76/cover500/k012534566_1.jpg",
            description="2배의 일을 절반의 시간에",
            price=16000,
            rating=4.3,
            review_count=1567,
            theme="work",
            category="경영",
            published_date=date(2015, 3, 11),
            page_count=284
        ),
        Book(
            title="THE GOAL",
            author="엘리 골드렛",
            publisher="동양북스",
            isbn="9788963724102",
            cover_image="https://image.aladin.co.kr/product/2012/99/cover500/8963724107_2.jpg",
            description="비즈니스 프로세스 혁신의 고전",
            price=18000,
            rating=4.5,
            review_count=2345,
            theme="work",
            category="경영",
            published_date=date(2013, 11, 25),
            page_count=464
        ),
        Book(
            title="OKR",
            author="존 도어",
            publisher="세종서적",
            isbn="9788984078901",
            cover_image="https://image.aladin.co.kr/product/18526/49/cover500/k512636044_1.jpg",
            description="전설적인 벤처투자자가 구글에 전해준 성공 방식",
            price=17000,
            rating=4.4,
            review_count=1890,
            theme="work",
            category="경영",
            published_date=date(2019, 1, 4),
            page_count=408
        ),
        Book(
            title="린 스타트업",
            author="에릭 리스",
            publisher="인사이트",
            isbn="9788966260614",
            cover_image="https://image.aladin.co.kr/product/2012/51/cover500/8966260616_2.jpg",
            description="지속 가능한 성장을 이끄는 창업의 과학",
            price=16000,
            rating=4.3,
            review_count=2567,
            theme="work",
            category="경영",
            published_date=date(2012, 5, 11),
            page_count=376
        ),
        Book(
            title="피터 드러커의 자기경영노트",
            author="피터 드러커",
            publisher="한국경제신문",
            isbn="9788947527958",
            cover_image="https://image.aladin.co.kr/product/70/22/cover500/8947527955_2.jpg",
            description="성과를 높이는 자기경영의 기술",
            price=15000,
            rating=4.6,
            review_count=1234,
            theme="work",
            category="경영",
            published_date=date(2008, 3, 3),
            page_count=288
        ),
        Book(
            title="실리콘밸리의 팀장들",
            author="킴 스콧",
            publisher="청림출판",
            isbn="9788935212521",
            cover_image="https://image.aladin.co.kr/product/13907/60/cover500/k472534860_1.jpg",
            description="빠르게 성장하는 팀을 만드는 방법",
            price=17000,
            rating=4.5,
            review_count=987,
            theme="work",
            category="경영",
            published_date=date(2018, 3, 5),
            page_count=384
        ),
        Book(
            title="마케팅 불변의 법칙",
            author="알 리스, 잭 트라우트",
            publisher="비즈니스맵",
            isbn="9788990489678",
            cover_image="https://image.aladin.co.kr/product/70/21/cover500/8990489679_2.jpg",
            description="22가지 마케팅의 법칙",
            price=12000,
            rating=4.4,
            review_count=1567,
            theme="work",
            category="마케팅",
            published_date=date(2008, 8, 25),
            page_count=204
        ),
        
        # ========== 힐링 테마 15권 (healing) ==========
        Book(
            title="나미야 잡화점의 기적",
            author="히가시노 게이고",
            publisher="현대문학",
            isbn="9788972756194",
            cover_image="https://image.aladin.co.kr/product/2936/68/cover500/8972756199_2.jpg",
            description="시간을 초월한 편지와 기적",
            price=13800,
            rating=4.7,
            review_count=4567,
            theme="healing",
            category="소설",
            published_date=date(2013, 8, 23),
            page_count=412
        ),
        Book(
            title="말의 품격",
            author="이기주",
            publisher="황소북스",
            isbn="9791186821886",
            cover_image="https://image.aladin.co.kr/product/12328/9/cover500/k032534839_1.jpg",
            description="말과 마음을 다스리는 법",
            price=14500,
            rating=4.3,
            review_count=3210,
            theme="healing",
            category="에세이",
            published_date=date(2017, 9, 1),
            page_count=256
        ),
        Book(
            title="여행의 이유",
            author="김영하",
            publisher="문학동네",
            isbn="9788954653640",
            cover_image="https://image.aladin.co.kr/product/16892/59/cover500/k022534892_1.jpg",
            description="떠나고 싶을 때 읽는 에세이",
            price=13000,
            rating=4.4,
            review_count=2890,
            theme="healing",
            category="에세이",
            published_date=date(2019, 4, 19),
            page_count=260
        ),
        Book(
            title="골목길 시인",
            author="이한샘",
            publisher="느낌이있는책",
            isbn="9791186697788",
            cover_image="https://image.aladin.co.kr/product/11907/60/cover500/k612534974_1.jpg",
            description="일상의 작은 행복을 찾는 시",
            price=13500,
            rating=4.5,
            review_count=1567,
            theme="healing",
            category="시",
            published_date=date(2017, 6, 15),
            page_count=192
        ),
        Book(
            title="연금술사",
            author="파울로 코엘료",
            publisher="문학동네",
            isbn="9788954605045",
            cover_image="https://image.aladin.co.kr/product/70/28/cover500/8954605044_2.jpg",
            description="꿈을 이루기 위한 여정",
            price=11000,
            rating=4.6,
            review_count=5678,
            theme="healing",
            category="소설",
            published_date=date(2001, 11, 15),
            page_count=248
        ),
        Book(
            title="채식주의자",
            author="한강",
            publisher="창비",
            isbn="9788936434120",
            cover_image="https://image.aladin.co.kr/product/70/54/cover500/8936434128_2.jpg",
            description="인간 존재의 폭력성과 고통에 대한 성찰",
            price=10800,
            rating=4.2,
            review_count=3456,
            theme="healing",
            category="소설",
            published_date=date(2007, 10, 30),
            page_count=188
        ),
        Book(
            title="죽고 싶지만 떡볶이는 먹고 싶어",
            author="백세희",
            publisher="흔",
            isbn="9791187058618",
            cover_image="https://image.aladin.co.kr/product/13907/62/cover500/k422534863_1.jpg",
            description="정신과 의사와 상담사의 따뜻한 대화",
            price=14000,
            rating=4.4,
            review_count=6789,
            theme="healing",
            category="에세이",
            published_date=date(2018, 5, 25),
            page_count=288
        ),
        Book(
            title="흔한남매",
            author="백난도, 정정한",
            publisher="미래엔아이세움",
            isbn="9791164138029",
            cover_image="https://image.aladin.co.kr/product/18526/43/cover500/k862636041_1.jpg",
            description="웃음과 공감을 주는 남매 이야기",
            price=11000,
            rating=4.7,
            review_count=2345,
            theme="healing",
            category="만화",
            published_date=date(2019, 5, 24),
            page_count=160
        ),
        Book(
            title="모든 순간이 너였다",
            author="하태완",
            publisher="시공사",
            isbn="9788952793379",
            cover_image="https://image.aladin.co.kr/product/9595/61/cover500/k672534851_1.jpg",
            description="사랑에 대한 짧고 깊은 이야기",
            price=12800,
            rating=4.3,
            review_count=4567,
            theme="healing",
            category="에세이",
            published_date=date(2017, 5, 30),
            page_count=232
        ),
        Book(
            title="살아있다는 것",
            author="정호승",
            publisher="열림원",
            isbn="9788970637891",
            cover_image="https://image.aladin.co.kr/product/70/54/cover500/8970637893_2.jpg",
            description="삶을 긍정하는 시",
            price=11000,
            rating=4.5,
            review_count=1890,
            theme="healing",
            category="시",
            published_date=date(2007, 10, 10),
            page_count=208
        ),
        Book(
            title="완전한 행복",
            author="정유정",
            publisher="은행나무",
            isbn="9788956607696",
            cover_image="https://image.aladin.co.kr/product/2936/67/cover500/8956607699_2.jpg",
            description="행복의 진정한 의미를 찾아가는 소설",
            price=13800,
            rating=4.4,
            review_count=2567,
            theme="healing",
            category="소설",
            published_date=date(2013, 8, 30),
            page_count=364
        ),
        Book(
            title="긍정의 배신",
            author="바버라 에런라이크",
            publisher="부키",
            isbn="9788960512726",
            cover_image="https://image.aladin.co.kr/product/2012/95/cover500/8960512729_2.jpg",
            description="긍정의 함정에서 벗어나기",
            price=16000,
            rating=4.2,
            review_count=1234,
            theme="healing",
            category="인문",
            published_date=date(2012, 6, 25),
            page_count=352
        ),
        Book(
            title="당신이 옳다",
            author="정혜신",
            publisher="해냄",
            isbn="9788965746683",
            cover_image="https://image.aladin.co.kr/product/16892/58/cover500/k252534891_1.jpg",
            description="공감과 위로의 대화법",
            price=14500,
            rating=4.6,
            review_count=3456,
            theme="healing",
            category="에세이",
            published_date=date(2018, 10, 1),
            page_count=280
        ),
        Book(
            title="보건교사 안은영",
            author="정세랑",
            publisher="민음사",
            isbn="9788937473685",
            cover_image="https://image.aladin.co.kr/product/9863/42/cover500/k302434851_1.jpg",
            description="판타지와 현실이 어우러진 소설",
            price=12800,
            rating=4.5,
            review_count=2890,
            theme="healing",
            category="소설",
            published_date=date(2015, 11, 27),
            page_count=264
        ),
        Book(
            title="어쩌면 별들이 너의 슬픔을 가져갈지도 몰라",
            author="김용택",
            publisher="마음산책",
            isbn="9788960900622",
            cover_image="https://image.aladin.co.kr/product/70/54/cover500/8960900621_2.jpg",
            description="위로가 되는 시 모음집",
            price=12000,
            rating=4.4,
            review_count=1567,
            theme="healing",
            category="시",
            published_date=date(2008, 9, 22),
            page_count=240
        ),
        
        # ========== 성장 테마 15권 (growth) ==========
        Book(
            title="생각하는 연습",
            author="나카니시 아쓰히로",
            publisher="더퀘스트",
            isbn="9791165210731",
            cover_image="https://image.aladin.co.kr/product/23494/54/cover500/k632635345_1.jpg",
            description="인생을 바꾸는 생각의 기술",
            price=14500,
            rating=4.4,
            review_count=1234,
            theme="growth",
            category="자기계발",
            published_date=date(2020, 5, 15),
            page_count=272
        ),
        Book(
            title="그릿",
            author="앤절라 더크워스",
            publisher="비즈니스북스",
            isbn="9791162540046",
            cover_image="https://image.aladin.co.kr/product/10907/60/cover500/k692534975_1.jpg",
            description="재능을 이기는 끈기의 힘",
            price=16000,
            rating=4.5,
            review_count=3456,
            theme="growth",
            category="자기계발",
            published_date=date(2016, 10, 4),
            page_count=432
        ),
        Book(
            title="마인드셋",
            author="캐럴 드웩",
            publisher="스몰빅라이프",
            isbn="9791186636541",
            cover_image="https://image.aladin.co.kr/product/9863/41/cover500/k762434850_1.jpg",
            description="성장 마인드셋의 힘",
            price=15000,
            rating=4.4,
            review_count=2345,
            theme="growth",
            category="자기계발",
            published_date=date(2017, 4, 19),
            page_count=348
        ),
        Book(
            title="몰입",
            author="황농문",
            publisher="리더스북",
            isbn="9788901072524",
            cover_image="https://image.aladin.co.kr/product/70/54/cover500/8901072521_2.jpg",
            description="최고의 나를 만드는 성공의 비밀",
            price=14000,
            rating=4.3,
            review_count=1890,
            theme="growth",
            category="자기계발",
            published_date=date(2007, 3, 14),
            page_count=308
        ),
        Book(
            title="총,균,쇠",
            author="제레드 다이아몬드",
            publisher="문학사상",
            isbn="9788970127248",
            cover_image="https://image.aladin.co.kr/product/70/21/cover500/8970127240_2.jpg",
            description="인류 문명의 비밀",
            price=23000,
            rating=4.7,
            review_count=4567,
            theme="growth",
            category="인문",
            published_date=date(2005, 12, 1),
            page_count=752
        ),
        Book(
            title="사피엔스",
            author="유발 하라리",
            publisher="김영사",
            isbn="9788934972464",
            cover_image="https://image.aladin.co.kr/product/6074/6/cover500/k822534554_1.jpg",
            description="인류의 역사와 미래",
            price=22000,
            rating=4.6,
            review_count=8901,
            theme="growth",
            category="인문",
            published_date=date(2015, 11, 27),
            page_count=636
        ),
        Book(
            title="호모 데우스",
            author="유발 하라리",
            publisher="김영사",
            isbn="9788934972471",
            cover_image="https://image.aladin.co.kr/product/10907/60/cover500/k222534975_1.jpg",
            description="미래 인류의 운명",
            price=22000,
            rating=4.5,
            review_count=5678,
            theme="growth",
            category="인문",
            published_date=date(2017, 5, 19),
            page_count=616
        ),
        Book(
            title="생각에 관한 생각",
            author="대니얼 카너먼",
            publisher="김영사",
            isbn="9788934955467",
            cover_image="https://image.aladin.co.kr/product/2328/62/cover500/8934955465_2.jpg",
            description="인간의 사고 시스템에 대한 통찰",
            price=18000,
            rating=4.4,
            review_count=2890,
            theme="growth",
            category="심리",
            published_date=date(2012, 4, 10),
            page_count=688
        ),
        Book(
            title="정의란 무엇인가",
            author="마이클 샌델",
            publisher="김영사",
            isbn="9788934942467",
            cover_image="https://image.aladin.co.kr/product/2012/48/cover500/8934942460_2.jpg",
            description="정의에 대한 철학적 탐구",
            price=15000,
            rating=4.5,
            review_count=6789,
            theme="growth",
            category="인문",
            published_date=date(2010, 5, 20),
            page_count=404
        ),
        Book(
            title="이기적 유전자",
            author="리처드 도킨스",
            publisher="을유문화사",
            isbn="9788932473901",
            cover_image="https://image.aladin.co.kr/product/70/21/cover500/8932473900_2.jpg",
            description="진화론의 새로운 관점",
            price=18000,
            rating=4.6,
            review_count=4567,
            theme="growth",
            category="과학",
            published_date=date(2006, 11, 29),
            page_count=556
        ),
        Book(
            title="시간은 흐르지 않는다",
            author="카를로 로벨리",
            publisher="쌤앤파커스",
            isbn="9788965706359",
            cover_image="https://image.aladin.co.kr/product/18526/42/cover500/k312636040_1.jpg",
            description="시간의 본질에 대한 물리학적 탐구",
            price=16000,
            rating=4.3,
            review_count=2345,
            theme="growth",
            category="과학",
            published_date=date(2019, 4, 9),
            page_count=256
        ),
        Book(
            title="우아한 거짓말",
            author="김려령",
            publisher="창비",
            isbn="9788936433727",
            cover_image="https://image.aladin.co.kr/product/2012/48/cover500/8936433725_2.jpg",
            description="학교 폭력에 대한 진솔한 이야기",
            price=10800,
            rating=4.4,
            review_count=3456,
            theme="growth",
            category="소설",
            published_date=date(2009, 9, 11),
            page_count=264
        ),
        Book(
            title="언어의 온도",
            author="이기주",
            publisher="말글터",
            isbn="9791187257011",
            cover_image="https://image.aladin.co.kr/product/9595/63/cover500/k812534853_1.jpg",
            description="말과 글의 따뜻한 힘",
            price=13500,
            rating=4.5,
            review_count=5678,
            theme="growth",
            category="에세이",
            published_date=date(2016, 8, 22),
            page_count=268
        ),
        Book(
            title="팩트풀니스",
            author="한스 로슬링",
            publisher="김영사",
            isbn="9788934986058",
            cover_image="https://image.aladin.co.kr/product/18526/43/cover500/k442636042_1.jpg",
            description="세상을 바로 보는 열 가지 방법",
            price=17000,
            rating=4.7,
            review_count=4890,
            theme="growth",
            category="인문",
            published_date=date(2019, 3, 4),
            page_count=392
        ),
        Book(
            title="밤의 여행자들",
            author="위화",
            publisher="푸른숲",
            isbn="9791159252464",
            cover_image="https://image.aladin.co.kr/product/10907/59/cover500/k612534974_1.jpg",
            description="중국 현대사를 관통하는 이야기",
            price=14800,
            rating=4.4,
            review_count=2345,
            theme="growth",
            category="소설",
            published_date=date(2017, 5, 12),
            page_count=392
        ),
    ]
    
    # ========== 큐레이터 추천 10권 ==========
    curator_picks = ["트렌드 코리아 2025", "아몬드", "달러구트 꿈 백화점", "딥 워크", 
                     "나미야 잡화점의 기적", "사피엔스", "미드나잇 라이브러리",
                     "원씽", "당신이 옳다", "팩트풀니스"]
    
    for book in books:
        if book.title in curator_picks:
            book.is_curator_pick = True
    
    return books


def seed_books():
    """도서 데이터 시딩 실행"""
    db = SessionLocal()
    
    try:
        print("🌱 도서 데이터 시딩 시작...")
        
        # 기존 데이터 삭제
        clear_books(db)
        
        # Mock 데이터 생성
        books = create_mock_books()
        
        # 데이터베이스에 추가
        db.add_all(books)
        db.commit()
        
        # 결과 확인
        total_count = db.query(Book).count()
        popular_count = db.query(Book).filter(Book.is_popular == True).count()
        work_count = db.query(Book).filter(Book.theme == "work").count()
        healing_count = db.query(Book).filter(Book.theme == "healing").count()
        growth_count = db.query(Book).filter(Book.theme == "growth").count()
        curator_count = db.query(Book).filter(Book.is_curator_pick == True).count()
        
        print(f"\n✅ 도서 데이터 시딩 완료!")
        print(f"   📚 전체 도서: {total_count}권")
        print(f"   🔥 인기 도서: {popular_count}권")
        print(f"   💼 업무 테마: {work_count}권")
        print(f"   🌿 힐링 테마: {healing_count}권")
        print(f"   🌱 성장 테마: {growth_count}권")
        print(f"   ⭐ 큐레이터 추천: {curator_count}권\n")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_books()
