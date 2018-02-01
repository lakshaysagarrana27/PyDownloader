from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import urllib.request


class Downloader(QDialog):
    # creating a derived class for our application and inheriting in from QDialog class

    def __init__(self):
        # constructor or initializer for our class
        QDialog.__init__(self)
        # inherits constructor from QDialog super class

        # Adding widgets
        layout = QVBoxLayout()  # creating a layout QVBox means Vertical Box

        self.url = QLineEdit()  # LineEdit where user enter the url, this is stored in url variable.
        self.save_location = QLineEdit()  # Line edit where user enter the location to save the file.
        # that is then stored to save_location variable.
        self.progress = QProgressBar()  # Progress bar
        download = QPushButton("Download")  # Download push Button
        browse = QPushButton("Browse") # Push Button to open dialog box which will browse the dirctory to save the file

        self.url.setPlaceholderText("Enter URL Here")  # Place Holder Text to show in Line Edit
        self.save_location.setPlaceholderText("File Save Location!")  # Place Holder Text to show in save_location
        self.progress.setValue(0)  # sets the initial value of progress bar to 0
        self.progress.setAlignment(Qt.AlignCenter)  # sets the alignment of zero to center in the progress bar

        # Now Add those widgets to the Layout
        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(download)

        self.setLayout(layout)  # setting the layout

        self.setWindowTitle("PyDownloader")  # setting the windows title to PyDownloader

        self.setFocus()  # this sets the focus to full window in other words at first the blinking cursor
        # is at url and we cannot see the placeholder text with this we can set the focus to window and then no cursor
        # will appear

        download.clicked.connect(self.download)  # when user clicks on download start download function

        browse.clicked.connect(self.browse_file) # when user clicks on browse button browse file function will start

    def browse_file(self): # this will open a dialog box from where user can chose the directory to save the file

        save_file = QFileDialog.getSaveFileName(self, caption="Save File As", directory=".", filter="All files (*.*)")
        # above line will open dialog box with name of box as "Save file as" as written in caption
        # and at opening the directory will be where the python file is stored as "." is in dirctory
        # and file types will all as in filter
        # then this path will be stored in save_file as string in PyQt
        # and as tuple in PySide and as we are using PyQt this will be stores as String

        self.save_location.setText(QDir.toNativeSeparators(save_file))
        # this will change the value of save_location to directory chosen by user
        # since we are making platform independent application
        # '\' are used in windows and '/' are used in linux or Mac
        # for eg. /home/blackpanda/downloads in linux.
        # the chosen directory may sometime show different backlshes so QDir.toNativeSeprator fix this
        # by converting the directory sepreator to native which is used by platform we are using
        # the program with

    def download(self):
        # this function will start the download process by asking the url entered to recieve data and
        # will update the progress bar and after that show appropriate mesage whether download failed or completed

        url = self.url.text()  # this converts url to string

        save_location = self.save_location.text()  # this converts save_location to string

        # try block below will will run the request function from urrlib with url save_location and report hook
        # and if any error arises, it will open a warning dialog that download failed and will return from function

        try:
            urllib.request.urlretrieve(url, save_location, self.report)
        except Exception:
            QMessageBox.warning(self, "Warning", "The download failed")
            return

        # if no exception arises and download is completed then dialog box will appear which will show that
        # download is completed
        QMessageBox.information(self, "Information", "The Download is completed")

        # these below line will reset the the url field, location field and progress bar

        self.progress.setValue(0)
        self.url.setText("")
        self.save_location.setText("")

    def report(self, blocknum, blocksize, totalsize):
        # this function is called in urlretrieve in download function
        # basically the third argument is in urlretreive is report hook which will send the block size ,
        # no of blocks sent and total size. So this is used to calculate progress as in block below
        # and will update the progress bar

        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            self.progress.setValue(int(percent))


# Starts the application
app = QApplication(sys.argv)
d1 = Downloader()
d1.show()
app.exec()

