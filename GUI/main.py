import sys
from PyQt5.QtWidgets import *

from node_editor_wnd import NodeEditorWnd

if __name__ == '__main__':
    # Start application
    app = QApplication(sys.argv)
    wnd = NodeEditorWnd()

    # Close application
    app.aboutToQuit.connect(wnd.cleanupResources)
    sys.exit(app.exec_())

