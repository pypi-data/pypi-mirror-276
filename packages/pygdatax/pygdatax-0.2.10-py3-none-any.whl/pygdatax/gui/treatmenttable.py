from silx.gui import qt
import os
from pygdatax.gui import FileBrowserWidget, DirectoryBrowserWidget, DataView
from pygdatax.instruments import sans
from pygdatax import cansas
from pygdatax.gui import DataView
import typing

class SpectraItemDelegate(qt.QItemDelegate):

    def __init__(self, directory=None, parent=None, extension=None):
        super().__init__(parent=parent)
        self.directory = None
        if directory:
            if os.path.isdir(directory) and os.path.exists(directory):
                self.directory = directory
        self.extension = extension

    def createEditor(self, parent: qt.QWidget, option: 'QStyleOptionViewItem', index: qt.QModelIndex) -> qt.QWidget:
        editor = qt.QLineEdit(parent)
        if self.directory and index.column() != 3:
            if not self.extension:
                completerList = os.listdir(self.directory)
            else:
                completerList = [file for file in os.listdir(self.directory) if file.endswith(self.extension)]
            completer = qt.QCompleter(completerList)
            editor.setCompleter(completer)
        # self.setFixedHeight(30)
        # self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.genersateMenu)
        return editor

    # def setEditorData(self, editor: qt.QWidget, index: QtCore.QModelIndex) -> None:


class SpectraTableModel(qt.QAbstractTableModel):

    def __init__(self, directory = None, vertical_header= None, extension=None):
        super().__init__()
        self._directory = None
        self._extension = extension
        self.set_directory(directory)
        self._headers = ['scatt', 'trans', 'trans_empty', 'tr value']
        self._vertical_header = vertical_header
        self._data = [["", "", "", ""]]
        if vertical_header:
            for i in range(len(vertical_header)-1):
                self.insertRow(-1)

    def rowCount(self, parent: qt.QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: qt.QModelIndex = ...) -> int:
        return len(self._headers)

    def headerData(self, section: int, orientation: qt.Qt.Orientation, role: int = ...)-> typing.Any:
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            return self._headers[section]
        if orientation == qt.Qt.Vertical and role == qt.Qt.DisplayRole:
            if self._vertical_header:
                return self._vertical_header[section]
            else:
                return f"{section + 1}"

    def data(self, index: qt.QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            if role == qt.Qt.DisplayRole or role == qt.Qt.EditRole:
                value = self._data[index.row()][index.column()]
                if index.column() ==3 and value is float:
                    return "%.4f" % value
                else:
                    return str(value)

    def setData(self, index: qt.QModelIndex, value: typing.Any, role= qt.Qt.EditRole) -> bool:
        if role ==qt. Qt.EditRole:
            col = index.column()
            if col == 3:
                try:
                    self._data[index.row()][index.column()] = float(value)
                    self.dataChanged.emit(index, index)
                    return True
                except ValueError:
                    return False
            else:
                path = os.path.join(self._directory,value)
                if os.path.exists(path):
                    if self._extension:
                        if path.endswith(self._extension):
                            self._data[index.row()][index.column()] = value
                            self.dataChanged.emit(index, index)
                            return True
                        else:
                            return False
                    else:
                        self._data[index.row()][index.column()] = value
                        self.dataChanged.emit(index, index)
                        return True
                else:
                    return False
        return False

    def flags(self, index: qt.QModelIndex) -> qt.Qt.ItemFlags:
        return qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled | qt.Qt.ItemIsEditable

    def insertRow(self, row, parent=qt.QModelIndex()):
        self.beginInsertRows(qt.QModelIndex(), row, row)
        self._data.insert(row, ["", "", "", ""])
        self.endInsertRows()
        return True

    def removeRow(self, row: int, parent: qt.QModelIndex = qt.QModelIndex()) -> bool:
        self.beginRemoveRows(qt.QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()
        return True

    def set_directory(self, directory):
        if directory:
            if os.path.isdir(directory) and os.path.exists(directory):
                self._directory = directory

    def get_directory(self):
        return self._directory


class SpectraTableView(qt.QTableView):
    show_data_clicked = qt.pyqtSignal(str)
    def __init__(self, directory=None, extension=None):
        super().__init__()
        self.setContextMenuPolicy(qt.Qt.ActionsContextMenu)
        self.setModel(SpectraTableModel(directory=directory, vertical_header=None, extension=extension))
        self.setItemDelegate(SpectraItemDelegate(parent=self, directory=directory, extension=extension))
        # add actions
        browseAction = qt.QAction(self)
        browseAction.setText('browse file')
        browseAction.triggered.connect(self.browse_data)
        showAction = qt.QAction(self)
        showAction.setText('show data')
        showAction.triggered.connect(self.on_show_data)
        self.addAction(browseAction)
        self.addAction(showAction)

    def set_directory(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            model = self.model()
            model.set_directory(path)
            delegate = self.itemDelegate()
            delegate.directory = path
            self.setItemDelegate(delegate)

    def browse_data(self):
        index = self.currentIndex()
        file, filter = qt.QFileDialog.getOpenFileName(self, caption="open data", directory=self.model()._directory, filter="Nexus File (*.nxs);; All (*.*)", options=qt.QFileDialog.DontUseNativeDialog)
        # if self.directory:
        #     dialog.setDirectory(self.directory)
        if file:
            ans = os.path.basename(file)
            model = self.model()
            model.setData(index,ans, role = qt.Qt.EditRole)
            self.setModel(model)

    def on_show_data(self):
        model = self.model()
        index = self.currentIndex()
        data = model.data(index, role = qt.Qt.DisplayRole)
        directory = model._directory
        if data:
            self.show_data_clicked.emit(os.path.join(directory, data))

class ReductionTableView(SpectraTableView):

    def __init__(self, directory=None, extension=None):
        super().__init__(directory=directory, extension=extension)
        model = SpectraTableModel(directory=directory, vertical_header=['dark', 'empty_cell', 'empty_beam' , 'water'])
        self.setModel(model)

    def get_files(self):
        """

        :return: files
        """
        model = self.model()
        directory = model.get_directory()
        ans = {}
        keyList =['dark_file', 'empty_cell_file', 'empty_beam_file', 'water_file']
        for i, key in enumerate(keyList):
            ans[key] = []
            for j in range(3):
                index = model.index(i,j)
                text = model.data(index,role=0)
                if text:
                    ans[key].append(os.path.join(directory,text))
                else:
                    ans[key].append(None)
        return ans


class ReductionParametersWidget(qt.QWidget):
    """
    Tab widget allowing to store reduction parameters such as the beam center, the mask file and the binning.
    The nummber of tabs corresponds to the number of detector
    """

    def __init__(self, parent=None):
        super(ReductionParametersWidget, self).__init__(parent=parent)
        self.x0LineEdit = qt.QLineEdit(parent=self)
        self.x0LineEdit.setValidator(qt.QDoubleValidator())
        self.y0LineEdit = qt.QLineEdit(parent=self)
        self.y0LineEdit.setValidator(qt.QDoubleValidator())
        self.distanceLineEdit = qt .QLineEdit(parent=self)
        self.distanceLineEdit.setValidator(qt.QDoubleValidator())
        self.binsLineEdit = qt.QLineEdit(parent=self)
        self.binsLineEdit.setValidator(qt.QIntValidator())
        self.maskLineEdit = FileBrowserWidget(label='mask file:', directory="", extensions="All files (*.*)", parent=self)
        layout = qt.QFormLayout()
        layout.addRow('x0 (pixels) : ', self.x0LineEdit)
        layout.addRow('y0 (pixels) :', self.y0LineEdit)
        layout.addRow('distance (mm):', self.distanceLineEdit)
        layout.addRow('bins :', self.binsLineEdit)
        vlayout = qt.QVBoxLayout()
        vlayout.addLayout(layout)
        vlayout.addWidget(self.maskLineEdit)
        self.setLayout(vlayout)

    def get_parameters(self):
        """
        Return a dictinnonary with reduction parameters (beam center, binning, mask file)
        :return:
        """
        d = {}
        x0 = self.x0LineEdit.text()
        if x0 != '':
            d['x0'] = float(x0)
        else:
            d['x0'] = None

        y0 = self.y0LineEdit.text()
        if y0 != '':
            d['y0'] = float(x0)
        else:
            d['y0'] = None

        bins = self.binsLineEdit.text()
        if bins:
            d['bins'] = int(bins)
        else:
            d['bins'] = None

        distance = self.distanceLineEdit.text()
        if distance:
            d['distance'] = float(distance)
        else:
            d['distance'] = None

        mask_file = self.maskLineEdit.get_file()
        if os.path.exists(mask_file):
            d['mask_file'] = mask_file
        else:
            d['mask_file'] = None
        return d


class ReductionParametersTabWidget(qt.QTabWidget):
    
    def __init__(self, nDet=1, parent=None):
        super(ReductionParametersTabWidget, self).__init__(parent=parent)
        for i in range(nDet):
            self.addTab(ReductionParametersWidget(parent=self), 'detector' + str(i))

    def get_parameters(self):
        d_all = {}
        nDet = self.count()
        d_all['x0'] = []
        d_all['y0'] = []
        d_all['mask_files'] = []
        d_all['distances'] = []
        for i in range(nDet):
            widget = self.widget(i)
            d = widget.get_parameters()
            d_all['x0'].append(d['x0'])
            d_all['y0'].append(d['y0'])
            d_all['mask_files'].append(d['mask_file'])
            d_all['distances'].append(d['distance'])
        print(d_all)
        return d_all


class ReductionPackageWidget(qt.QWidget):

    def __init__(self, parent=None, nDet=1, directory=None, extension=None):
        super(ReductionPackageWidget, self).__init__(parent=parent)
        self.parameterTabWidget = ReductionParametersTabWidget(nDet=nDet)
        self.table = ReductionTableView(directory=None, extension=extension)
        self.directoryBrowser = DirectoryBrowserWidget(label='data directory:', parent=self)
        # self.directoryButton = qt.QPushButton(parent=self)
        # self.directoryButton.setIcon(getQIcon('directory.ico'))
        #roi size for transmission computation
        self.roiWidthLineEdit = qt.QLineEdit("10")
        self.roiWidthLineEdit.setValidator(qt.QDoubleValidator())
        self.roiHeightLineEdit = qt.QLineEdit("10")
        self.roiHeightLineEdit.setValidator(qt.QDoubleValidator())
        # compute transmission button
        self.makePackageButton = qt.QPushButton("make reduction package")
        # self.packageFileLineEdit = qt.QLineEdit(parent=self)
        # self.saveButton = qt.QPushButton('Save', parent=self)
        # self.quitButton = qt.QPushButton('Quit', parent=self)
        # layout
        layout = qt.QVBoxLayout()
        layout.addWidget(self.directoryBrowser)
        layout.addWidget(self.parameterTabWidget)
        #roi
        hlayout = qt.QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(qt.QLabel("roi width (pixels):"))
        hlayout.addWidget(self.roiWidthLineEdit)
        hlayout.addWidget(qt.QLabel("roi height (pixels):"))
        hlayout.addWidget(self.roiHeightLineEdit)
        hlayout.addStretch(1)
        layout.addLayout(hlayout)
        layout.addWidget(self.makePackageButton)
        layout.addWidget(self.table)
        layout.addWidget(self.makePackageButton)
        # filename of the package to be saved
        # hlayout0 = qt.QHBoxLayout()
        # hlayout0.addWidget(qt.QLabel('Package file:'))
        # hlayout0.addWidget(self.packageFileLineEdit)
        # layout.addLayout(hlayout0)
        # buttons
        # hlayout = qt.QHBoxLayout()
        # hlayout.addWidget(self.saveButton)
        # hlayout.addWidget(self.quitButton)
        # layout.addLayout(hlayout)
        self.setLayout(layout)

        # connect signals
        # self.quitButton.clicked.connect(self.on_quit)
        # self.saveButton.clicked.connect(self.on_save)
        self.directoryBrowser.directoryChanged.connect(self.on_directoryChanged)
        self.table.show_data_clicked.connect(self.on_showData)
        self.makePackageButton.clicked.connect(self.on_makePackage)
        # init directory
        if directory and os.path.isdir(directory):
            self.directoryBrowser.set_directory(directory)

    def on_directoryChanged(self, path):
        self.table.set_directory(path)

    def on_showData(self, filepath):
        w = DataView()

        w.addImage()
        pass

    def on_makePackage(self):
        files = self.table.get_files()
        params = self.parameterTabWidget.get_parameters()
        x0 = params["x0"]
        y0 = params["y0"]
        tList = len(files)*[None]
        try:
            roi_width = float(self.roiWidthLineEdit.text())
            roi_heigth = float(self.roiHeightLineEdit.text())
            roi = [int(x0[0]-roi_width/2), int(y0[0]-roi_heigth/2), int(x0[0]+roi_width/2), int(y0[0]+roi_heigth/2)]
        except TypeError:
            roi = [None, None, None, None]
        for i, key in enumerate(files):
            # scattering file
            if files[key][0]:
                files[key][0] = cansas.convert2nxsas(files[key][0])
            # transmission file
            if files[key][1]:
                files[key][1] = cansas.convert2nxsas(files[key][1])
            # direct_beam
            if files[key][2]:
                files[key][2] = cansas.convert2nxsas(files[key][2])

            if files[key][0]:
                for j in range(len(x0)):
                    sans.set_beam_center(files[key][0], x0=x0[j], y0=y0[j], detector_number=j)
                tList[i] = sans.set_transmission(files[key][0], trans_file=files[key][1],
                                                 direct_beam_file=files[key][2], roi=roi)
        packagepath, _ = qt.QFileDialog.getSaveFileName(self, "Save reduction package", "", "All (*.*) ; Nexus (*.nxs)", options=qt.QFileDialog.DontUseNativeDialog)
        if packagepath:
        # packagepath = os.path.join(self.table.model().get_directory(),'lot0.nxs')
            for key in files:
                files[key] = files[key][0]

            sans.make_reduction_package(packagepath, x0=x0, y0=y0, mask_files=params['mask_files'],
                                        distance=params['distances'],
                                        **files)

        for i, trans in enumerate(tList):
            model = self.table.model()
            index = model.index(i, 3)
            if trans:
                model.setData(index, trans)

    def on_quit(self):
        self.close()


if __name__ == '__main__':
    import sys

    standards = dict()
    standards['FD'] = ['XY3200', 'XY3208', 'XY3216', 'XY3226']
    standards['B4C'] = [['XY3206', 'XY3200'], ['XY3214', 'XY3208'], ['XY3223', 'XY3216'], ['XY3233', 'XY3226']]
    standards['EC'] = [['XY3207', 'XY3203'], ['XY3215', 'XY3211'], ['XY3224', 'XY3219'], ['XY3234', 'XY3229']]
    standards['H2O'] = [[None, None], [None, None], ['XY3225', 'XY3220'], ['XY3235', 'XY3230']]
    sample = dict()
    sample['NE_PS30k_HG'] = [['XY3204', 'XY3201'],
                                  ['XY3212', 'XY3209'],
                                  ['XY3221', 'XY3217'],
                                  ['XY3231', 'XY3227']]
    mask_file = ['mask_TPQ.edf', 'mask_PQ.edf', 'mask_MQ.edf', 'mask_GQ.edf']
    norm_file = ['norm_TPQ.nxs', 'norm_PQ.nxs', 'norm_MQ.nxs', 'norm_GQ.nxs']
    sub_file = ['sous_TPQ.nxs', 'sous_PQ.nxs', 'sous_MQ.nxs', 'sous_GQ.nxs']
    app = qt.QApplication([])
    folder = "/home/achennev/python/pygdatax/example_data/PAXY"
    w = ReductionPackageWidget(nDet=1, directory=folder,extension='.32')
    # init table
    model = w.table.model()
    index = model.index(0,0)
    model.setData(index, standards['B4C'][0][0]+'.32')
    index = model.index(0, 1)
    model.setData(index, standards['B4C'][0][1] + '.32')
    index = model.index(0, 2)
    model.setData(index, standards['FD'][0] + '.32')
    index = model.index(1,0)
    model.setData(index, standards['EC'][0][0]+'.32')
    index = model.index(1, 1)
    model.setData(index, standards['EC'][0][1] + '.32')
    index = model.index(1, 2)
    model.setData(index, standards['FD'][0] + '.32')

    w.show()
    result = app.exec_()
    app.deleteLater()
    sys.exit(result)
    # dark_file: str = None, empty_cell_file: str = None, empty_beam_file: str = None,
    #                            water_file: str = None,
    #                            mask_files: Union[str, list]= None,
    #                            x0: Union[float, list] = None,
    #                            y0
