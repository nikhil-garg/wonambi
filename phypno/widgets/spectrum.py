"""Widget to show power spectrum.

"""
from logging import getLogger
lg = getLogger(__name__)

from numpy import log, ceil, floor, min
from scipy.signal import welch
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QComboBox,
                         QFormLayout,
                         QGraphicsView,
                         QGraphicsScene,
                         QGroupBox,
                         QPen,
                         QVBoxLayout,
                         QWidget,
                         )

from .utils import Path
from .settings import Config, FormFloat, FormBool


class ConfigSpectrum(Config):

    def __init__(self, update_widget):
        super().__init__('spectrum', update_widget)

    def create_config(self):

        box0 = QGroupBox('Spectrum')

        for k in self.value:
            self.index[k] = FormFloat()
        self.index['log'] = FormBool('Log-transform')

        form_layout = QFormLayout()
        form_layout.addRow('Min X', self.index['x_min'])
        form_layout.addRow('Max X', self.index['x_max'])
        form_layout.addRow('Ticks on X-axis', self.index['x_tick'])
        form_layout.addRow('Min Y', self.index['y_min'])
        form_layout.addRow('Max Y', self.index['y_max'])
        form_layout.addRow('Ticks on Y-axis', self.index['y_tick'])

        form_layout.addWidget(self.index['log'])
        box0.setLayout(form_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(box0)
        main_layout.addStretch(1)

        self.setLayout(main_layout)


class Spectrum(QWidget):
    """Plot the power spectrum for a specified channel.

    Attributes
    ----------
    parent : instance of QMainWindow
        the main window.
    x_limit : tuple or list
        2 values specifying the limit on x-axis
    y_limit : tuple or list
        2 values specifying the limit on y-axis
    log : bool
        log-transform the data or not
    idx_chan : instance of QComboBox
        the element with the list of channel names.
    idx_x_min : instance of QLineEdit
        value with min x value
    idx_x_max : instance of QLineEdit
        value with max x value
    idx_y_min : instance of QLineEdit
        value with min y value
    idx_y_max : instance of QLineEdit
        value with max y value
    idx_log : instance of QCheckBox
        widget that defines if log should be used or not
    idx_fig : instance of QGraphicsView
        the view with the power spectrum
    scene : instance of QGraphicsScene
        the scene with GraphicsItems

    Notes
    -----
    If data contains NaN, it doesn't create any spectrum (feature or bug?).

    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.config = ConfigSpectrum(self.display)

        self.idx_chan = None
        self.idx_fig = None
        self.scene = None

        self.create()

    def create(self):
        """Create empty scene for power spectrum."""
        self.idx_chan = QComboBox()
        self.idx_chan.activated.connect(self.display_window)

        self.idx_fig = QGraphicsView(self)
        self.idx_fig.scale(1, -1)

        value = self.config.value
        self.scene = QGraphicsScene(value['x_min'], value['y_min'],
                                    value['x_max'] - value['x_min'],
                                    value['y_max'] - value['y_min'])
        self.idx_fig.setScene(self.scene)

        layout = QVBoxLayout()
        layout.addWidget(self.idx_chan)
        layout.addWidget(self.idx_fig)
        self.setLayout(layout)

        self.resizeEvent(None)

    def update(self):
        """Add channel names to the combobox.

        This function is called when the channels are chosen. But it doesn't
        display the power spectrum yet, because that can only happen after
        the recordings have been read.

        """
        self.idx_chan.clear()
        for chan_name in self.parent.traces.chan:
            self.idx_chan.addItem(chan_name)

    def display_window(self):
        """Read the channel name from QComboBox and plot its spectrum.

        This function is necessary it reads the data and it sends it to
        self.display. When the user selects a smaller chunk of data from the
        visible traces, then we don't need to call this function.
        """
        chan_name = self.idx_chan.currentText()
        lg.info('Power spectrum for channel ' + chan_name)

        if not chan_name:
            return

        trial = 0
        data = self.parent.traces.data(trial=trial, chan=chan_name)
        self.display(data)

    def display(self, data):
        """Make graphicsitem for spectrum figure.

        Parameters
        ----------
        data : ndarray
            1D vector containing the data only

        This function can be called by self.display_window (which reads the
        data for the selected channel) or by the mouse-events functions in
        traces (which read chunks of data from the user-made selection).
        """
        value = self.config.value
        self.scene.setSceneRect(value['x_min'], value['y_min'],
                                value['x_max'] - value['x_min'],
                                value['y_max'] - value['y_min'])
        self.scene.clear()
        self.add_grid()
        self.resizeEvent(None)

        s_freq = self.parent.traces.data.s_freq
        f, Pxx = welch(data, fs=s_freq, nperseg=min((s_freq, len(data))))

        freq_limit = (value['x_min'] <= f) & (f <= value['x_max'])

        if self.config.value['log']:
            Pxx_to_plot = log(Pxx[freq_limit])
        else:
            Pxx_to_plot = Pxx[freq_limit]

        self.scene.addPath(Path(f[freq_limit], Pxx_to_plot))

    def add_grid(self):
        """Add axis and ticks to figure.

        Notes
        -----
        I know that visvis and pyqtgraphs can do this in much simpler way, but
        those packages create too large a padding around the figure and this is
        pretty fast.

        """
        value = self.config.value

        # X-AXIS
        # x-bottom
        self.scene.addLine(value['x_min'], value['y_min'],
                           value['x_min'], value['y_max'])
        # at y = 0, dashed
        self.scene.addLine(value['x_min'], 0,
                           value['x_max'], 0, QPen(Qt.DashLine))
        # ticks on y-axis
        y_high = int(floor(value['y_max']))
        y_low = int(ceil(value['y_min']))
        x_length = (value['x_max'] - value['x_min']) / value['x_tick']
        for y in range(y_low, y_high):
            self.scene.addLine(value['x_min'], y,
                               value['x_min'] + x_length, y)
        # Y-AXIS
        # left axis
        self.scene.addLine(value['x_min'], value['y_min'],
                           value['x_max'], value['y_min'])
        # larger ticks on x-axis every 10 Hz
        x_high = int(floor(value['x_max']))
        x_low = int(ceil(value['x_min']))
        y_length = (value['y_max'] - value['y_min']) / value['y_tick']
        for x in range(x_low, x_high, 10):
            self.scene.addLine(x, value['y_min'],
                               x, value['y_min'] + y_length)
        # smaller ticks on x-axis every 10 Hz
        y_length = (value['y_max'] - value['y_min']) / value['y_tick'] / 2
        for x in range(x_low, x_high, 5):
            self.scene.addLine(x, value['y_min'],
                               x, value['y_min'] + y_length)

    def resizeEvent(self, event):
        """Fit the whole scene in view.

        Parameters
        ----------
        event : instance of Qt.Event
            not important

        """
        lg.debug('resize spectrum')
        value = self.config.value
        self.idx_fig.fitInView(value['x_min'],
                               value['y_min'],
                               value['x_max'] - value['x_min'],
                               value['y_max'] - value['y_min'])
