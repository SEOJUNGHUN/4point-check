# 금융분석도구 📊

종합 금융 데이터 분석 모바일 앱

## 기능

### 🏠 메인 대시보드
- 4가지 핵심 모니터링 지표 개요
- 투자 관점에서의 중요 포인트 설명

### 📊 주식 데이터
- TradingView 최고 순이익 주식 정보
- 실시간 데이터 업데이트

### 📈 S&P500 이익수익률
- S&P500 vs 미국채 금리 비교
- 주식 시장 매력도 분석

### 💰 M2 통화량
- 미국 연방준비제도 M2 통화량 데이터
- 인플레이션 및 유동성 지표

### 💱 USD/JPY 환율
- 달러/엔 환율 실시간 정보
- 글로벌 투자 심리 지표

## 기술 스택

- **Frontend**: Kivy (Python)
- **Data**: BeautifulSoup, Requests
- **Build**: Buildozer
- **CI/CD**: GitHub Actions

## 설치 및 실행

### 데스크톱에서 실행
```bash
pip install kivy requests beautifulsoup4 lxml
python main.py
```

### 안드로이드 APK 빌드
GitHub Actions를 통해 자동으로 APK가 빌드됩니다.

1. 이 저장소를 Fork하거나 Clone
2. 코드 수정 후 Push
3. Actions 탭에서 빌드 진행 상황 확인
4. 완료 후 Artifacts에서 APK 다운로드

## 라이선스

MIT License

## 기여

Pull Request를 환영합니다!