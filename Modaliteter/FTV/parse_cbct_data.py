import numpy as np
from pathlib import Path
import dicom_image_tools as dit


# folder 
dpath = Path()

data = dit.import_dicom_from_folder(folder=dpath)

#ori_axial_morita = '[0.000000, 1.000000, 0.000000, 0.000000, 0.000000, -1.000000]'

def get_serie_ssm_data_from_morita_dicom_files(serie):
    res = dict()
    
    common_data = serie.CompleteMetadata[0]
    nr_images_in_stack = int(common_data.ImagesInAcquisition)
    
    # patient birth date yyyymmdd
    res["birth_date"] = str(common_data.PatientBirthDate)
    #DAP in mGycm2
    res["DAP"] = float(common_data.ImageAndFluoroscopyAreaDoseProduct)
    res["CTDIvol"] = common_data.CTDIvol
    res["sex"] = common_data.PatientSex
    res["study_description"] = common_data.StudyDescription

    comment = common_data.ImageComments
    tmp1 = comment.split("PixelSpacing")
    tmp2 = tmp1[0].split("VOLUME_RADIUS:")
    # radius in mm
    res["stack_radius"] = float(tmp2[1])




    for image in serie.CompleteMetadata:        
        instance_nr = int(image.InstanceNumber)
        if instance_nr == 1:
            pos_start = image.ImagePositionPatient
        
        if instance_nr == nr_images_in_stack:
            pos_stop = image.ImagePositionPatient
        

    a = 1
    # stack height im mm
    res["stack_height"] = abs(float(pos_start[2]) - float(pos_stop[2]))

    a=1

for serie in data[study_id].Series:
    serie.import_image_volume()
    
    res = get_serie_ssm_data_from_morita_dicom_files(serie)
























    #for image in serie.CompleteMetadata:
    #    nr_images_in_stack = int(image.ImagesInAcquisition)
    #    a=1
# sort out axial stack
#print(len(data[study_id].Series))
#for serie in data[study_id].Series:
#    orientation = serie.CompleteMetadata[0].ImageOrientationPatient
#    if str(orientation) != ori_axial_morita:
#        data[study_id].Series.remove(serie)
        
        #print(orientation)


# data[study_id].Series[0].import_image_volume()
# data[study_id].Series[0].CompleteMetadata[0].ImageOrientationPatient


print('hello')


# Ax, Ay, Az, Bx, By, Bz
# +0 +1 +0 +0 +0 -1 ? 

# +1 +0 +0 +0 +0 -1

# +1 +0 +0 +0 +1 +0 # AXIAL
 
