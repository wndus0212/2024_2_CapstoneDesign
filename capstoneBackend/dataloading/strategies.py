import backtrader as bt
class FixedAllocationStrategy(bt.Strategy):
    params = (
        ('rebalance_months', 1),  # 리밸런싱 간격 (개월 수)
        ('portfolio_name', 'Default Portfolio')  # 포트폴리오 이름
    )

    def __init__(self, allocation):
        """
        allocation: 각 종목의 초기 투자 비율 딕셔너리, 예: {"AAPL": 0.4, "MSFT": 0.3, "JPM": 0.3}
        """
        self.allocation = allocation
        self.last_rebalance = None  # 마지막 리밸런싱 날짜 저장
        self.rebalance_log = []  # 리밸런싱 결과 저장 리스트
        self.portfolio_values = []

    def next(self):
        # 현재 날짜 및 포트폴리오 가치 기록
        current_date = self.datas[0].datetime.date(0)
        current_value = self.broker.get_value()
        self.portfolio_values.append(current_value)

        # 첫 번째 리밸런싱 실행 시점 설정
        if not self.last_rebalance:
            self.last_rebalance = current_date

        # 리밸런싱: 현재 날짜와 마지막 리밸런싱 날짜 비교
        months_since_rebalance = (current_date.year - self.last_rebalance.year) * 12 + (
                    current_date.month - self.last_rebalance.month)
        if months_since_rebalance >= self.params.rebalance_months:
            self.rebalance_portfolio()
            self.last_rebalance = current_date

    def rebalance_portfolio(self):
        """
        목표 비중에 맞춰 포트폴리오를 리밸런싱합니다.
        """
        total_value = self.broker.get_value()
        positions = {}  # 현재 포지션 정보 저장

        for data in self.datas:
            ticker = data._name
            if ticker not in self.allocation:
                continue  # allocation에 포함되지 않은 종목은 건너뜀

            target_value = total_value * self.allocation.get(ticker, 0)
            current_position = self.getposition(data).size
            current_price = data.close[0]
            target_position = target_value // current_price

            if current_position < target_position:
                self.buy(data=data, size=target_position - current_position)
            elif current_position > target_position:
                self.sell(data=data, size=current_position - target_position)

            # 포지션 정보 저장 (allocation에 포함된 종목만 기록)
            positions[ticker] = target_position

        # 리밸런싱 로그 저장
        self.rebalance_log.append({
            'portfolio_name': self.params.portfolio_name,
            'date': self.last_rebalance,
            'portfolio_value': total_value,
            'positions': positions,
        })

        print(f"리밸런싱 완료: {self.last_rebalance}")
        print(f"포트폴리오 이름: {self.params.portfolio_name}")
        print(f"포지션: {positions}")