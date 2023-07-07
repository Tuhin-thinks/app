from pathlib import Path
import os
from PyQt5.QtWidgets import QApplication
import pytest
from pytestqt.qtbot import QtBot

from PyQt5 import QtCore

from src.run_torpoker import AppHome


@pytest.fixture  # (scope="module")
def app_home(qtbot: QtBot):
    os.chdir(Path(__file__).parent.parent / "src")
    window = AppHome()
    # window.show()
    qtbot.addWidget(window)
    
    # run
    yield window
    
    # teardown


def test_xmr_login(app_home: AppHome, qapp: QtBot, qtbot: QtBot):
    host_string = "xmr.poker"
    port_string = "443"
    
    app_home.ui.lineEdit_address.setText(host_string)
    app_home.ui.lineEdit_address_port.setText(port_string)
    
    qtbot.mouseClick(app_home.ui.pushButton_connect, QtCore.Qt.LeftButton)
