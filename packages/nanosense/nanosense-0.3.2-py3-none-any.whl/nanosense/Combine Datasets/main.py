import sys 
import os 
from PySide6 .QtWidgets import QApplication ,QWidget ,QLabel ,QPushButton ,QCheckBox ,QComboBox ,QListWidget ,QVBoxLayout ,QHBoxLayout ,QFileDialog ,QMessageBox ,QStyleFactory 
from PySide6 .QtCore import Qt 
from PySide6 .QtGui import QPalette ,QColor ,QFont 
import numpy as np 

class SDCombineDatasets (QWidget ):
    def __init__ (self ):
        super ().__init__ ()
        self .setWindowTitle ("SD Combine Datasets")
        self .resize (500 ,700 )


        self .app_name_label =QLabel ("SD Combine Datasets")
        self .app_name_label .setAlignment (Qt .AlignCenter )
        self .app_name_label .setFont (QFont ("Arial",16 ,QFont .Bold ))
        self .email_label =QLabel ("shankar.dutt@anu.edu.au")
        self .email_label .setAlignment (Qt .AlignCenter )
        self .select_folder_button =QPushButton ("Select Folder")
        self .include_subfolders_checkbox =QCheckBox ("Include Subfolders")
        self .extension_dropdown =QComboBox ()
        self .extension_dropdown .addItems ([".dataset.npz",".MLdataset.npz"])
        self .file_list =QListWidget ()
        self .file_list .setSelectionMode (QListWidget .SelectionMode .MultiSelection )
        self .select_all_checkbox =QCheckBox ("Select All")
        self .folder_path_label =QLabel ()
        self .folder_path_label .setWordWrap (True )
        self .combine_datasets_button =QPushButton ("Combine Datasets")


        main_layout =QVBoxLayout ()
        main_layout .addWidget (self .app_name_label )
        main_layout .addWidget (self .email_label )
        main_layout .addWidget (self .select_folder_button )
        main_layout .addWidget (self .include_subfolders_checkbox )
        main_layout .addWidget (self .extension_dropdown )
        main_layout .addWidget (self .file_list )
        main_layout .addWidget (self .select_all_checkbox )
        main_layout .addWidget (self .folder_path_label )
        main_layout .addWidget (self .combine_datasets_button )

        self .setLayout (main_layout )


        self .select_folder_button .clicked .connect (self .select_folder )
        self .select_all_checkbox .stateChanged .connect (self .select_all )
        self .combine_datasets_button .clicked .connect (self .combine_datasets )

    def select_folder (self ):
        folder_path =QFileDialog .getExistingDirectory (self ,"Select Folder")
        if folder_path :
            self .file_list .clear ()
            self .folder_path_label .setText (f"Selected Folder: {folder_path}")
            extension =self .extension_dropdown .currentText ()
            if self .include_subfolders_checkbox .isChecked ():
                for root ,dirs ,files in os .walk (folder_path ):
                    for file in files :
                        if file .endswith (extension ):
                            file_path =os .path .relpath (os .path .join (root ,file ),folder_path )
                            self .file_list .addItem (file_path )
            else :
                for file in os .listdir (folder_path ):
                    if file .endswith (extension ):
                        self .file_list .addItem (file )

    def select_all (self ,state ):
        is_checked =self .select_all_checkbox .isChecked ()
        for index in range (self .file_list .count ()):
            item =self .file_list .item (index )
            item .setSelected (is_checked )

    def combine_datasets (self ):
        selected_files =[self .file_list .item (i ).text ()for i in range (self .file_list .count ())if self .file_list .item (i ).isSelected ()]
        if selected_files :
            combined_data =None 
            settings_file =None 
            folder_path =self .folder_path_label .text ().replace ("Selected Folder: ","")
            for file_path in selected_files :
                full_path =os .path .join (folder_path ,file_path )
                with np .load (full_path )as data :
                    if combined_data is None :
                        combined_data =data ['X']
                    else :
                        combined_data =np .concatenate ((combined_data ,data ['X']))
                    if settings_file is None :
                        settings_file =data ['settings']

            extension =self .extension_dropdown .currentText ()
            save_path ,_ =QFileDialog .getSaveFileName (self ,"Save Combined Dataset","",f"NumPy Files (*{extension})")
            if save_path :
                if not save_path .endswith (extension ):
                    save_path +=extension 
                np .savez (save_path ,X =combined_data ,settings =settings_file )
                QMessageBox .information (self ,"Success","Datasets combined successfully.")
        else :
            QMessageBox .warning (self ,"Warning","No files selected.")

if __name__ =='__main__':
    app =QApplication (sys .argv )
    app .setStyle (QStyleFactory .create ('Fusion'))


    palette =QPalette ()
    palette .setColor (QPalette .ColorRole .Window ,QColor (53 ,53 ,53 ))
    palette .setColor (QPalette .ColorRole .WindowText ,Qt .GlobalColor .white )
    palette .setColor (QPalette .ColorRole .Base ,QColor (25 ,25 ,25 ))
    palette .setColor (QPalette .ColorRole .AlternateBase ,QColor (53 ,53 ,53 ))
    palette .setColor (QPalette .ColorRole .ToolTipBase ,Qt .GlobalColor .white )
    palette .setColor (QPalette .ColorRole .ToolTipText ,Qt .GlobalColor .white )
    palette .setColor (QPalette .ColorRole .Text ,Qt .GlobalColor .white )
    palette .setColor (QPalette .ColorRole .Button ,QColor (53 ,53 ,53 ))
    palette .setColor (QPalette .ColorRole .ButtonText ,Qt .GlobalColor .white )
    palette .setColor (QPalette .ColorRole .BrightText ,Qt .GlobalColor .red )
    palette .setColor (QPalette .ColorRole .Link ,QColor (42 ,130 ,218 ))
    palette .setColor (QPalette .ColorRole .Highlight ,QColor (42 ,130 ,218 ))
    palette .setColor (QPalette .ColorRole .HighlightedText ,Qt .GlobalColor .black )
    app .setPalette (palette )

    window =SDCombineDatasets ()
    window .show ()
    sys .exit (app .exec ())