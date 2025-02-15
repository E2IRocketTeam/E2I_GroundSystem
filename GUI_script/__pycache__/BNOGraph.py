import pyqtgraph as pg
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout

class BNOGraph:
    """BNO 데이터를 그래프로 시각화하는 클래스"""
    
    def __init__(self, parent_widget, serial_port):
        self.serial_port = serial_port  # 시리얼 포트
        self.time_counter = 0  # X축 카운터

        # 데이터 저장용 리스트
        self.yaw_data = []
        self.pitch_data = []
        self.roll_data = []
        self.time_data = []

        # PyQtGraph 초기화
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')

        # 폰트 설정
        font = QFont("Arial", 12, QFont.Bold)
        self.plot_widget.getAxis("bottom").setStyle(tickFont=font)
        self.plot_widget.getAxis("left").setStyle(tickFont=font)

        # 축 스타일 적용
        self.plot_widget.getAxis("bottom").setPen(pg.mkPen("black", width=2))
        self.plot_widget.getAxis("left").setPen(pg.mkPen("black", width=2))

        # 레이아웃에 그래프 추가
        layout = QVBoxLayout(parent_widget)
        layout.addWidget(self.plot_widget)
        parent_widget.setLayout(layout)

        # 그래프 곡선 추가
        self.yaw_curve = self.plot_widget.plot(pen=pg.mkPen("r", width=2), name="Yaw")
        self.pitch_curve = self.plot_widget.plot(pen=pg.mkPen("g", width=2), name="Pitch")
        self.roll_curve = self.plot_widget.plot(pen=pg.mkPen("b", width=2), name="Roll")

        # 타이머 설정 (100ms 간격)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)

    def update_graph(self):
        """시리얼 데이터를 읽고 그래프를 갱신"""
        if self.serial_port.in_waiting > 0:
            try:
                # 시리얼 데이터 읽기
                line = self.serial_port.readline().decode('utf-8').strip()
                values = line.split(',')

                if len(values) == 3:
                    raw_yaw, raw_pitch, raw_roll = map(float, values)

                    # 데이터 저장
                    self.yaw_data.append(raw_yaw)
                    self.pitch_data.append(raw_pitch)
                    self.roll_data.append(raw_roll)
                    self.time_data.append(self.time_counter)
                    self.time_counter += 1

                    # 최근 100개 데이터만 유지
                    if len(self.yaw_data) > 100:
                        self.yaw_data.pop(0)
                        self.pitch_data.pop(0)
                        self.roll_data.pop(0)
                        self.time_data.pop(0)

                    # 그래프 갱신
                    self.yaw_curve.setData(self.time_data, self.yaw_data)
                    self.pitch_curve.setData(self.time_data, self.pitch_data)
                    self.roll_curve.setData(self.time_data, self.roll_data)

            except Exception as e:
                print(f"데이터 읽기 오류: {e}")
