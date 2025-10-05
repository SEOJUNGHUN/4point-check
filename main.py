# -*- coding: utf-8 -*-
# 모바일용 금융 분석 앱 (Kivy)

import requests
from bs4 import BeautifulSoup
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
import threading

# URL 설정
TV_URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-highest-net-income/"
EARNINGS_URL = "https://www.currentmarketvaluation.com/models/earnings-yield-gap.php"
M2_URL = "https://fred.stlouisfed.org/series/M2SL"
USDJPY_URL = "https://kr.investing.com/currencies/usd-jpy"

class MainDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # 제목
        title = Label(
            text='[size=24][b]핵심 모니터링 지표[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=60,
            text_size=(None, None)
        )
        self.add_widget(title)
        
        # 설명
        desc = Label(
            text='불확실성의 시대에 현명한 투자는 객관적인 지표 변화를 지속적으로 추적하고 자신의 전략을 능동적 조정이 필요',
            text_size=(None, None),
            size_hint_y=None,
            height=80,
            halign='center'
        )
        self.add_widget(desc)
        
        # 스크롤 가능한 카드 영역
        scroll = ScrollView()
        cards_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        cards_layout.bind(minimum_height=cards_layout.setter('height'))
        
        # 4개 지표 카드
        cards = [
            {
                'title': '📈 미국 기업 순이익률',
                'desc': '강세로 근간입니다. 이익률의 견고함이 성장 동력의 지속성을 판단하는 핵심입니다',
                'status': '현재: AI 기업들의 PER은 47.6배로, 전체 산업(19.0배)의 2.5배'
            },
            {
                'title': '⚖️ S&P 500 이익수익률 vs. 미국채 금리',
                'desc': '주식의 상대적 매력도입니다. 역전 폭이 확대될 경우 주식장의 강력한 위험 신호임',
                'status': '현재: 주식보다 채권이 더 매력적인 이례적 상황임'
            },
            {
                'title': '💰 광의통화(M2) 증가 속도',
                'desc': '민간 신용 창출의 바로미터입니다. M2의 꾸준한 확장은 유동성 장세의 지속성을 나타냄',
                'status': '2025-26년 예상: 준비금 변동과 지표로 작용할 것으로 예상됨'
            },
            {
                'title': '🌐 달러/엔 환율 동향',
                'desc': '엔화 강세는 엔 캐리 트레이드 청산을 촉발, 글로벌 유동성 위축의 잠재적 트리거가 됨',
                'status': '2025년 이후: 달러/엔 환율의 변화는 글로벌 투자에 큰 영향을 미칠 것임'
            }
        ]
        
        for card_data in cards:
            card = self.create_card(card_data)
            cards_layout.add_widget(card)
        
        scroll.add_widget(cards_layout)
        self.add_widget(scroll)
        
        # 하단 메시지
        bottom_msg = Label(
            text='[b]투자자의 지혜:[/b] 맹목적인 낙관이나 비관은 모두 경계해야 하며, 객관적인 지표 변화를 지속적으로 추적하며 자신의 투자 전략을 능동적으로 조정하는 것입니다.',
            markup=True,
            text_size=(None, None),
            size_hint_y=None,
            height=100,
            halign='center'
        )
        self.add_widget(bottom_msg)
    
    def create_card(self, card_data):
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=200,
            padding=15,
            spacing=10
        )
        
        # 제목
        title = Label(
            text=f'[size=18][b]{card_data["title"]}[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=40,
            text_size=(None, None),
            halign='left'
        )
        
        # 설명
        desc = Label(
            text=f'[size=14]{card_data["desc"]}[/size]',
            markup=True,
            text_size=(None, None),
            size_hint_y=None,
            height=80,
            halign='left'
        )
        
        # 현재 상태
        status = Label(
            text=f'[size=12][color=ff6600]💡 {card_data["status"]}[/color][/size]',
            markup=True,
            text_size=(None, None),
            size_hint_y=None,
            height=60,
            halign='left'
        )
        
        card.add_widget(title)
        card.add_widget(desc)
        card.add_widget(status)
        
        return card

class DataTab(BoxLayout):
    def __init__(self, title, url, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.url = url
        
        # 제목
        title_label = Label(
            text=f'[size=20][b]{title}[/b][/size]',
            markup=True,
            size_hint_y=None,
            height=50
        )
        self.add_widget(title_label)
        
        # 버튼들
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        refresh_btn = Button(text='새로고침', size_hint_x=0.5)
        refresh_btn.bind(on_press=self.refresh_data)
        
        open_btn = Button(text='브라우저에서 열기', size_hint_x=0.5)
        open_btn.bind(on_press=self.open_browser)
        
        btn_layout.add_widget(refresh_btn)
        btn_layout.add_widget(open_btn)
        self.add_widget(btn_layout)
        
        # 데이터 표시 영역
        self.data_label = Label(
            text='데이터를 로드하는 중...',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        
        scroll = ScrollView()
        scroll.add_widget(self.data_label)
        self.add_widget(scroll)
        
        # 초기 데이터 로드
        self.refresh_data()
    
    def refresh_data(self, *args):
        # 백그라운드에서 데이터 로드
        threading.Thread(target=self.load_data).start()
    
    def load_data(self):
        try:
            hdrs = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
            }
            r = requests.get(self.url, headers=hdrs, timeout=10)
            r.raise_for_status()
            
            # 간단한 정보 추출
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text() if title else "데이터"
            
            # UI 업데이트는 메인 스레드에서
            Clock.schedule_once(lambda dt: self.update_data(title_text))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_data(f"데이터 로드 오류: {str(e)}"))
    
    def update_data(self, data):
        self.data_label.text = f'[size=14]{data}[/size]\n\n실시간 차트와 상세 데이터는 "브라우저에서 열기" 버튼을 클릭하세요.'
        self.data_label.markup = True
    
    def open_browser(self, *args):
        try:
            webbrowser.open(self.url)
        except:
            popup = Popup(
                title='알림',
                content=Label(text='브라우저를 열 수 없습니다.'),
                size_hint=(0.8, 0.4)
            )
            popup.open()

class FinanceApp(App):
    def build(self):
        # 탭 패널 생성
        tab_panel = TabbedPanel(do_default_tab=False)
        
        # 메인 대시보드 탭
        main_tab = TabbedPanelItem(text='🏠 메인')
        main_tab.add_widget(MainDashboard())
        tab_panel.add_widget(main_tab)
        
        # 데이터 탭들
        tabs_data = [
            ('📊 주식', TV_URL),
            ('📈 S&P500', EARNINGS_URL),
            ('💰 M2', M2_URL),
            ('💱 환율', USDJPY_URL)
        ]
        
        for tab_name, url in tabs_data:
            tab = TabbedPanelItem(text=tab_name)
            tab.add_widget(DataTab(tab_name, url))
            tab_panel.add_widget(tab)
        
        return tab_panel

if __name__ == '__main__':
    FinanceApp().run()