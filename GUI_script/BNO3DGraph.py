import pyqtgraph.opengl as gl
from PyQt5.QtGui import QVector3D
from PyQt5.QtCore import QTimer
import numpy as np

class BNO3DGraph:
    """BNO 데이터를 3D로 시각화하는 클래스"""

    def __init__(self, parent_widget):
        self.parent_widget = parent_widget

        # 3D 그래프 위젯 생성
        self.gl_widget = gl.GLViewWidget(parent_widget)
        self.gl_widget.setGeometry(0, 0, 371, 361)  # BNO3D 위젯의 크기에 맞춤
        self.gl_widget.setCameraPosition(distance=10)  # 카메라 위치 설정

        # 3D 축 추가
        self.axis = gl.GLAxisItem()
        self.gl_widget.addItem(self.axis)

        # 3D 객체 초기화 (큐브로 표현)
        # self.cube = gl.GLMeshItem(
        #     meshdata=gl.MeshData.createCube(),
        #     color=(0, 1, 0, 0.5),  # 초록색 반투명 큐브
        #     glOptions='translucent'
        # )
        # self.gl_widget.addItem(self.cube)

        # 타이머 설정 (100ms 간격)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_3d_graph)
        self.timer.start(100)

    def update_3d_graph(self, yaw=0, pitch=0, roll=0):
        """BNO 데이터를 받아 3D 그래프를 갱신"""
        # 오일러 각을 사용하여 회전 행렬 생성
        rotation_matrix = self.euler_to_matrix(yaw, pitch, roll)

        # 큐브의 회전 적용
        self.cube.resetTransform()
        self.cube.rotate(yaw, 0, 0, 1)  # Z축 회전 (Yaw)
        self.cube.rotate(pitch, 1, 0, 0)  # X축 회전 (Pitch)
        self.cube.rotate(roll, 0, 1, 0)  # Y축 회전 (Roll)

    def euler_to_matrix(self, yaw, pitch, roll):
        """오일러 각을 회전 행렬로 변환"""
        # Yaw (Z축 회전)
        yaw_matrix = np.array([
            [np.cos(yaw), -np.sin(yaw), 0],
            [np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1]
        ])

        # Pitch (X축 회전)
        pitch_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)]
        ])

        # Roll (Y축 회전)
        roll_matrix = np.array([
            [np.cos(roll), 0, np.sin(roll)],
            [0, 1, 0],
            [-np.sin(roll), 0, np.cos(roll)]
        ])

        # 최종 회전 행렬
        rotation_matrix = np.dot(roll_matrix, np.dot(pitch_matrix, yaw_matrix))
        return rotation_matrix