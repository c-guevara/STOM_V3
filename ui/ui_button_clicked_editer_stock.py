
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QSize, QRect
from PyQt5.QtWidgets import QMessageBox, QApplication
from multiprocessing import Process
from backtest.optimiz import Optimize
from backtest.backtest import BackTest
from backtest.backfinder import BackFinder
from backtest.optimiz_conditions import OptimizeConditions
from backtest.rolling_walk_forward_test import RollingWalkForwardTest
from backtest.optimiz_genetic_algorithm import OptimizeGeneticAlgorithm
from ui.set_style import style_bc_by, style_bc_dk, style_bc_bs, style_bc_bd
from ui.set_text import testtext, rwfttext, gaoptext, vedittxt, optitext, condtext, cedittxt, example_finder
from utility.static import error_decorator


def group_animation_01(ui):
    """stock_opti_test_editer, stock_rwf_test_editer, stock_opti_editer용 그룹 애니메이션"""
    # 위젯들의 현재 지오메트리 저장
    current_geo_03 = ui.ss_textEditttt_03.geometry()
    current_geo_04 = ui.ss_textEditttt_04.geometry()
    current_geo_05 = ui.ss_textEditttt_05.geometry()
    current_geo_combo = ui.svc_comboBoxxx_02.geometry()
    current_geo_line = ui.svc_lineEdittt_02.geometry()
    current_geo_btn03 = ui.svc_pushButton_03.geometry()
    current_geo_btn04 = ui.svc_pushButton_04.geometry()
    current_geo_zoo01 = ui.szoo_pushButon_01.geometry()
    current_geo_zoo02 = ui.szoo_pushButon_02.geometry()
    
    # 목표 지오메트리 설정
    target_geo_03 = QRect(7, 10, 647, 740 if ui.extend_window else 463)
    target_geo_04 = QRect(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    target_geo_05 = QRect(659, 10, 347, 1347 if ui.extend_window else 740)
    target_geo_combo = QRect(1012, 115, 165, 30)
    target_geo_line = QRect(1182, 115, 165, 30)
    target_geo_btn03 = QRect(1012, 150, 165, 30)
    target_geo_btn04 = QRect(1182, 150, 165, 30)
    target_geo_zoo01 = QRect(584, 15, 50, 20)
    target_geo_zoo02 = QRect(584, 761 if ui.extend_window else 483, 50, 20)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 지오메트리 애니메이션 생성
    anim_03 = QPropertyAnimation(ui.ss_textEditttt_03, b'geometry')
    anim_03.setDuration(500)
    anim_03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_03.setStartValue(current_geo_03)
    anim_03.setEndValue(target_geo_03)
    
    anim_04 = QPropertyAnimation(ui.ss_textEditttt_04, b'geometry')
    anim_04.setDuration(500)
    anim_04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_04.setStartValue(current_geo_04)
    anim_04.setEndValue(target_geo_04)
    
    anim_05 = QPropertyAnimation(ui.ss_textEditttt_05, b'geometry')
    anim_05.setDuration(500)
    anim_05.setEasingCurve(QEasingCurve.InOutCirc)
    anim_05.setStartValue(current_geo_05)
    anim_05.setEndValue(target_geo_05)
    
    anim_combo = QPropertyAnimation(ui.svc_comboBoxxx_02, b'geometry')
    anim_combo.setDuration(500)
    anim_combo.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo.setStartValue(current_geo_combo)
    anim_combo.setEndValue(target_geo_combo)
    
    anim_line = QPropertyAnimation(ui.svc_lineEdittt_02, b'geometry')
    anim_line.setDuration(500)
    anim_line.setEasingCurve(QEasingCurve.InOutCirc)
    anim_line.setStartValue(current_geo_line)
    anim_line.setEndValue(target_geo_line)
    
    anim_btn03 = QPropertyAnimation(ui.svc_pushButton_03, b'geometry')
    anim_btn03.setDuration(500)
    anim_btn03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn03.setStartValue(current_geo_btn03)
    anim_btn03.setEndValue(target_geo_btn03)
    
    anim_btn04 = QPropertyAnimation(ui.svc_pushButton_04, b'geometry')
    anim_btn04.setDuration(500)
    anim_btn04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn04.setStartValue(current_geo_btn04)
    anim_btn04.setEndValue(target_geo_btn04)
    
    anim_zoo01 = QPropertyAnimation(ui.szoo_pushButon_01, b'geometry')
    anim_zoo01.setDuration(500)
    anim_zoo01.setEasingCurve(QEasingCurve.InOutCirc)
    anim_zoo01.setStartValue(current_geo_zoo01)
    anim_zoo01.setEndValue(target_geo_zoo01)
    
    anim_zoo02 = QPropertyAnimation(ui.szoo_pushButon_02, b'geometry')
    anim_zoo02.setDuration(500)
    anim_zoo02.setEasingCurve(QEasingCurve.InOutCirc)
    anim_zoo02.setStartValue(current_geo_zoo02)
    anim_zoo02.setEndValue(target_geo_zoo02)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_03)
    ui.animation_group.addAnimation(anim_04)
    ui.animation_group.addAnimation(anim_05)
    ui.animation_group.addAnimation(anim_combo)
    ui.animation_group.addAnimation(anim_line)
    ui.animation_group.addAnimation(anim_btn03)
    ui.animation_group.addAnimation(anim_btn04)
    ui.animation_group.addAnimation(anim_zoo01)
    ui.animation_group.addAnimation(anim_zoo02)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_02(ui):
    """stock_opti_ga_editer용 그룹 애니메이션"""
    # 위젯들의 현재 지오메트리 저장
    current_geo_03 = ui.ss_textEditttt_03.geometry()
    current_geo_04 = ui.ss_textEditttt_04.geometry()
    current_geo_06 = ui.ss_textEditttt_06.geometry()
    current_geo_combo = ui.svc_comboBoxxx_02.geometry()
    current_geo_line = ui.svc_lineEdittt_02.geometry()
    current_geo_btn03 = ui.svc_pushButton_03.geometry()
    current_geo_btn04 = ui.svc_pushButton_04.geometry()
    current_geo_combo2 = ui.sva_comboBoxxx_01.geometry()
    current_geo_line2 = ui.sva_lineEdittt_01.geometry()
    current_geo_btn04_2 = ui.sva_pushButton_04.geometry()
    current_geo_btn05 = ui.sva_pushButton_05.geometry()
    current_geo_zoo01 = ui.szoo_pushButon_01.geometry()
    current_geo_zoo02 = ui.szoo_pushButon_02.geometry()
    
    # 목표 지오메트리 설정
    target_geo_03 = QRect(7, 10, 647, 740 if ui.extend_window else 463)
    target_geo_04 = QRect(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    target_geo_06 = QRect(659, 10, 347, 1347 if ui.extend_window else 740)
    target_geo_combo = QRect(1012, 115, 165, 30)
    target_geo_line = QRect(1182, 115, 165, 30)
    target_geo_btn03 = QRect(1012, 150, 165, 30)
    target_geo_btn04 = QRect(1182, 150, 165, 30)
    target_geo_combo2 = QRect(1012, 115, 165, 30)
    target_geo_line2 = QRect(1182, 115, 165, 30)
    target_geo_btn04_2 = QRect(1012, 150, 165, 30)
    target_geo_btn05 = QRect(1182, 150, 165, 30)
    target_geo_zoo01 = QRect(584, 15, 50, 20)
    target_geo_zoo02 = QRect(584, 761 if ui.extend_window else 483, 50, 20)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 지오메트리 애니메이션 생성
    anim_03 = QPropertyAnimation(ui.ss_textEditttt_03, b'geometry')
    anim_03.setDuration(500)
    anim_03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_03.setStartValue(current_geo_03)
    anim_03.setEndValue(target_geo_03)
    
    anim_04 = QPropertyAnimation(ui.ss_textEditttt_04, b'geometry')
    anim_04.setDuration(500)
    anim_04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_04.setStartValue(current_geo_04)
    anim_04.setEndValue(target_geo_04)
    
    anim_06 = QPropertyAnimation(ui.ss_textEditttt_06, b'geometry')
    anim_06.setDuration(500)
    anim_06.setEasingCurve(QEasingCurve.InOutCirc)
    anim_06.setStartValue(current_geo_06)
    anim_06.setEndValue(target_geo_06)
    
    anim_combo = QPropertyAnimation(ui.svc_comboBoxxx_02, b'geometry')
    anim_combo.setDuration(500)
    anim_combo.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo.setStartValue(current_geo_combo)
    anim_combo.setEndValue(target_geo_combo)
    
    anim_line = QPropertyAnimation(ui.svc_lineEdittt_02, b'geometry')
    anim_line.setDuration(500)
    anim_line.setEasingCurve(QEasingCurve.InOutCirc)
    anim_line.setStartValue(current_geo_line)
    anim_line.setEndValue(target_geo_line)
    
    anim_btn03 = QPropertyAnimation(ui.svc_pushButton_03, b'geometry')
    anim_btn03.setDuration(500)
    anim_btn03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn03.setStartValue(current_geo_btn03)
    anim_btn03.setEndValue(target_geo_btn03)
    
    anim_btn04 = QPropertyAnimation(ui.svc_pushButton_04, b'geometry')
    anim_btn04.setDuration(500)
    anim_btn04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn04.setStartValue(current_geo_btn04)
    anim_btn04.setEndValue(target_geo_btn04)
    
    anim_combo2 = QPropertyAnimation(ui.sva_comboBoxxx_01, b'geometry')
    anim_combo2.setDuration(500)
    anim_combo2.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo2.setStartValue(current_geo_combo2)
    anim_combo2.setEndValue(target_geo_combo2)
    
    anim_line2 = QPropertyAnimation(ui.sva_lineEdittt_01, b'geometry')
    anim_line2.setDuration(500)
    anim_line2.setEasingCurve(QEasingCurve.InOutCirc)
    anim_line2.setStartValue(current_geo_line2)
    anim_line2.setEndValue(target_geo_line2)
    
    anim_btn04_2 = QPropertyAnimation(ui.sva_pushButton_04, b'geometry')
    anim_btn04_2.setDuration(500)
    anim_btn04_2.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn04_2.setStartValue(current_geo_btn04_2)
    anim_btn04_2.setEndValue(target_geo_btn04_2)
    
    anim_btn05 = QPropertyAnimation(ui.sva_pushButton_05, b'geometry')
    anim_btn05.setDuration(500)
    anim_btn05.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn05.setStartValue(current_geo_btn05)
    anim_btn05.setEndValue(target_geo_btn05)
    
    anim_zoo01 = QPropertyAnimation(ui.szoo_pushButon_01, b'geometry')
    anim_zoo01.setDuration(500)
    anim_zoo01.setEasingCurve(QEasingCurve.InOutCirc)
    anim_zoo01.setStartValue(current_geo_zoo01)
    anim_zoo01.setEndValue(target_geo_zoo01)
    
    anim_zoo02 = QPropertyAnimation(ui.szoo_pushButon_02, b'geometry')
    anim_zoo02.setDuration(500)
    anim_zoo02.setEasingCurve(QEasingCurve.InOutCirc)
    anim_zoo02.setStartValue(current_geo_zoo02)
    anim_zoo02.setEndValue(target_geo_zoo02)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_03)
    ui.animation_group.addAnimation(anim_04)
    ui.animation_group.addAnimation(anim_06)
    ui.animation_group.addAnimation(anim_combo)
    ui.animation_group.addAnimation(anim_line)
    ui.animation_group.addAnimation(anim_btn03)
    ui.animation_group.addAnimation(anim_btn04)
    ui.animation_group.addAnimation(anim_combo2)
    ui.animation_group.addAnimation(anim_line2)
    ui.animation_group.addAnimation(anim_btn04_2)
    ui.animation_group.addAnimation(anim_btn05)
    ui.animation_group.addAnimation(anim_zoo01)
    ui.animation_group.addAnimation(anim_zoo02)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_03(ui):
    """stock_opti_vars_editer용 그룹 애니메이션"""
    # 위젯들의 현재 지오메트리 저장
    current_geo_05 = ui.ss_textEditttt_05.geometry()
    current_geo_06 = ui.ss_textEditttt_06.geometry()
    current_geo_combo = ui.svc_comboBoxxx_02.geometry()
    current_geo_line = ui.svc_lineEdittt_02.geometry()
    current_geo_btn03 = ui.svc_pushButton_03.geometry()
    current_geo_btn04 = ui.svc_pushButton_04.geometry()
    current_geo_combo2 = ui.sva_comboBoxxx_01.geometry()
    current_geo_line2 = ui.sva_lineEdittt_01.geometry()
    current_geo_btn04_2 = ui.sva_pushButton_04.geometry()
    current_geo_btn05 = ui.sva_pushButton_05.geometry()
    
    # 목표 지오메트리 설정
    target_geo_05 = QRect(7, 10, 497, 1347 if ui.extend_window else 740)
    target_geo_06 = QRect(509, 10, 497, 1347 if ui.extend_window else 740)
    target_geo_combo = QRect(1012, 10, 165, 30)
    target_geo_line = QRect(1182, 10, 165, 30)
    target_geo_btn03 = QRect(1012, 45, 165, 30)
    target_geo_btn04 = QRect(1182, 45, 165, 30)
    target_geo_combo2 = QRect(1012, 80, 165, 30)
    target_geo_line2 = QRect(1182, 80, 165, 30)
    target_geo_btn04_2 = QRect(1012, 115, 165, 30)
    target_geo_btn05 = QRect(1182, 115, 165, 30)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 지오메트리 애니메이션 생성
    anim_05 = QPropertyAnimation(ui.ss_textEditttt_05, b'geometry')
    anim_05.setDuration(500)
    anim_05.setEasingCurve(QEasingCurve.InOutCirc)
    anim_05.setStartValue(current_geo_05)
    anim_05.setEndValue(target_geo_05)
    
    anim_06 = QPropertyAnimation(ui.ss_textEditttt_06, b'geometry')
    anim_06.setDuration(500)
    anim_06.setEasingCurve(QEasingCurve.InOutCirc)
    anim_06.setStartValue(current_geo_06)
    anim_06.setEndValue(target_geo_06)
    
    anim_combo = QPropertyAnimation(ui.svc_comboBoxxx_02, b'geometry')
    anim_combo.setDuration(500)
    anim_combo.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo.setStartValue(current_geo_combo)
    anim_combo.setEndValue(target_geo_combo)
    
    anim_line = QPropertyAnimation(ui.svc_lineEdittt_02, b'geometry')
    anim_line.setDuration(500)
    anim_line.setEasingCurve(QEasingCurve.InOutCirc)
    anim_line.setStartValue(current_geo_line)
    anim_line.setEndValue(target_geo_line)
    
    anim_btn03 = QPropertyAnimation(ui.svc_pushButton_03, b'geometry')
    anim_btn03.setDuration(500)
    anim_btn03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn03.setStartValue(current_geo_btn03)
    anim_btn03.setEndValue(target_geo_btn03)
    
    anim_btn04 = QPropertyAnimation(ui.svc_pushButton_04, b'geometry')
    anim_btn04.setDuration(500)
    anim_btn04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn04.setStartValue(current_geo_btn04)
    anim_btn04.setEndValue(target_geo_btn04)
    
    anim_combo2 = QPropertyAnimation(ui.sva_comboBoxxx_01, b'geometry')
    anim_combo2.setDuration(500)
    anim_combo2.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo2.setStartValue(current_geo_combo2)
    anim_combo2.setEndValue(target_geo_combo2)
    
    anim_line2 = QPropertyAnimation(ui.sva_lineEdittt_01, b'geometry')
    anim_line2.setDuration(500)
    anim_line2.setEasingCurve(QEasingCurve.InOutCirc)
    anim_line2.setStartValue(current_geo_line2)
    anim_line2.setEndValue(target_geo_line2)
    
    anim_btn04_2 = QPropertyAnimation(ui.sva_pushButton_04, b'geometry')
    anim_btn04_2.setDuration(500)
    anim_btn04_2.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn04_2.setStartValue(current_geo_btn04_2)
    anim_btn04_2.setEndValue(target_geo_btn04_2)
    
    anim_btn05 = QPropertyAnimation(ui.sva_pushButton_05, b'geometry')
    anim_btn05.setDuration(500)
    anim_btn05.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn05.setStartValue(current_geo_btn05)
    anim_btn05.setEndValue(target_geo_btn05)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_05)
    ui.animation_group.addAnimation(anim_06)
    ui.animation_group.addAnimation(anim_combo)
    ui.animation_group.addAnimation(anim_line)
    ui.animation_group.addAnimation(anim_btn03)
    ui.animation_group.addAnimation(anim_btn04)
    ui.animation_group.addAnimation(anim_combo2)
    ui.animation_group.addAnimation(anim_line2)
    ui.animation_group.addAnimation(anim_btn04_2)
    ui.animation_group.addAnimation(anim_btn05)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_04(ui):
    """stock_vars_editer용 그룹 애니메이션"""
    # 위젯들의 현재 위치와 크기 저장
    current_pos_01 = ui.ss_textEditttt_01.pos()
    current_size_01 = ui.ss_textEditttt_01.size()
    current_pos_02 = ui.ss_textEditttt_02.pos()
    current_size_02 = ui.ss_textEditttt_02.size()
    current_pos_03 = ui.ss_textEditttt_03.pos()
    current_size_03 = ui.ss_textEditttt_03.size()
    current_pos_04 = ui.ss_textEditttt_04.pos()
    current_size_04 = ui.ss_textEditttt_04.size()
    current_pos_combo_jb = ui.svjb_comboBoxx_01.pos()
    current_pos_btn_jb = ui.svjb_pushButon_01.pos()
    current_pos_combo_js = ui.svjs_comboBoxx_01.pos()
    current_pos_btn_js = ui.svjs_pushButon_01.pos()
    current_pos_combo = ui.svc_comboBoxxx_02.pos()
    current_pos_line = ui.svc_lineEdittt_02.pos()
    current_pos_btn03 = ui.svc_pushButton_03.pos()
    current_pos_btn04 = ui.svc_pushButton_04.pos()
    
    # 목표 위치와 크기 설정
    target_pos_01 = QPoint(7, 10)
    target_size_01 = QSize(497, 740 if ui.extend_window else 463)
    target_pos_02 = QPoint(7, 756 if ui.extend_window else 478)
    target_size_02 = QSize(497, 602 if ui.extend_window else 272)
    target_pos_03 = QPoint(509, 10)
    target_size_03 = QSize(497, 740 if ui.extend_window else 463)
    target_pos_04 = QPoint(509, 756 if ui.extend_window else 478)
    target_size_04 = QSize(497, 602 if ui.extend_window else 272)
    target_pos_combo_jb = QPoint(1012, 10)
    target_pos_btn_jb = QPoint(1182, 10)
    target_pos_combo_js = QPoint(1012, 478)
    target_pos_btn_js = QPoint(1182, 478)
    target_pos_combo = QPoint(1012, 115)
    target_pos_line = QPoint(1182, 115)
    target_pos_btn03 = QPoint(1012, 150)
    target_pos_btn04 = QPoint(1182, 150)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 위치 애니메이션 생성
    anim_01 = QPropertyAnimation(ui.ss_textEditttt_01, b'pos')
    anim_01.setDuration(500)
    anim_01.setEasingCurve(QEasingCurve.InOutCirc)
    anim_01.setStartValue(current_pos_01)
    anim_01.setEndValue(target_pos_01)
    
    anim_02 = QPropertyAnimation(ui.ss_textEditttt_02, b'pos')
    anim_02.setDuration(500)
    anim_02.setEasingCurve(QEasingCurve.InOutCirc)
    anim_02.setStartValue(current_pos_02)
    anim_02.setEndValue(target_pos_02)
    
    anim_03 = QPropertyAnimation(ui.ss_textEditttt_03, b'pos')
    anim_03.setDuration(500)
    anim_03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_03.setStartValue(current_pos_03)
    anim_03.setEndValue(target_pos_03)
    
    anim_04 = QPropertyAnimation(ui.ss_textEditttt_04, b'pos')
    anim_04.setDuration(500)
    anim_04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_04.setStartValue(current_pos_04)
    anim_04.setEndValue(target_pos_04)
    
    anim_combo_jb = QPropertyAnimation(ui.svjb_comboBoxx_01, b'pos')
    anim_combo_jb.setDuration(500)
    anim_combo_jb.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo_jb.setStartValue(current_pos_combo_jb)
    anim_combo_jb.setEndValue(target_pos_combo_jb)
    
    anim_btn_jb = QPropertyAnimation(ui.svjb_pushButon_01, b'pos')
    anim_btn_jb.setDuration(500)
    anim_btn_jb.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn_jb.setStartValue(current_pos_btn_jb)
    anim_btn_jb.setEndValue(target_pos_btn_jb)
    
    anim_combo_js = QPropertyAnimation(ui.svjs_comboBoxx_01, b'pos')
    anim_combo_js.setDuration(500)
    anim_combo_js.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo_js.setStartValue(current_pos_combo_js)
    anim_combo_js.setEndValue(target_pos_combo_js)
    
    anim_btn_js = QPropertyAnimation(ui.svjs_pushButon_01, b'pos')
    anim_btn_js.setDuration(500)
    anim_btn_js.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn_js.setStartValue(current_pos_btn_js)
    anim_btn_js.setEndValue(target_pos_btn_js)
    
    anim_combo = QPropertyAnimation(ui.svc_comboBoxxx_02, b'pos')
    anim_combo.setDuration(500)
    anim_combo.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo.setStartValue(current_pos_combo)
    anim_combo.setEndValue(target_pos_combo)
    
    anim_line = QPropertyAnimation(ui.svc_lineEdittt_02, b'pos')
    anim_line.setDuration(500)
    anim_line.setEasingCurve(QEasingCurve.InOutCirc)
    anim_line.setStartValue(current_pos_line)
    anim_line.setEndValue(target_pos_line)
    
    anim_btn03 = QPropertyAnimation(ui.svc_pushButton_03, b'pos')
    anim_btn03.setDuration(500)
    anim_btn03.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn03.setStartValue(current_pos_btn03)
    anim_btn03.setEndValue(target_pos_btn03)
    
    anim_btn04 = QPropertyAnimation(ui.svc_pushButton_04, b'pos')
    anim_btn04.setDuration(500)
    anim_btn04.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn04.setStartValue(current_pos_btn04)
    anim_btn04.setEndValue(target_pos_btn04)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_01)
    ui.animation_group.addAnimation(anim_02)
    ui.animation_group.addAnimation(anim_03)
    ui.animation_group.addAnimation(anim_04)
    ui.animation_group.addAnimation(anim_combo_jb)
    ui.animation_group.addAnimation(anim_btn_jb)
    ui.animation_group.addAnimation(anim_combo_js)
    ui.animation_group.addAnimation(anim_btn_js)
    ui.animation_group.addAnimation(anim_combo)
    ui.animation_group.addAnimation(anim_line)
    ui.animation_group.addAnimation(anim_btn03)
    ui.animation_group.addAnimation(anim_btn04)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_05(ui):
    """stock_backtest_log용 그룹 애니메이션"""
    # 위젯들의 현재 위치와 크기 저장
    current_pos_09 = ui.ss_textEditttt_09.pos()
    current_size_09 = ui.ss_textEditttt_09.size()
    current_pos_progress = ui.ss_progressBar_01.pos()
    current_pos_btn = ui.ss_pushButtonn_08.pos()
    
    # 목표 위치와 크기 설정
    target_pos_09 = QPoint(7, 10)
    target_size_09 = QSize(1000, 1313 if ui.extend_window else 703)
    target_pos_progress = QPoint(7, 1328 if ui.extend_window else 718)
    target_pos_btn = QPoint(842, 1328 if ui.extend_window else 718)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 위치 애니메이션 생성
    anim_09 = QPropertyAnimation(ui.ss_textEditttt_09, b'pos')
    anim_09.setDuration(500)
    anim_09.setEasingCurve(QEasingCurve.InOutCirc)
    anim_09.setStartValue(current_pos_09)
    anim_09.setEndValue(target_pos_09)
    
    anim_progress = QPropertyAnimation(ui.ss_progressBar_01, b'pos')
    anim_progress.setDuration(500)
    anim_progress.setEasingCurve(QEasingCurve.InOutCirc)
    anim_progress.setStartValue(current_pos_progress)
    anim_progress.setEndValue(target_pos_progress)
    
    anim_btn = QPropertyAnimation(ui.ss_pushButtonn_08, b'pos')
    anim_btn.setDuration(500)
    anim_btn.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn.setStartValue(current_pos_btn)
    anim_btn.setEndValue(target_pos_btn)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_09)
    ui.animation_group.addAnimation(anim_progress)
    ui.animation_group.addAnimation(anim_btn)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_06(ui):
    """stock_backtest_detail용 그룹 애니메이션"""
    # 위젯들의 현재 위치와 크기 저장
    current_pos_table = ui.ss_tableWidget_01.pos()
    current_size_table = ui.ss_tableWidget_01.size()
    
    # 목표 위치와 크기 설정
    target_pos_table = QPoint(7, 40)
    target_size_table = QSize(1000, 1318 if ui.extend_window else 713)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 테이블 위젯 위치 애니메이션 생성
    anim_table = QPropertyAnimation(ui.ss_tableWidget_01, b'pos')
    anim_table.setDuration(500)
    anim_table.setEasingCurve(QEasingCurve.InOutCirc)
    anim_table.setStartValue(current_pos_table)
    anim_table.setEndValue(target_pos_table)
    
    # 그룹에 애니메이션 추가
    ui.animation_group.addAnimation(anim_table)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_07(ui):
    """stock_stg_editer용 그룹 애니메이션"""
    # 위젯들의 현재 위치와 크기 저장
    current_pos_01 = ui.ss_textEditttt_01.pos()
    current_size_01 = ui.ss_textEditttt_01.size()
    current_pos_02 = ui.ss_textEditttt_02.pos()
    current_size_02 = ui.ss_textEditttt_02.size()
    current_pos_combo_jb = ui.svjb_comboBoxx_01.pos()
    current_pos_btn_jb = ui.svjb_pushButon_01.pos()
    current_pos_combo_js = ui.svjs_comboBoxx_01.pos()
    current_pos_btn_js = ui.svjs_pushButon_01.pos()
    current_pos_zoo01 = ui.szoo_pushButon_01.pos()
    current_pos_zoo02 = ui.szoo_pushButon_02.pos()
    
    # 목표 위치와 크기 설정
    target_pos_01 = QPoint(7, 10)
    target_size_01 = QSize(1000, 740 if ui.extend_window else 463)
    target_pos_02 = QPoint(7, 756 if ui.extend_window else 478)
    target_size_02 = QSize(1000, 602 if ui.extend_window else 272)
    target_pos_combo_jb = QPoint(1012, 10)
    target_pos_btn_jb = QPoint(1012, 40)
    target_pos_combo_js = QPoint(1012, 478)
    target_pos_btn_js = QPoint(1012, 508)
    target_pos_zoo01 = QPoint(937, 15)
    target_pos_zoo02 = QPoint(937, 761 if ui.extend_window else 483)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 위치 애니메이션 생성
    anim_01 = QPropertyAnimation(ui.ss_textEditttt_01, b'pos')
    anim_01.setDuration(500)
    anim_01.setEasingCurve(QEasingCurve.InOutCirc)
    anim_01.setStartValue(current_pos_01)
    anim_01.setEndValue(target_pos_01)
    
    anim_02 = QPropertyAnimation(ui.ss_textEditttt_02, b'pos')
    anim_02.setDuration(500)
    anim_02.setEasingCurve(QEasingCurve.InOutCirc)
    anim_02.setStartValue(current_pos_02)
    anim_02.setEndValue(target_pos_02)
    
    anim_combo_jb = QPropertyAnimation(ui.svjb_comboBoxx_01, b'pos')
    anim_combo_jb.setDuration(500)
    anim_combo_jb.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo_jb.setStartValue(current_pos_combo_jb)
    anim_combo_jb.setEndValue(target_pos_combo_jb)
    
    anim_btn_jb = QPropertyAnimation(ui.svjb_pushButon_01, b'pos')
    anim_btn_jb.setDuration(500)
    anim_btn_jb.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn_jb.setStartValue(current_pos_btn_jb)
    anim_btn_jb.setEndValue(target_pos_btn_jb)
    
    anim_combo_js = QPropertyAnimation(ui.svjs_comboBoxx_01, b'pos')
    anim_combo_js.setDuration(500)
    anim_combo_js.setEasingCurve(QEasingCurve.InOutCirc)
    anim_combo_js.setStartValue(current_pos_combo_js)
    anim_combo_js.setEndValue(target_pos_combo_js)
    
    anim_btn_js = QPropertyAnimation(ui.svjs_pushButon_01, b'pos')
    anim_btn_js.setDuration(500)
    anim_btn_js.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn_js.setStartValue(current_pos_btn_js)
    anim_btn_js.setEndValue(target_pos_btn_js)
    
    anim_zoo01 = QPropertyAnimation(ui.szoo_pushButon_01, b'pos')
    anim_zoo01.setDuration(500)
    anim_zoo01.setEasingCurve(QEasingCurve.InOutCirc)
    anim_zoo01.setStartValue(current_pos_zoo01)
    anim_zoo01.setEndValue(target_pos_zoo01)
    
    anim_zoo02 = QPropertyAnimation(ui.szoo_pushButon_02, b'pos')
    anim_zoo02.setDuration(500)
    anim_zoo02.setEasingCurve(QEasingCurve.InOutCirc)
    anim_zoo02.setStartValue(current_pos_zoo02)
    anim_zoo02.setEndValue(target_pos_zoo02)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_01)
    ui.animation_group.addAnimation(anim_02)
    ui.animation_group.addAnimation(anim_combo_jb)
    ui.animation_group.addAnimation(anim_btn_jb)
    ui.animation_group.addAnimation(anim_combo_js)
    ui.animation_group.addAnimation(anim_btn_js)
    ui.animation_group.addAnimation(anim_zoo01)
    ui.animation_group.addAnimation(anim_zoo02)
    
    # 애니메이션 시작
    ui.animation_group.start()


def group_animation_08(ui):
    """stock_cond_editer용 그룹 애니메이션"""
    # 위젯들의 현재 지오메트리 저장
    current_geo_07 = ui.ss_textEditttt_07.geometry()
    current_geo_08 = ui.ss_textEditttt_08.geometry()
    
    # 목표 지오메트리 설정
    target_geo_07 = QRect(7, 10, 497, 1347 if ui.extend_window else 740)
    target_geo_08 = QRect(509, 10, 497, 1347 if ui.extend_window else 740)
    
    # 애니메이션 그룹 생성
    ui.animation_group = QParallelAnimationGroup()
    
    # 각 위젯의 지오메트리 애니메이션 생성
    anim_07 = QPropertyAnimation(ui.ss_textEditttt_07, b'geometry')
    anim_07.setDuration(500)
    anim_07.setEasingCurve(QEasingCurve.InOutCirc)
    anim_07.setStartValue(current_geo_07)
    anim_07.setEndValue(target_geo_07)
    
    anim_08 = QPropertyAnimation(ui.ss_textEditttt_08, b'geometry')
    anim_08.setDuration(500)
    anim_08.setEasingCurve(QEasingCurve.InOutCirc)
    anim_08.setStartValue(current_geo_08)
    anim_08.setEndValue(target_geo_08)
    
    # 그룹에 모든 애니메이션 추가
    ui.animation_group.addAnimation(anim_07)
    ui.animation_group.addAnimation(anim_08)
    
    # 애니메이션 시작
    ui.animation_group.start()


@error_decorator
def stock_opti_test_editer(ui):
    group_animation_01(ui)
    # ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    # ui.ss_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
    #
    # ui.svc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    # ui.svc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    # ui.svc_pushButton_03.setGeometry(1012, 150, 165, 30)
    # ui.svc_pushButton_04.setGeometry(1182, 150, 165, 30)
    #
    # ui.szoo_pushButon_01.setGeometry(584, 15, 50, 20)
    # ui.szoo_pushButon_02.setGeometry(584, 761 if ui.extend_window else 483, 50, 20)

    ui.szoo_pushButon_01.setText('확대(esc)')
    ui.szoo_pushButon_02.setText('확대(esc)')

    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(True)
    ui.ss_textEditttt_04.setVisible(True)
    ui.ss_textEditttt_05.setVisible(True)
    ui.ss_textEditttt_06.setVisible(False)

    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_gaopti_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_esczom_list:
        item.setVisible(True)
    for item in ui.stock_optimz_list:
        item.setVisible(True)
    for item in ui.stock_period_list:
        item.setVisible(True)
    for item in ui.stock_optest_list:
        item.setVisible(True)

    ui.svc_pushButton_03.setText('최적화 변수범위 로딩(F9)')
    ui.svc_pushButton_04.setText('최적화 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.svc_labellllll_04.setText(testtext)
    ui.svc_labellllll_05.setVisible(False)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_07.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_rwf_test_editer(ui):
    group_animation_01(ui)
    # ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    # ui.ss_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
    #
    # ui.svc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    # ui.svc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    # ui.svc_pushButton_03.setGeometry(1012, 150, 165, 30)
    # ui.svc_pushButton_04.setGeometry(1182, 150, 165, 30)
    #
    # ui.szoo_pushButon_01.setGeometry(584, 15, 50, 20)
    # ui.szoo_pushButon_02.setGeometry(584, 761 if ui.extend_window else 483, 50, 20)

    ui.szoo_pushButon_01.setText('확대(esc)')
    ui.szoo_pushButon_02.setText('확대(esc)')

    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(True)
    ui.ss_textEditttt_04.setVisible(True)
    ui.ss_textEditttt_05.setVisible(True)
    ui.ss_textEditttt_06.setVisible(False)

    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_gaopti_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_esczom_list:
        item.setVisible(True)
    for item in ui.stock_optimz_list:
        item.setVisible(True)
    for item in ui.stock_period_list:
        item.setVisible(True)
    for item in ui.stock_rwftvd_list:
        item.setVisible(True)

    ui.svc_pushButton_03.setText('최적화 변수범위 로딩(F9)')
    ui.svc_pushButton_04.setText('최적화 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.svc_labellllll_01.setVisible(False)
    ui.svc_labellllll_04.setText(rwfttext)
    ui.svc_labellllll_05.setVisible(False)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_06.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_opti_ga_editer(ui):
    group_animation_02(ui)
    # ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    # ui.ss_textEditttt_06.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
    #
    # ui.svc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    # ui.svc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    # ui.svc_pushButton_03.setGeometry(1012, 150, 165, 30)
    # ui.svc_pushButton_04.setGeometry(1182, 150, 165, 30)
    #
    # ui.sva_comboBoxxx_01.setGeometry(1012, 115, 165, 30)
    # ui.sva_lineEdittt_01.setGeometry(1182, 115, 165, 30)
    # ui.sva_pushButton_04.setGeometry(1012, 150, 165, 30)
    # ui.sva_pushButton_05.setGeometry(1182, 150, 165, 30)
    #
    # ui.szoo_pushButon_01.setGeometry(584, 15, 50, 20)
    # ui.szoo_pushButon_02.setGeometry(584, 761 if ui.extend_window else 483, 50, 20)

    ui.szoo_pushButon_01.setText('확대(esc)')
    ui.szoo_pushButon_02.setText('확대(esc)')

    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(True)
    ui.ss_textEditttt_04.setVisible(True)
    ui.ss_textEditttt_05.setVisible(False)
    ui.ss_textEditttt_06.setVisible(True)

    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_esczom_list:
        item.setVisible(True)
    for item in ui.stock_optimz_list:
        item.setVisible(True)
    for item in ui.stock_period_list:
        item.setVisible(True)
    for item in ui.stock_gaopti_list:
        item.setVisible(True)

    ui.sva_pushButton_04.setText('GA 변수범위 로딩(F9)')
    ui.sva_pushButton_05.setText('GA 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.svc_labellllll_04.setText(gaoptext)
    ui.svc_labellllll_05.setVisible(False)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_10.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_opti_vars_editer(ui):
    group_animation_03(ui)
    # ui.ss_textEditttt_05.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
    # ui.ss_textEditttt_06.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)
    #
    # ui.svc_comboBoxxx_02.setGeometry(1012, 10, 165, 30)
    # ui.svc_lineEdittt_02.setGeometry(1182, 10, 165, 30)
    # ui.svc_pushButton_03.setGeometry(1012, 45, 165, 30)
    # ui.svc_pushButton_04.setGeometry(1182, 45, 165, 30)
    #
    # ui.sva_comboBoxxx_01.setGeometry(1012, 80, 165, 30)
    # ui.sva_lineEdittt_01.setGeometry(1182, 80, 165, 30)
    # ui.sva_pushButton_04.setGeometry(1012, 115, 165, 30)
    # ui.sva_pushButton_05.setGeometry(1182, 115, 165, 30)

    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(False)
    ui.ss_textEditttt_04.setVisible(False)
    ui.ss_textEditttt_05.setVisible(True)
    ui.ss_textEditttt_06.setVisible(True)

    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_esczom_list:
        item.setVisible(False)
    for item in ui.stock_optimz_list:
        item.setVisible(False)
    for item in ui.stock_period_list:
        item.setVisible(True)
    for item in ui.stock_gaopti_list:
        item.setVisible(True)

    ui.sva_pushButton_04.setText('GA 변수범위 로딩')
    ui.sva_pushButton_05.setText('GA 변수범위 저장')
    ui.svc_pushButton_03.setText('최적화 변수범위 로딩')
    ui.svc_pushButton_04.setText('최적화 변수범위 저장')

    ui.svc_pushButton_06.setVisible(False)
    ui.svc_pushButton_07.setVisible(False)
    ui.svc_pushButton_08.setVisible(False)
    ui.svc_pushButton_27.setVisible(False)
    ui.svc_pushButton_28.setVisible(False)
    ui.svc_pushButton_29.setVisible(False)

    ui.sva_pushButton_01.setVisible(False)
    ui.sva_pushButton_02.setVisible(False)
    ui.sva_pushButton_03.setVisible(False)

    ui.svc_comboBoxxx_02.setVisible(True)
    ui.svc_lineEdittt_02.setVisible(True)
    ui.svc_pushButton_03.setVisible(True)
    ui.svc_pushButton_04.setVisible(True)

    ui.svc_pushButton_11.setVisible(True)

    ui.image_label1.setVisible(True)
    ui.svc_labellllll_05.setVisible(True)
    ui.svc_labellllll_04.setText(gaoptext)
    ui.svc_labellllll_05.setText(vedittxt)
    ui.svc_pushButton_21.setVisible(True)
    ui.svc_pushButton_22.setVisible(True)
    ui.svc_pushButton_23.setVisible(True)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_12.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_opti_editer(ui):
    group_animation_01(ui)
    # ui.ss_textEditttt_03.setGeometry(7, 10, 647, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_04.setGeometry(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272)
    # ui.ss_textEditttt_05.setGeometry(659, 10, 347, 1347 if ui.extend_window else 740)
    #
    # ui.svc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    # ui.svc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    # ui.svc_pushButton_03.setGeometry(1012, 150, 165, 30)
    # ui.svc_pushButton_04.setGeometry(1182, 150, 165, 30)
    #
    # ui.szoo_pushButon_01.setGeometry(584, 15, 50, 20)
    # ui.szoo_pushButon_02.setGeometry(584, 761 if ui.extend_window else 483, 50, 20)

    ui.szoo_pushButon_01.setText('확대(esc)')
    ui.szoo_pushButon_02.setText('확대(esc)')

    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(True)
    ui.ss_textEditttt_04.setVisible(True)
    ui.ss_textEditttt_05.setVisible(True)
    ui.ss_textEditttt_06.setVisible(False)

    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_gaopti_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_esczom_list:
        item.setVisible(True)
    for item in ui.stock_optimz_list:
        item.setVisible(True)
    for item in ui.stock_period_list:
        item.setVisible(True)

    ui.svc_pushButton_03.setText('최적화 변수범위 로딩(F9)')
    ui.svc_pushButton_04.setText('최적화 변수범위 저장(F12)')

    ui.image_label1.setVisible(False)
    ui.svc_labellllll_04.setText(optitext)
    ui.svc_labellllll_05.setVisible(False)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_08.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_vars_editer(ui):
    group_animation_04(ui)
    # ui.ss_textEditttt_01.setGeometry(7, 10, 497, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 478, 497, 602 if ui.extend_window else 272)
    # ui.ss_textEditttt_03.setGeometry(509, 10, 497, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_04.setGeometry(509, 756 if ui.extend_window else 478, 497, 602 if ui.extend_window else 272)
    #
    # ui.svjb_comboBoxx_01.setGeometry(1012, 10, 165, 30)
    # ui.svjb_pushButon_01.setGeometry(1182, 10, 165, 30)
    # ui.svjs_comboBoxx_01.setGeometry(1012, 478, 165, 30)
    # ui.svjs_pushButon_01.setGeometry(1182, 478, 165, 30)
    #
    # ui.svc_comboBoxxx_02.setGeometry(1012, 115, 165, 30)
    # ui.svc_lineEdittt_02.setGeometry(1182, 115, 165, 30)
    # ui.svc_pushButton_03.setGeometry(1012, 150, 165, 30)
    # ui.svc_pushButton_04.setGeometry(1182, 150, 165, 30)

    ui.ss_textEditttt_01.setVisible(True)
    ui.ss_textEditttt_02.setVisible(True)
    ui.ss_textEditttt_03.setVisible(True)
    ui.ss_textEditttt_04.setVisible(True)
    ui.ss_textEditttt_05.setVisible(False)
    ui.ss_textEditttt_06.setVisible(False)

    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_gaopti_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_esczom_list:
        item.setVisible(False)
    for item in ui.stock_optimz_list:
        item.setVisible(True)
    for item in ui.stock_period_list:
        item.setVisible(True)

    ui.svjb_pushButon_01.setText('매수전략 로딩')
    ui.svjs_pushButon_01.setText('매도전략 로딩')

    ui.svjb_comboBoxx_01.setVisible(True)
    ui.svjb_pushButon_01.setVisible(True)
    ui.svjs_comboBoxx_01.setVisible(True)
    ui.svjs_pushButon_01.setVisible(True)

    ui.svc_lineEdittt_04.setVisible(False)
    ui.svc_pushButton_13.setVisible(False)
    ui.svc_lineEdittt_05.setVisible(False)
    ui.svc_pushButton_14.setVisible(False)

    ui.image_label1.setVisible(False)
    ui.svc_labellllll_04.setText(optitext)
    ui.svc_labellllll_05.setVisible(False)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(True)
    ui.svc_pushButton_25.setVisible(True)
    ui.svc_pushButton_26.setVisible(True)

    ui.svj_pushButton_13.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def change_pre_button_edit(ui):
    if ui.svj_pushButton_01.isVisible():
        ui.svj_pushButton_09.setStyleSheet(style_bc_bd)
    elif ui.svc_pushButton_32.isVisible():
        ui.svj_pushButton_07.setStyleSheet(style_bc_bd)
    elif ui.svc_pushButton_35.isVisible():
        ui.svj_pushButton_06.setStyleSheet(style_bc_bd)
    elif ui.sva_pushButton_03.isVisible():
        ui.svj_pushButton_10.setStyleSheet(style_bc_bd)
    elif ui.svo_pushButton_08.isVisible():
        ui.svj_pushButton_11.setStyleSheet(style_bc_bd)
    elif ui.svc_pushButton_23.isVisible():
        ui.svj_pushButton_12.setStyleSheet(style_bc_bd)
    elif ui.svc_pushButton_26.isVisible():
        ui.svj_pushButton_13.setStyleSheet(style_bc_bd)
    elif ui.svc_pushButton_29.isVisible():
        ui.svj_pushButton_08.setStyleSheet(style_bc_bd)


@error_decorator
def stock_backtest_log(ui):
    group_animation_05(ui)
    change_pre_button_edit(ui)
    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(False)
    ui.ss_textEditttt_04.setVisible(False)
    ui.ss_textEditttt_05.setVisible(False)
    ui.ss_textEditttt_06.setVisible(False)
    ui.ss_textEditttt_07.setVisible(False)
    ui.ss_textEditttt_08.setVisible(False)

    # ui.ss_textEditttt_09.setGeometry(7, 10, 1000, 1313 if ui.extend_window else 703)
    # ui.ss_progressBar_01.setGeometry(7, 1328 if ui.extend_window else 718, 830, 30)
    # ui.ss_pushButtonn_08.setGeometry(842, 1328 if ui.extend_window else 718, 165, 30)

    for item in ui.stock_esczom_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(True)

    ui.ss_pushButtonn_08.setStyleSheet(style_bc_by)
    ui.svj_pushButton_14.setFocus()
    ui.svj_pushButton_14.setStyleSheet(style_bc_dk)
    ui.svj_pushButton_15.setStyleSheet(style_bc_bs)


@error_decorator
def stock_backtest_detail(ui):
    group_animation_06(ui)
    change_pre_button_edit(ui)
    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(False)
    ui.ss_textEditttt_04.setVisible(False)
    ui.ss_textEditttt_05.setVisible(False)
    ui.ss_textEditttt_06.setVisible(False)
    ui.ss_textEditttt_07.setVisible(False)
    ui.ss_textEditttt_08.setVisible(False)

    # ui.ss_tableWidget_01.setGeometry(7, 40, 1000, 1318 if ui.extend_window else 713)
    if (ui.extend_window and ui.ss_tableWidget_01.rowCount() < 60) or \
            (not ui.extend_window and ui.ss_tableWidget_01.rowCount() < 32):
        ui.ss_tableWidget_01.setRowCount(60 if ui.extend_window else 32)

    for item in ui.stock_esczom_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(True)

    ui.svj_pushButton_15.setFocus()
    ui.svj_pushButton_15.setStyleSheet(style_bc_dk)
    ui.svj_pushButton_14.setStyleSheet(style_bc_bs)


@error_decorator
def stock_stg_editer(ui):
    group_animation_07(ui)
    # ui.ss_textEditttt_01.setGeometry(7, 10, 1000, 740 if ui.extend_window else 463)
    # ui.ss_textEditttt_02.setGeometry(7, 756 if ui.extend_window else 478, 1000, 602 if ui.extend_window else 272)
    #
    # ui.svjb_comboBoxx_01.setGeometry(1012, 10, 165, 25)
    # ui.svjb_pushButon_01.setGeometry(1012, 40, 165, 30)
    # ui.svjs_comboBoxx_01.setGeometry(1012, 478, 165, 25)
    # ui.svjs_pushButon_01.setGeometry(1012, 508, 165, 30)
    #
    # ui.szoo_pushButon_01.setGeometry(937, 15, 50, 20)
    # ui.szoo_pushButon_02.setGeometry(937, 761 if ui.extend_window else 483, 50, 20)

    ui.szoo_pushButon_01.setText('확대(esc)')
    ui.szoo_pushButon_02.setText('확대(esc)')

    ui.ss_textEditttt_01.setVisible(True)
    ui.ss_textEditttt_02.setVisible(True)
    ui.ss_textEditttt_03.setVisible(False)
    ui.ss_textEditttt_04.setVisible(False)
    ui.ss_textEditttt_05.setVisible(False)
    ui.ss_textEditttt_06.setVisible(False)

    for item in ui.stock_optimz_list:
        item.setVisible(False)
    for item in ui.stock_period_list:
        item.setVisible(False)
    for item in ui.stock_opcond_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_gaopti_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_datedt_list:
        item.setVisible(True)
    for item in ui.stock_esczom_list:
        item.setVisible(True)
    for item in ui.stock_backte_list:
        item.setVisible(True)

    ui.svjb_pushButon_01.setText('매수전략 로딩(F1)')
    ui.svjs_pushButon_01.setText('매도전략 로딩(F5)')

    ui.image_label1.setVisible(False)
    ui.svc_labellllll_05.setVisible(False)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_09.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_cond_editer(ui):
    group_animation_08(ui)
    # ui.ss_textEditttt_07.setGeometry(7, 10, 497, 1347 if ui.extend_window else 740)
    # ui.ss_textEditttt_08.setGeometry(509, 10, 497, 1347 if ui.extend_window else 740)

    ui.ss_textEditttt_01.setVisible(False)
    ui.ss_textEditttt_02.setVisible(False)
    ui.ss_textEditttt_03.setVisible(False)
    ui.ss_textEditttt_04.setVisible(False)
    ui.ss_textEditttt_05.setVisible(False)
    ui.ss_textEditttt_06.setVisible(False)

    for item in ui.stock_esczom_list:
        item.setVisible(False)
    for item in ui.stock_backte_list:
        item.setVisible(False)
    for item in ui.stock_detail_list:
        item.setVisible(False)
    for item in ui.stock_baklog_list:
        item.setVisible(False)
    for item in ui.stock_gaopti_list:
        item.setVisible(False)
    for item in ui.stock_optest_list:
        item.setVisible(False)
    for item in ui.stock_rwftvd_list:
        item.setVisible(False)
    for item in ui.stock_datedt_list:
        item.setVisible(False)
    for item in ui.stock_optimz_list:
        item.setVisible(True)
    for item in ui.stock_period_list:
        item.setVisible(True)
    for item in ui.stock_opcond_list:
        item.setVisible(True)

    ui.svc_lineEdittt_04.setVisible(False)
    ui.svc_lineEdittt_05.setVisible(False)
    ui.svc_pushButton_13.setVisible(False)
    ui.svc_pushButton_14.setVisible(False)

    ui.svc_comboBoxxx_08.setVisible(False)
    ui.svc_lineEdittt_03.setVisible(False)
    ui.svc_pushButton_09.setVisible(False)
    ui.svc_pushButton_10.setVisible(False)

    ui.svc_comboBoxxx_02.setVisible(False)
    ui.svc_lineEdittt_02.setVisible(False)
    ui.svc_pushButton_03.setVisible(False)
    ui.svc_pushButton_04.setVisible(False)

    ui.image_label1.setVisible(True)
    ui.svc_labellllll_01.setVisible(False)
    ui.svc_labellllll_04.setVisible(True)
    ui.svc_labellllll_05.setVisible(True)
    ui.svc_labellllll_04.setText(condtext)
    ui.svc_labellllll_05.setText(cedittxt)
    ui.svc_pushButton_21.setVisible(False)
    ui.svc_pushButton_22.setVisible(False)
    ui.svc_pushButton_23.setVisible(False)
    ui.svc_pushButton_24.setVisible(False)
    ui.svc_pushButton_25.setVisible(False)
    ui.svc_pushButton_26.setVisible(False)

    ui.svj_pushButton_11.setFocus()
    sChangeSvjButtonColor(ui)


@error_decorator
def stock_backtest_start(ui):
    if ui.BacktestProcessAlive():
        QMessageBox.critical(ui, '오류 알림', '현재 백테스트가 실행중입니다.\n중복 실행할 수 없습니다.\n')
    else:
        if ui.back_engining:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 구동 중...\n')
            return
        if ui.dialog_backengine.isVisible() and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진이 구동되지 않았습니다.\n')
            return
        back_club = True if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (
                    QApplication.keyboardModifiers() & Qt.AltModifier) else False
        if back_club and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진을 먼저 구동하십시오.\n')
            return
        if not back_club and (not ui.backtest_engine or (QApplication.keyboardModifiers() & Qt.ControlModifier)):
            ui.BackTestengineShow('주식')
            return
        if ui.back_cancelling:
            QMessageBox.critical(ui, '오류 알림', '이전 백테스트를 중지하고 있습니다.\n잠시 후 다시 시도하십시오.\n')
            return

        startday = ui.svjb_dateEditt_01.date().toString('yyyyMMdd')
        endday = ui.svjb_dateEditt_02.date().toString('yyyyMMdd')
        starttime = ui.svjb_lineEditt_02.text()
        endtime = ui.svjb_lineEditt_03.text()
        betting = ui.svjb_lineEditt_04.text()
        avgtime = ui.svjb_lineEditt_05.text()
        buystg = ui.svjb_comboBoxx_01.currentText()
        sellstg = ui.svjs_comboBoxx_01.currentText()
        bl = True if ui.dict_set['블랙리스트추가'] else False

        if int(avgtime) not in ui.avg_list:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 시작 시 포함되지 않은 평균값틱수를 사용하였습니다.\n현재의 틱수로 백테스팅하려면 백테엔진을 다시 시작하십시오.\n')
            return
        if '' in (startday, endday, starttime, endtime, betting, avgtime):
            QMessageBox.critical(ui, '오류 알림', '일부 설정값이 공백 상태입니다.\n')
            return
        if '' in (buystg, sellstg):
            QMessageBox.critical(ui, '오류 알림', '전략을 저장하고 콤보박스에서 선택하십시오.\n')
            return

        ui.ClearBacktestQ()
        for q in ui.back_eques:
            q.put(('백테유형', '백테스트'))

        ui.backQ.put((
            betting, avgtime, startday, endday, starttime, endtime, buystg, sellstg, ui.dict_cn, ui.back_count,
            bl, False, back_club
        ))

        gubun = 'S' if '키움증권' in ui.dict_set['증권사'] else 'SF'
        ui.proc_backtester_bs = Process(
            target=BackTest,
            args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                  ui.back_sques, '백테스트', gubun, ui.dict_set)
        )
        ui.proc_backtester_bs.start()
        ui.StockBacktestLog()
        ui.ss_progressBar_01.setValue(0)
        ui.ssicon_alert = True


@error_decorator
def stock_backfinder_start(ui):
    if ui.BacktestProcessAlive():
        QMessageBox.critical(ui, '오류 알림', '현재 백테스트가 실행중입니다.\n중복 실행할 수 없습니다.\n')
    else:
        if ui.back_engining:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 구동 중...\n')
            return
        if ui.dialog_backengine.isVisible() and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진이 구동되지 않았습니다.\n')
            return
        if not ui.backtest_engine or (QApplication.keyboardModifiers() & Qt.ControlModifier):
            ui.BackTestengineShow('주식')
            return
        if ui.back_cancelling:
            QMessageBox.critical(ui, '오류 알림', '이전 백테스트를 중지하고 있습니다.\n잠시 후 다시 시도하십시오.\n')
            return

        startday = ui.svjb_dateEditt_01.date().toString('yyyyMMdd')
        endday = ui.svjb_dateEditt_02.date().toString('yyyyMMdd')
        starttime = ui.svjb_lineEditt_02.text()
        endtime = ui.svjb_lineEditt_03.text()
        avgtime = ui.svjb_lineEditt_05.text()
        buystg = ui.svjb_comboBoxx_01.currentText()

        if int(avgtime) not in ui.avg_list:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 시작 시 포함되지 않은 평균값틱수를 사용하였습니다.\n현재의 틱수로 백테스팅하려면 백테엔진을 다시 시작하십시오.\n')
            return
        if '' in (startday, endday, starttime, endtime, avgtime):
            QMessageBox.critical(ui, '오류 알림', '일부 설정값이 공백 상태입니다.\n')
            return
        if buystg == '':
            QMessageBox.critical(ui, '오류 알림', '매수전략을 저장하고 콤보박스에서 선택하십시오.\n')
            return
        if 'self.tickcols' not in ui.ss_textEditttt_01.toPlainText():
            QMessageBox.critical(ui, '오류 알림', '현재 매수전략이 백파인더용이 아닙니다.\n')
            return

        ui.ClearBacktestQ()
        for q in ui.back_eques:
            q.put(('백테유형', '백파인더'))

        ui.backQ.put((avgtime, startday, endday, starttime, endtime, buystg, ui.back_count))
        gubun = 'S' if '키움증권' in ui.dict_set['증권사'] else 'SF'
        ui.proc_backtester_bf = Process(
            target=BackFinder,
            args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, gubun, ui.dict_set)
        )
        ui.proc_backtester_bf.start()
        ui.StockBacktestLog()
        ui.ss_progressBar_01.setValue(0)
        ui.ssicon_alert = True


@error_decorator
def stock_backfinder_sample(ui):
    if ui.ss_textEditttt_01.isVisible():
        ui.ss_textEditttt_01.clear()
        ui.ss_textEditttt_02.clear()
        ui.ss_textEditttt_01.append(example_finder)


@error_decorator
def stock_opti_start(ui, back_name):
    if ui.BacktestProcessAlive():
        QMessageBox.critical(ui, '오류 알림', '현재 백테스트가 실행중입니다.\n중복 실행할 수 없습니다.\n')
    else:
        if ui.back_engining:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 구동 중...\n')
            return
        if ui.dialog_backengine.isVisible() and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진이 구동되지 않았습니다.\n')
            return
        if not ui.backtest_engine or (not (QApplication.keyboardModifiers() & Qt.ShiftModifier) and
                                      not (QApplication.keyboardModifiers() & Qt.AltModifier) and
                                      (QApplication.keyboardModifiers() & Qt.ControlModifier)):
            ui.BackTestengineShow('주식')
            return
        if ui.back_cancelling:
            QMessageBox.critical(ui, '오류 알림', '이전 백테스트를 중지하고 있습니다.\n잠시 후 다시 시도하십시오.\n')
            return

        randomopti = True if not (QApplication.keyboardModifiers() & Qt.ControlModifier) and (
                    QApplication.keyboardModifiers() & Qt.AltModifier) else False
        onlybuy = True if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (
                    QApplication.keyboardModifiers() & Qt.ShiftModifier) else False
        onlysell = True if (QApplication.keyboardModifiers() & Qt.ControlModifier) and (
                    QApplication.keyboardModifiers() & Qt.AltModifier) else False
        starttime   = ui.svjb_lineEditt_02.text()
        endtime     = ui.svjb_lineEditt_03.text()
        betting     = ui.svjb_lineEditt_04.text()
        buystg      = ui.svc_comboBoxxx_01.currentText()
        sellstg     = ui.svc_comboBoxxx_08.currentText()
        optivars    = ui.svc_comboBoxxx_02.currentText()
        ccount      = ui.svc_comboBoxxx_06.currentText()
        optistd     = ui.svc_comboBoxxx_07.currentText()
        weeks_train = ui.svc_comboBoxxx_03.currentText()
        weeks_valid = ui.svc_comboBoxxx_04.currentText()
        weeks_test  = ui.svc_comboBoxxx_05.currentText()
        benginesday = ui.be_dateEdittttt_01.date().toString('yyyyMMdd')
        bengineeday = ui.be_dateEdittttt_02.date().toString('yyyyMMdd')
        optunasampl = ui.op_comboBoxxxx_01.currentText()
        optunafixv  = ui.op_lineEditttt_01.text()
        optunacount = ui.op_lineEditttt_02.text()
        optunaautos = 1 if ui.op_checkBoxxxx_01.isChecked() else 0

        if 'VC' in back_name and weeks_train != 'ALL' and int(weeks_train) % int(weeks_valid) != 0:
            QMessageBox.critical(ui, '오류 알림', '교차검증의 학습기간은 검증기간의 배수로 선택하십시오.\n')
            return
        if '' in (starttime, endtime, betting):
            QMessageBox.critical(ui, '오류 알림', '일부 설정값이 공백 상태입니다.\n')
            return
        if '' in (buystg, sellstg):
            QMessageBox.critical(ui, '오류 알림', '전략을 저장하고 콤보박스에서 선택하십시오.\n')
            return
        if optivars == '':
            QMessageBox.critical(ui, '오류 알림', '변수를 설장하고 콤보박스에서 선택하십시오.\n')
            return

        ui.ClearBacktestQ()
        for q in ui.back_eques:
            q.put(('백테유형', '최적화'))

        ui.backQ.put((
            betting, starttime, endtime, buystg, sellstg, optivars, ui.dict_cn, ccount, ui.dict_set['최적화기준값제한'],
            optistd, ui.back_count, False, weeks_train, weeks_valid, weeks_test, benginesday, bengineeday, optunasampl,
            optunafixv, optunacount, optunaautos, randomopti, onlybuy, onlysell
        ))

        gubun = 'S' if '키움증권' in ui.dict_set['증권사'] else 'SF'
        if back_name == '최적화O':
            ui.proc_backtester_o = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_o.start()
        elif back_name == '최적화OV':
            ui.proc_backtester_ov = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ov.start()
        elif back_name == '최적화OVC':
            ui.proc_backtester_ovc = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ovc.start()
        elif back_name == '최적화B':
            ui.proc_backtester_b = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_b.start()
        elif back_name == '최적화BV':
            ui.proc_backtester_bv = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_bv.start()
        elif back_name == '최적화BVC':
            ui.proc_backtester_bvc = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_bvc.start()
        elif back_name == '최적화OT':
            ui.proc_backtester_ot = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ot.start()
        elif back_name == '최적화OVT':
            ui.proc_backtester_ovt = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ovt.start()
        elif back_name == '최적화OVCT':
            ui.proc_backtester_ovct = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ovct.start()
        elif back_name == '최적화BT':
            ui.proc_backtester_bt = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_bt.start()
        elif back_name == '최적화BVT':
            ui.proc_backtester_bvt = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_bvt.start()
        else:
            ui.proc_backtester_bvct = Process(
                target=Optimize,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_bvct.start()
        ui.StockBacktestLog()
        ui.ss_progressBar_01.setValue(0)
        ui.ssicon_alert = True


@error_decorator
def stock_opti_rwft_start(ui, back_name):
    if ui.BacktestProcessAlive():
        QMessageBox.critical(ui, '오류 알림', '현재 백테스트가 실행중입니다.\n중복 실행할 수 없습니다.\n')
    else:
        if ui.back_engining:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 구동 중...\n')
            return
        if ui.dialog_backengine.isVisible() and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진이 구동되지 않았습니다.\n')
            return
        if not ui.backtest_engine or (QApplication.keyboardModifiers() & Qt.ControlModifier):
            ui.BackTestengineShow('주식')
            return
        if ui.back_cancelling:
            QMessageBox.critical(ui, '오류 알림', '이전 백테스트를 중지하고 있습니다.\n잠시 후 다시 시도하십시오.\n')
            return

        randomopti  = True if (QApplication.keyboardModifiers() & Qt.AltModifier) and 'B' not in back_name else False
        startday    = ui.svjb_dateEditt_01.date().toString('yyyyMMdd')
        endday      = ui.svjb_dateEditt_02.date().toString('yyyyMMdd')
        starttime   = ui.svjb_lineEditt_02.text()
        endtime     = ui.svjb_lineEditt_03.text()
        betting     = ui.svjb_lineEditt_04.text()
        buystg      = ui.svc_comboBoxxx_01.currentText()
        sellstg     = ui.svc_comboBoxxx_08.currentText()
        optivars    = ui.svc_comboBoxxx_02.currentText()
        ccount      = ui.svc_comboBoxxx_06.currentText()
        optistd     = ui.svc_comboBoxxx_07.currentText()
        weeks_train = ui.svc_comboBoxxx_03.currentText()
        weeks_valid = ui.svc_comboBoxxx_04.currentText()
        weeks_test  = ui.svc_comboBoxxx_05.currentText()
        benginesday = ui.be_dateEdittttt_01.date().toString('yyyyMMdd')
        bengineeday = ui.be_dateEdittttt_02.date().toString('yyyyMMdd')
        optunasampl = ui.op_comboBoxxxx_01.currentText()
        optunafixv  = ui.op_lineEditttt_01.text()
        optunacount = ui.op_lineEditttt_02.text()
        optunaautos = 1 if ui.op_checkBoxxxx_01.isChecked() else 0

        if 'VC' in back_name and weeks_train != 'ALL' and int(weeks_train) % int(weeks_valid) != 0:
            QMessageBox.critical(ui, '오류 알림', '교차검증의 학습기간은 검증기간의 배수로 선택하십시오.\n')
            return
        if weeks_train == 'ALL':
            QMessageBox.critical(ui, '오류 알림', '전진분석 학습기간은 전체를 선택할 수 없습니다.\n')
            return
        if '' in (starttime, endtime, betting):
            QMessageBox.critical(ui, '오류 알림', '일부 설정값이 공백 상태입니다.\n')
            return
        if '' in (buystg, sellstg):
            QMessageBox.critical(ui, '오류 알림', '전략을 저장하고 콤보박스에서 선택하십시오.\n')
            return
        if optivars == '':
            QMessageBox.critical(ui, '오류 알림', '변수를 설장하고 콤보박스에서 선택하십시오.\n')
            return

        ui.ClearBacktestQ()
        for q in ui.back_eques:
            q.put(('백테유형', '전진분석'))

        ui.backQ.put((
            betting, startday, endday, starttime, endtime, buystg, sellstg, optivars, ui.dict_cn, ccount,
            ui.dict_set['최적화기준값제한'], optistd, ui.back_count, False, weeks_train, weeks_valid, weeks_test,
            benginesday, bengineeday, optunasampl, optunafixv, optunacount, optunaautos, randomopti
        ))

        gubun = 'S' if '키움증권' in ui.dict_set['증권사'] else 'SF'
        if back_name == '전진분석OR':
            ui.proc_backtester_or = Process(
                target=RollingWalkForwardTest,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_or.start()
        elif back_name == '전진분석ORV':
            ui.proc_backtester_orv = Process(
                target=RollingWalkForwardTest,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_orv.start()
        elif back_name == '전진분석ORVC':
            ui.proc_backtester_orvc = Process(
                target=RollingWalkForwardTest,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_orvc.start()
        elif back_name == '전진분석BR':
            ui.proc_backtester_br = Process(
                target=RollingWalkForwardTest,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_br.start()
        elif back_name == '전진분석BRV':
            ui.proc_backtester_brv = Process(
                target=RollingWalkForwardTest,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_brv.start()
        else:
            ui.proc_backtester_brvc = Process(
                target=RollingWalkForwardTest,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.teleQ, ui.back_eques,
                      ui.back_sques, ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_brvc.start()
        ui.StockBacktestLog()
        ui.ss_progressBar_01.setValue(0)
        ui.ssicon_alert = True


@error_decorator
def stock_opti_ga_start(ui, back_name):
    if ui.BacktestProcessAlive():
        QMessageBox.critical(ui, '오류 알림', '현재 백테스트가 실행중입니다.\n중복 실행할 수 없습니다.\n')
    else:
        if ui.back_engining:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 구동 중...\n')
            return
        if ui.dialog_backengine.isVisible() and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진이 구동되지 않았습니다.\n')
            return
        if not ui.backtest_engine or (QApplication.keyboardModifiers() & Qt.ControlModifier):
            ui.BackTestengineShow('주식')
            return
        if ui.back_cancelling:
            QMessageBox.critical(ui, '오류 알림', '이전 백테스트를 중지하고 있습니다.\n잠시 후 다시 시도하십시오.\n')
            return

        starttime   = ui.svjb_lineEditt_02.text()
        endtime     = ui.svjb_lineEditt_03.text()
        betting     = ui.svjb_lineEditt_04.text()
        buystg      = ui.svc_comboBoxxx_01.currentText()
        sellstg     = ui.svc_comboBoxxx_08.currentText()
        optivars    = ui.sva_comboBoxxx_01.currentText()
        optistd     = ui.svc_comboBoxxx_07.currentText()
        weeks_train = ui.svc_comboBoxxx_03.currentText()
        weeks_valid = ui.svc_comboBoxxx_04.currentText()
        weeks_test  = ui.svc_comboBoxxx_05.currentText()
        benginesday = ui.be_dateEdittttt_01.date().toString('yyyyMMdd')
        bengineeday = ui.be_dateEdittttt_02.date().toString('yyyyMMdd')

        if 'VC' in back_name and weeks_train != 'ALL' and int(weeks_train) % int(weeks_valid) != 0:
            QMessageBox.critical(ui, '오류 알림', '교차검증의 학습기간은 검증기간의 배수로 선택하십시오.\n')
            return
        if '' in (starttime, endtime, betting):
            QMessageBox.critical(ui, '오류 알림', '일부 설정값이 공백 상태입니다.\n')
            return
        if '' in (buystg, sellstg):
            QMessageBox.critical(ui, '오류 알림', '전략을 저장하고 콤보박스에서 선택하십시오.\n')
            return
        if optivars == '':
            QMessageBox.critical(ui, '오류 알림', '변수를 설장하고 콤보박스에서 선택하십시오.\n')
            return

        ui.ClearBacktestQ()
        for q in ui.back_eques:
            q.put(('백테유형', 'GA최적화'))

        ui.backQ.put((
            betting, starttime, endtime, buystg, sellstg, optivars, ui.dict_cn, ui.dict_set['최적화기준값제한'],
            optistd, ui.back_count, weeks_train, weeks_valid, weeks_test, benginesday, bengineeday
        ))

        gubun = 'S' if '키움증권' in ui.dict_set['증권사'] else 'SF'
        if back_name == '최적화OG':
            ui.proc_backtester_og = Process(
                target=OptimizeGeneticAlgorithm,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, ui.back_sques,
                      ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_og.start()
        elif back_name == '최적화OGV':
            ui.proc_backtester_ogv = Process(
                target=OptimizeGeneticAlgorithm,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, ui.back_sques,
                      ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ogv.start()
        else:
            ui.proc_backtester_ogvc = Process(
                target=OptimizeGeneticAlgorithm,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, ui.back_sques,
                      ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ogvc.start()
        ui.StockBacktestLog()
        ui.ss_progressBar_01.setValue(0)
        ui.ssicon_alert = True


@error_decorator
def stock_opti_cond_start(ui, back_name):
    if ui.BacktestProcessAlive():
        QMessageBox.critical(ui, '오류 알림', '현재 백테스트가 실행중입니다.\n중복 실행할 수 없습니다.\n')
    else:
        if ui.back_engining:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 구동 중...\n')
            return
        if ui.dialog_backengine.isVisible() and not ui.backtest_engine:
            QMessageBox.critical(ui, '오류 알림', '백테엔진이 구동되지 않았습니다.\n')
            return
        if not ui.backtest_engine or (QApplication.keyboardModifiers() & Qt.ControlModifier):
            ui.BackTestengineShow('주식')
            return
        if ui.back_cancelling:
            QMessageBox.critical(ui, '오류 알림', '이전 백테스트를 중지하고 있습니다.\n잠시 후 다시 시도하십시오.\n')
            return

        starttime   = ui.svjb_lineEditt_02.text()
        endtime     = ui.svjb_lineEditt_03.text()
        betting     = ui.svjb_lineEditt_04.text()
        avgtime     = ui.svjb_lineEditt_05.text()
        buystg      = ui.svo_comboBoxxx_01.currentText()
        sellstg     = ui.svo_comboBoxxx_02.currentText()
        bcount      = ui.svo_lineEdittt_03.text()
        scount      = ui.svo_lineEdittt_04.text()
        rcount      = ui.svo_lineEdittt_05.text()
        optistd     = ui.svc_comboBoxxx_07.currentText()
        weeks_train = ui.svc_comboBoxxx_03.currentText()
        weeks_valid = ui.svc_comboBoxxx_04.currentText()
        weeks_test  = ui.svc_comboBoxxx_05.currentText()
        benginesday = ui.be_dateEdittttt_01.date().toString('yyyyMMdd')
        bengineeday = ui.be_dateEdittttt_02.date().toString('yyyyMMdd')

        if 'VC' in back_name and weeks_train != 'ALL' and int(weeks_train) % int(weeks_valid) != 0:
            QMessageBox.critical(ui, '오류 알림', '교차검증의 학습기간은 검증기간의 배수로 선택하십시오.\n')
            return
        if int(avgtime) not in ui.avg_list:
            QMessageBox.critical(ui, '오류 알림', '백테엔진 시작 시 포함되지 않은 평균값틱수를 사용하였습니다.\n현재의 틱수로 백테스팅하려면 백테엔진을 다시 시작하십시오.\n')
            return
        if '' in (starttime, endtime, betting, avgtime, bcount, scount, rcount):
            QMessageBox.critical(ui, '오류 알림', '일부 설정값이 공백 상태입니다.\n')
            return
        if '' in (buystg, sellstg):
            QMessageBox.critical(ui, '오류 알림', '조건을 저장하고 콤보박스에서 선택하십시오.\n')
            return

        ui.ClearBacktestQ()
        for q in ui.back_eques:
            q.put(('백테유형', '조건최적화'))

        ui.backQ.put((
            betting, avgtime, starttime, endtime, buystg, sellstg, ui.dict_set['최적화기준값제한'], optistd, bcount,
            scount, rcount, ui.back_count, weeks_train, weeks_valid, weeks_test, benginesday, bengineeday
        ))

        gubun = 'S' if '키움증권' in ui.dict_set['증권사'] else 'SF'
        if back_name == '최적화OC':
            ui.proc_backtester_oc = Process(
                target=OptimizeConditions,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, ui.back_sques,
                      ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_oc.start()
        elif back_name == '최적화OCV':
            ui.proc_backtester_ocv = Process(
                target=OptimizeConditions,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, ui.back_sques,
                      ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ocv.start()
        else:
            ui.proc_backtester_ocvc = Process(
                target=OptimizeConditions,
                args=(ui.shared_cnt, ui.windowQ, ui.backQ, ui.soundQ, ui.totalQ, ui.liveQ, ui.back_eques, ui.back_sques,
                      ui.multi, back_name, gubun, ui.dict_set)
            )
            ui.proc_backtester_ocvc.start()
        ui.StockBacktestLog()
        ui.ss_progressBar_01.setValue(0)
        ui.ssicon_alert = True


@error_decorator
def stock_optivars_to_gavars(ui):
    opti_vars_text = ui.ss_textEditttt_05.toPlainText()
    if opti_vars_text:
        ga_vars_text = ui.GetOptivarsToGavars(opti_vars_text)
        ui.ss_textEditttt_06.clear()
        ui.ss_textEditttt_06.append(ga_vars_text)
    else:
        QMessageBox.critical(ui, '오류 알림', '현재 최적화 범위 코드가 공백 상태입니다.\n최적화 범위 코드를 작성하거나 로딩하십시오.\n')


@error_decorator
def stock_gavars_to_optivars(ui):
    ga_vars_text = ui.ss_textEditttt_06.toPlainText()
    if ga_vars_text:
        opti_vars_text = ui.GetGavarsToOptivars(ga_vars_text)
        ui.ss_textEditttt_05.clear()
        ui.ss_textEditttt_05.append(opti_vars_text)
    else:
        QMessageBox.critical(ui, '오류 알림', '현재 GA 범위 코드가 공백 상태입니다.\nGA 범위 코드를 작성하거나 로딩하십시오.\n')


@error_decorator
def stock_stg_vars_change(ui):
    buystg = ui.ss_textEditttt_01.toPlainText()
    sellstg = ui.ss_textEditttt_02.toPlainText()
    buystg_str, sellstg_str = ui.GetStgtxtToVarstxt(buystg, sellstg)
    ui.ss_textEditttt_03.clear()
    ui.ss_textEditttt_04.clear()
    ui.ss_textEditttt_03.append(buystg_str)
    ui.ss_textEditttt_04.append(sellstg_str)


@error_decorator
def stock_stgvars_key_sort(ui):
    optivars = ui.ss_textEditttt_05.toPlainText()
    gavars = ui.ss_textEditttt_06.toPlainText()
    optivars_str, gavars_str = ui.GetStgtxtSort2(optivars, gavars)
    ui.ss_textEditttt_05.clear()
    ui.ss_textEditttt_06.clear()
    ui.ss_textEditttt_05.append(optivars_str)
    ui.ss_textEditttt_06.append(gavars_str)


@error_decorator
def stock_optivars_key_sort(ui):
    buystg = ui.ss_textEditttt_03.toPlainText()
    sellstg = ui.ss_textEditttt_04.toPlainText()
    buystg_str, sellstg_str = ui.GetStgtxtSort(buystg, sellstg)
    ui.ss_textEditttt_03.clear()
    ui.ss_textEditttt_04.clear()
    ui.ss_textEditttt_03.append(buystg_str)
    ui.ss_textEditttt_04.append(sellstg_str)


@error_decorator
def sChangeSvjButtonColor(ui):
    for button in ui.stock_editer_list:
        button.setStyleSheet(style_bc_dk if ui.focusWidget() == button else style_bc_bs)
