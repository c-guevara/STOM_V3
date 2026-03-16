
from PyQt5.QtCore import QRect, QParallelAnimationGroup, QPropertyAnimation, QEasingCurve
from utility.static import error_decorator


def group_animation(ui, pushButton, textEdit, pushButton_qrect, textEdit_qrect, finished_func=None):
    current_geo_btn01 = pushButton.geometry()
    current_geo_tedt1 = textEdit.geometry()

    ui.animation_group = QParallelAnimationGroup()

    anim_btn01 = QPropertyAnimation(textEdit, b'geometry')
    anim_btn01.setDuration(500)
    anim_btn01.setEasingCurve(QEasingCurve.InOutCirc)
    anim_btn01.setStartValue(current_geo_tedt1)
    anim_btn01.setEndValue(textEdit_qrect)

    anim_tedt1 = QPropertyAnimation(pushButton, b'geometry')
    anim_tedt1.setDuration(500)
    anim_tedt1.setEasingCurve(QEasingCurve.InOutCirc)
    anim_tedt1.setStartValue(current_geo_btn01)
    anim_tedt1.setEndValue(pushButton_qrect)
    if finished_func is not None:
        anim_tedt1.finished.connect(finished_func)

    ui.animation_group.addAnimation(anim_btn01)
    ui.animation_group.addAnimation(anim_tedt1)

    ui.animation_group.start()


@error_decorator
def sz_button_clicked_01(ui):
    def finished_func1():
        ui.ss_textEditttt_02.setVisible(False)
        ui.szoo_pushButon_02.setVisible(False)

    def finished_func2():
        ui.ss_textEditttt_02.setVisible(True)
        ui.szoo_pushButon_02.setVisible(True)

    def finished_func3():
        ui.ss_textEditttt_04.setVisible(False)
        if ui.sva_pushButton_01.isVisible():
            ui.ss_textEditttt_06.setVisible(False)
        else:
            ui.ss_textEditttt_05.setVisible(False)
        ui.szoo_pushButon_02.setVisible(False)

    def finished_func4():
        ui.ss_textEditttt_04.setVisible(True)
        if ui.sva_pushButton_01.isVisible():
            ui.ss_textEditttt_06.setVisible(True)
        else:
            ui.ss_textEditttt_05.setVisible(True)
        ui.szoo_pushButon_02.setVisible(True)

    if ui.svj_pushButton_01.isVisible():
        if ui.szoo_pushButon_01.text() == '확대(esc)':
            ui.szoo_pushButon_01.setText('축소(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_01,
                ui.ss_textEditttt_01,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func1
            )
        else:
            ui.szoo_pushButon_01.setText('확대(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_01,
                ui.ss_textEditttt_01,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 740 if ui.extend_window else 463),
                finished_func2
            )
    else:
        if ui.szoo_pushButon_01.text() == '확대(esc)':
            ui.szoo_pushButon_01.setText('축소(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_01,
                ui.ss_textEditttt_03,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func3
            )
        else:
            ui.szoo_pushButon_01.setText('확대(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_01,
                ui.ss_textEditttt_03,
                QRect(584, 15, 50, 20),
                QRect(7, 10, 647, 740 if ui.extend_window else 463),
                finished_func4
            )


@error_decorator
def sz_button_clicked_02(ui):
    def finished_func1():
        ui.ss_textEditttt_01.setVisible(False)
        ui.szoo_pushButon_01.setVisible(False)

    def finished_func2():
        ui.ss_textEditttt_01.setVisible(True)
        ui.szoo_pushButon_01.setVisible(True)

    def finished_func3():
        ui.ss_textEditttt_03.setVisible(False)
        if ui.sva_pushButton_01.isVisible():
            ui.ss_textEditttt_06.setVisible(False)
        else:
            ui.ss_textEditttt_05.setVisible(False)
        ui.szoo_pushButon_01.setVisible(False)

    def finished_func4():
        ui.ss_textEditttt_03.setVisible(True)
        if ui.sva_pushButton_01.isVisible():
            ui.ss_textEditttt_06.setVisible(True)
        else:
            ui.ss_textEditttt_05.setVisible(True)
        ui.szoo_pushButon_01.setVisible(True)

    if ui.svj_pushButton_01.isVisible():
        if ui.szoo_pushButon_02.text() == '확대(esc)':
            ui.szoo_pushButon_02.setText('축소(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_02,
                ui.ss_textEditttt_02,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func1
            )
        else:
            ui.szoo_pushButon_02.setText('확대(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_02,
                ui.ss_textEditttt_02,
                QRect(937, 761 if ui.extend_window else 483, 50, 20),
                QRect(7, 756 if ui.extend_window else 480, 1000, 602 if ui.extend_window else 272),
                finished_func2
            )
    else:
        if ui.szoo_pushButon_02.text() == '확대(esc)':
            ui.szoo_pushButon_02.setText('축소(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_02,
                ui.ss_textEditttt_04,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func3
            )
        else:
            ui.szoo_pushButon_02.setText('확대(esc)')
            group_animation(
                ui,
                ui.szoo_pushButon_02,
                ui.ss_textEditttt_04,
                QRect(584, 761 if ui.extend_window else 483, 50, 20),
                QRect(7, 756 if ui.extend_window else 480, 647, 602 if ui.extend_window else 272),
                finished_func4
            )


@error_decorator
def cz_button_clicked_01(ui):
    def finished_func1():
        ui.cs_textEditttt_02.setVisible(False)
        ui.czoo_pushButon_02.setVisible(False)

    def finished_func2():
        ui.cs_textEditttt_02.setVisible(True)
        ui.czoo_pushButon_02.setVisible(True)

    def finished_func3():
        ui.cs_textEditttt_04.setVisible(False)
        if ui.cva_pushButton_01.isVisible():
            ui.cs_textEditttt_06.setVisible(False)
        else:
            ui.cs_textEditttt_05.setVisible(False)
        ui.czoo_pushButon_02.setVisible(False)

    def finished_func4():
        ui.cs_textEditttt_04.setVisible(True)
        if ui.cva_pushButton_01.isVisible():
            ui.cs_textEditttt_06.setVisible(True)
        else:
            ui.cs_textEditttt_05.setVisible(True)
        ui.czoo_pushButon_02.setVisible(True)

    if ui.cvj_pushButton_01.isVisible():
        if ui.czoo_pushButon_01.text() == '확대(esc)':
            ui.czoo_pushButon_01.setText('축소(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_01,
                ui.cs_textEditttt_01,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func1
            )
        else:
            ui.czoo_pushButon_01.setText('확대(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_01,
                ui.cs_textEditttt_01,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 740 if ui.extend_window else 463),
                finished_func2
            )
    else:
        if ui.czoo_pushButon_01.text() == '확대(esc)':
            ui.czoo_pushButon_01.setText('축소(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_01,
                ui.cs_textEditttt_03,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func3
            )
        else:
            ui.czoo_pushButon_01.setText('확대(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_01,
                ui.cs_textEditttt_03,
                QRect(584, 15, 50, 20),
                QRect(7, 10, 647, 740 if ui.extend_window else 463),
                finished_func4
            )


@error_decorator
def cz_button_clicked_02(ui):
    def finished_func1():
        ui.cs_textEditttt_01.setVisible(False)
        ui.czoo_pushButon_01.setVisible(False)

    def finished_func2():
        ui.cs_textEditttt_01.setVisible(True)
        ui.czoo_pushButon_01.setVisible(True)

    def finished_func3():
        ui.cs_textEditttt_03.setVisible(False)
        if ui.cva_pushButton_01.isVisible():
            ui.cs_textEditttt_06.setVisible(False)
        else:
            ui.cs_textEditttt_05.setVisible(False)
        ui.czoo_pushButon_01.setVisible(False)

    def finished_func4():
        ui.cs_textEditttt_03.setVisible(True)
        if ui.cva_pushButton_01.isVisible():
            ui.cs_textEditttt_06.setVisible(True)
        else:
            ui.cs_textEditttt_05.setVisible(True)
        ui.czoo_pushButon_01.setVisible(True)

    if ui.cvj_pushButton_01.isVisible():
        if ui.czoo_pushButon_02.text() == '확대(esc)':
            ui.czoo_pushButon_02.setText('축소(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_02,
                ui.cs_textEditttt_02,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func1
            )
        else:
            ui.czoo_pushButon_02.setText('확대(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_02,
                ui.cs_textEditttt_02,
                QRect(937, 761 if ui.extend_window else 483, 50, 20),
                QRect(7, 756 if ui.extend_window else 480, 1000, 602 if ui.extend_window else 272),
                finished_func2
            )
    else:
        if ui.czoo_pushButon_02.text() == '확대(esc)':
            ui.czoo_pushButon_02.setText('축소(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_02,
                ui.cs_textEditttt_04,
                QRect(937, 15, 50, 20),
                QRect(7, 10, 1000, 1347 if ui.extend_window else 740),
                finished_func3
            )
        else:
            ui.czoo_pushButon_02.setText('확대(esc)')
            group_animation(
                ui,
                ui.czoo_pushButon_02,
                ui.cs_textEditttt_04,
                QRect(584, 761 if ui.extend_window else 483, 50, 20),
                QRect(7, 756 if ui.extend_window else 478, 647, 602 if ui.extend_window else 272),
                finished_func4
            )
