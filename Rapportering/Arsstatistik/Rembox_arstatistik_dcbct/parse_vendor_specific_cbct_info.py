import numpy as np
from datetime import datetime

def get_serie_ssm_data_from_morita_dicom_files(serie, alignment, age_lim=16):
    res = dict()
    
    common_data = serie.CompleteMetadata[0]
    
    # patient birth date yyyymmdd
    birth_date = datetime.strptime(str(common_data.PatientBirthDate), '%Y%m%d')
    study_date = datetime.strptime(str(common_data.StudyDate), '%Y%m%d')

    age_at_study = study_date - birth_date
    age_at_study_years = int(age_at_study.days/(365))
    res["name"] = str(common_data.PatientName)
    res["birth_date"] = str(common_data.PatientBirthDate)
    res["pat_age"] = age_at_study_years
    res["in_correct_age_limit"] = True if age_at_study_years >= age_lim else False 
    res["sex"] = common_data.PatientSex
    res["study_description"] = common_data.StudyDescription
    res["axial_alignment_percentage"] = np.round(100 * alignment, 2)

    if [0x0018, 0x115e] in common_data:
        #X-Ray dose, measured in dGy*cm*cm
        res["DAP"] = float(common_data.ImageAndFluoroscopyAreaDoseProduct)

    if [0x0020, 0x4000] in common_data:
        comment = common_data.ImageComments
        tmp1 = comment.split("PixelSpacing")
        tmp2 = tmp1[0].split("VOLUME_RADIUS:")
        # radius in mm
        res["stack_radius"] = float(tmp2[1])

    # get instance numbers in stack    
    instance_nrs = [int(image.InstanceNumber) for image in serie.CompleteMetadata]
    
    for image in serie.CompleteMetadata:        
        instance_nr = int(image.InstanceNumber)
        if instance_nr == min(instance_nrs):
            pos_start = image.ImagePositionPatient
        
        if instance_nr == max(instance_nrs):
            pos_stop = image.ImagePositionPatient
        
    # stack height im mm
    res["stack_height"] = abs(float(pos_start[2]) - float(pos_stop[2]))

    return res


def get_serie_ssm_data_from_gendex_dicom_files(serie, alignment):
    res = dict()
    
    common_data = serie.CompleteMetadata[0]
    
    private_tag = str(common_data[0x000d, 0x1000].value)
    
    split = private_tag.split("Attribute name=")
    
    for i in range(len(split)):
        if "fov_width" in split[i]:
            fov_width = float(split[i].split(">")[1].split("<")[0])
        if "fov_height" in split[i]:
            fov_height = float(split[i].split(">")[1].split("<")[0])
        if "dose" in split[i]:
            dose = float(split[i].split(">")[1].split("<")[0])
        
    # patient birth date yyyymmdd
    res["birth_date"] = str(common_data.PatientBirthDate)
    #DAP in mGycm2
    res["dose"] = dose
    res["fov_width"] = fov_width
    res["fov_height"] = fov_height
    res["sex"] = common_data.PatientSex
    res["study_description"] = common_data.StudyDescription
    res["axial_alignment_percentage"] = np.round(100 * alignment, 2)
    
    # get instance numbers in stack    
    instance_nrs = [int(image.InstanceNumber) for image in serie.CompleteMetadata]
    
    for image in serie.CompleteMetadata:        
        instance_nr = int(image.InstanceNumber)
        if instance_nr == min(instance_nrs):
            pos_start = image.ImagePositionPatient
        
        if instance_nr == max(instance_nrs):
            pos_stop = image.ImagePositionPatient
        
    # stack height im mm
    res["stack_height"] = abs(float(pos_start[2]) - float(pos_stop[2]))

    return res
