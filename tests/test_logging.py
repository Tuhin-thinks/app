from pathlib import Path
import os
from PyQt5.QtWidgets import QApplication
import pytest
from pytestqt.qtbot import QtBot

from PyQt5 import QtCore

from src.run_torpoker import AppHome
from m_logging import get_logger

LOGS_DIR = Path(__file__).parent.parent / "test_logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = get_logger(__name__, LOGS_DIR / "test_logging.log")


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

    assert app_home.ui.statusbar.currentMessage() == "Connecting..."

    qtbot.wait(5000)  # wait for 5secs.


def test_joinTable_open(app_home: AppHome, qapp: QtBot, qtbot: QtBot):
    active_window = QApplication.activeWindow()
    assert active_window is not None

    logger.info("active window title:" + active_window.windowTitle())
