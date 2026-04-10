
from PyQt5.QtCore import Qt
from ui.set_widget import BounceButton
from utility.static import error_decorator
from PyQt5.QtWidgets import QPushButton, QMessageBox
from ui.ui_process_alive import trader_process_alive


@error_decorator
def checkbox_changed_01(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state != Qt.Checked and trader_process_alive(ui):
        ui.sj_main_cheBox_01.nextCheckState()
        QMessageBox.critical(ui, '오류 알림', '트레이더 실행 중에는 모의모드를 해제할 수 없습니다.\n')


@error_decorator
def checkbox_changed_02(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state != Qt.Checked:
        if ui.dialog_factor.focusWidget() == ui.ft_checkBoxxxxx_01:
            ui.ft_checkBoxxxxx_01.nextCheckState()
            QMessageBox.critical(ui.dialog_factor, '오류 알림', '현재가는 해제할 수 없습니다.\n')


@error_decorator
def checkbox_changed_03(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state == Qt.Checked:
        for widget in ui.sj_ilbunback_listtt:
            if widget != ui.focusWidget() and widget.isChecked():
                widget.nextCheckState()


@error_decorator
def checkbox_changed_04(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state == Qt.Checked:
        if not ui.sj_back_cheBox_13.isChecked():
            ui.sj_back_cheBox_13.nextCheckState()


@error_decorator
def checkbox_changed_05(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state != Qt.Checked:
        if ui.sj_back_cheBox_12.isChecked():
            ui.sj_back_cheBox_12.nextCheckState()


@error_decorator
def checkbox_changed_06(ui, state):
    gubun = ui.list_checkBoxxxxxx.index(ui.dialog_scheduler.focusWidget())
    if state == Qt.Checked:
        for item in ('백테스트',
                     '그리드 최적화', '그리드 검증 최적화', '그리드 교차검증 최적화',
                     '그리드 최적화 테스트', '그리드 검증 최적화 테스트', '그리드 교차검증 최적화 테스트',
                     '그리드 최적화 전진분석', '그리드 검증 최적화 전진분석', '그리드 교차검증 최적화 전진분석',
                     '베이지안 최적화', '베이지안 검증 최적화', '베이지안 교차검증 최적화',
                     '베이지안 최적화 테스트', '베이지안 검증 최적화 테스트', '베이지안 교차검증 최적화 테스트',
                     '베이지안 최적화 전진분석', '베이지안 검증 최적화 전진분석', '베이지안 교차검증 최적화 전진분석',
                     'GA 최적화', '검증 GA 최적화', '교차검증 GA 최적화',
                     '조건 최적화', '검증 조건 최적화', '교차검증 조건 최적화'):
            ui.list_gcomboBoxxxxx[gubun].addItem(item)
    else:
        ui.list_gcomboBoxxxxx[gubun].clear()
        ui.list_bcomboBoxxxxx[gubun].clear()
        ui.list_scomboBoxxxxx[gubun].clear()
        ui.list_vcomboBoxxxxx[gubun].clear()
        ui.list_p1comboBoxxxx[gubun].clear()
        ui.list_p2comboBoxxxx[gubun].clear()
        ui.list_p3comboBoxxxx[gubun].clear()
        ui.list_p4comboBoxxxx[gubun].clear()
        ui.list_tcomboBoxxxxx[gubun].clear()


@error_decorator
def checkbox_changed_07(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton):
        if state == Qt.Checked:
            if ui.sj_back_cheBox_16.isChecked():
                ui.sj_back_cheBox_16.nextCheckState()
        else:
            if not ui.sj_back_cheBox_16.isChecked():
                ui.sj_back_cheBox_16.nextCheckState()


@error_decorator
def checkbox_changed_08(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton):
        if state == Qt.Checked:
            if ui.sj_back_cheBox_15.isChecked():
                ui.sj_back_cheBox_15.nextCheckState()
        else:
            if not ui.sj_back_cheBox_15.isChecked():
                ui.sj_back_cheBox_15.nextCheckState()


# noinspection PyUnusedLocal
@error_decorator
def checkbox_changed_09(ui, state):
    ui.ctpg_code = None


@error_decorator
def sbcheckbox_changed_01(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state == Qt.Checked:
        for widget in ui.sodb_checkbox_list1:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


@error_decorator
def sbcheckbox_changed_02(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state == Qt.Checked:
        for widget in ui.sodb_checkbox_list2:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


@error_decorator
def sscheckbox_changed_01(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state == Qt.Checked:
        for widget in ui.sods_checkbox_list1:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


@error_decorator
def sscheckbox_changed_02(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton) and state == Qt.Checked:
        for widget in ui.sods_checkbox_list2:
            if widget != ui.focusWidget():
                if widget.isChecked():
                    widget.nextCheckState()


@error_decorator
def setting_stock_weight_cotrol_changed(ui, state):
    if ui.focusWidget().__class__ not in (QPushButton, BounceButton):
        if state == Qt.Checked:
            for widget in ui.ss_bj_check_button_list:
                if widget != ui.focusWidget():
                    if widget.isChecked():
                        widget.nextCheckState()
