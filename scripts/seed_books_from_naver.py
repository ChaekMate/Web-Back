import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
import time
from datetime import datetime
from app.core.database import SessionLocal
from app.models.book import Book
from app.core.config import settings

# 네이버 API 설정
NAVER_API_URL = "https://openapi.naver.com/v1/search/book.json"
CLIENT_ID = settings.NAVER_CLIENT_ID
CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

# 검색 키워드 (카테고리별)
SEARCH_QUERIES = {
    "work": [
        "경제", "경영", "자기계발", "비즈니스", "마케팅",
        "리더십", "IT", "프로그래밍", "업무", "생산성"
    ],
    "healing": [
        "소설", "에세이", "시", "힐링", "위로",
        "감성", "여행", "일상", "공감"
    ],
    "growth": [
        "인문", "철학", "역사", "과학", "심리학",
        "사회", "교양", "성장", "사고"
    ]
}

# 테마 매핑 (출판사/카테고리 기반)
THEME_KEYWORDS = {
    "work": ["경제", "경영", "자기계발", "비즈니스", "마케팅", "IT", "컴퓨터"],
    "healing": ["소설", "에세이", "시", "문학", "여행"],
    "growth": ["인문", "철학", "역사", "과학", "심리", "사회"]
}


def search_naver_books(query, display=10):
    """네이버 책 검색 API 호출"""
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "sim"  # sim: 정확도순, date: 출간일순
    }
    
    try:
        print(f"  📡 검색 중: '{query}'")
        response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])
        else:
            print(f"    ❌ API 오류: {response.status_code}")
            return []
    except Exception as e:
        print(f"    ❌ 에러: {e}")
        return []


def determine_theme(title, description):
    """제목과 설명으로 테마 결정"""
    text = f"{title} {description}".lower()
    
    scores = {"work": 0, "healing": 0, "growth": 0}
    
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[theme] += 1
    
    # 최고 점수의 테마 반환, 동점이면 growth
    max_theme = max(scores, key=scores.get)
    return max_theme if scores[max_theme] > 0 else "growth"


def clean_html_tags(text):
    """HTML 태그 제거"""
    import re
    return re.sub('<[^<]+?>', '', text)


def parse_naver_item(item, theme, index):
    """네이버 아이템을 Book 모델로 변환"""
    
    # HTML 태그 제거
    title = clean_html_tags(item.get("title", "제목 없음"))
    author = clean_html_tags(item.get("author", "저자 미상"))
    description = clean_html_tags(item.get("description", ""))
    
    # 출판일 파싱
    try:
        pub_date_str = item.get("pubdate", "")
        if pub_date_str and len(pub_date_str) == 8:
            pub_date = datetime.strptime(pub_date_str, "%Y%m%d").date()
        else:
            pub_date = None
    except:
        pub_date = None
    
    # 가격 파싱
    try:
        price = int(item.get("discount", item.get("price", 0)))
    except:
        price = 0
    
    # ISBN (isbn13 우선, 없으면 isbn)
    isbn = item.get("isbn", "").split()[-1] if item.get("isbn") else ""
    
    # 인기도 및 큐레이터 추천
    is_popular = index <= 5
    is_curator_pick = index <= 3
    
    return Book(
        title=title,
        author=author,
        publisher=item.get("publisher", ""),
        isbn=isbn,
        cover_image=item.get("image", ""),
        description=description,
        price=price,
        rating=0.0,
        review_count=0,
        theme=theme,
        category="",
        is_popular=is_popular,
        is_curator_pick=is_curator_pick,
        published_date=pub_date,
        page_count=None
    )


def seed_books_from_naver():
    """네이버 API로 도서 데이터 시딩"""
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ 네이버 API 키가 설정되지 않았습니다.")
        print("   .env 파일에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 추가해주세요.")
        return
    
    db = SessionLocal()
    
    try:
        print("🌱 네이버 책 검색 API로 도서 데이터 가져오기 시작...\n")
        
        # 기존 데이터 삭제
        db.query(Book).delete()
        db.commit()
        print("✅ 기존 도서 데이터 삭제 완료\n")
        
        all_books = []
        seen_isbns = set()
        
        # 테마별로 도서 수집
        for theme, queries in SEARCH_QUERIES.items():
            print(f"\n📚 [{theme.upper()}] 테마 도서 수집 중...")
            theme_count = 0
            
            for query in queries:
                if theme_count >= 20:  # 테마별 최대 20권
                    break
                
                items = search_naver_books(query, display=10)
                
                for i, item in enumerate(items, 1):
                    isbn = item.get("isbn", "").split()[-1] if item.get("isbn") else ""
                    
                    # ISBN 중복 체크
                    if isbn and isbn in seen_isbns:
                        continue
                    
                    if isbn:
                        seen_isbns.add(isbn)
                    
                    # 테마별 제한
                    if theme_count >= 20:
                        break
                    
                    book = parse_naver_item(item, theme, theme_count + 1)
                    all_books.append(book)
                    theme_count += 1
                    
                    title = clean_html_tags(item.get("title", ""))
                    print(f"    ✅ {title}")
                
                # API 요청 제한 방지
                time.sleep(0.1)
            
            print(f"  ✅ {theme} 테마: {theme_count}권 수집 완료")
        
        # 데이터베이스에 저장
        if all_books:
            db.add_all(all_books)
            db.commit()
            
            # 통계
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
        else:
            print("\n⚠️  수집된 도서가 없습니다.")
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_books_from_naver()
