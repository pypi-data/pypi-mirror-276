import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),"dicom_standard_scrapping"))
import pydicom.multival
import pydicom.valuerep
import pandas as pd
import numpy as np
import pydicom
from pydicom.pixel_data_handlers import apply_rescale
from pathlib import Path
from typing import Union
from typing import Optional
from datetime import datetime
import logging
import copy
from .utils import *
import nibabel as nib
import inspect
from PyDicomGrouping.dicom_standard_scrapping.webscraping import DicomStandardTemplate
from PyDicomGrouping.dicom_standard_scrapping.DicomStandardEnums import DicomStandardTreeNode, DicomModuleItem, DicomAttributeItem, IODModuleUsage, DicomTagType
from alive_progress import alive_bar,alive_it
from typing import List
import shutil

def dicom_grouping(project_path: Union[str, Path,os.PathLike],
                     data_root_path: Union[str, Path, os.PathLike],
                     save_path: Union[str, Path, os.PathLike],
                     survey_excel_path: Union[str, Path, os.PathLike] = None,
                     survey_log_path: Union[str, Path, os.PathLike] = None,
                     remove_original_cache: bool = False,           # break-point
                     IODFilters: List = None,
                     ignore_duplicated: bool = True):
    # PyDicomGroupingEngine
    # data_root_path:
    # dataformat requirement:
    #   - PatientIDs
    #       - MRIScans
    #           - Sequences [i.e. seperated or mixed]
    #
    #
    # if survey_excel_path is not specified, we use the default instead.
    output_log_dir = os.path.join(project_path, 'logs')
    output_cache_dir = os.path.join(project_path, 'CacheFiles')
    survey_excel_dir = os.path.join(project_path, 'Survey_excels')
    studies_cache_path = os.path.join(output_cache_dir,'Caches_' + os.path.basename(data_root_path) + '.pkl')
    if not os.path.exists(output_log_dir):
        os.makedirs(output_log_dir)
    if not os.path.exists(output_cache_dir):
        os.makedirs(output_cache_dir)
    if not os.path.exists(survey_excel_dir):
        os.makedirs(survey_excel_dir)
    if not survey_excel_path:
        survey_excel_path = os.path.join(survey_excel_dir,'Survey_Excel_' + datetime.now().strftime(r'%Y_%m_%d') + '_' +os.path.basename(data_root_path)+'.xlsx')
    # if survey_log_path is not specified, we use the default instead
    if not survey_log_path:
        survey_log_path = os.path.join(output_log_dir,'Survey_log_'+datetime.now().strftime(r'%Y_%m_%d') + '_' +os.path.basename(data_root_path)+'.log')
    if remove_original_cache:
        if os.path.isfile(survey_log_path):
            os.remove(survey_log_path)
        if os.path.isfile(survey_excel_path):
            os.remove(survey_excel_path)
        if os.path.isfile(studies_cache_path):
            os.remove(studies_cache_path)
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logging.basicConfig(filename=survey_log_path,
                       level = logging.INFO,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                       datefmt='%m-%d-%Y %H:%M:%S'
                       )
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    #reload studies_cache_path
    if not os.path.exists(studies_cache_path):
        studies_cache = {}
        os.makedirs(os.path.dirname(studies_cache_path),exist_ok=True)
        pickle_dump(studies_cache,studies_cache_path)
    else:
        studies_cache = pickle_load(studies_cache_path)
    #init dicom template caches
    dicomStandardTemplateCache = DicomStandardTemplate()
    if not IODFilters:
        IODFilters = ["MR Image IOD", "CT Image IOD"] # default for MR
    # In case of mixed study for different patients or different study from same patienr, coarse group is necessary
    #-----------------------------
    #Exec PyDicomCoarseGrouping
    #-----------------------------
    studies = []
    dataloader_cache = dict()
    dataloader_cachefile_path = os.path.join(output_cache_dir, 'dataloader_cache_' + os.path.basename(data_root_path) + '.pkl')
    if not os.path.exists(dataloader_cachefile_path):
        dicoms = []
        for home, dirs, files in os.walk(data_root_path):
            for filename in files:
                dicoms.append(os.path.join(home,filename))
        with alive_bar(len(dicoms)) as bar:
            for idx, dicom in enumerate(dicoms):
                PyDicomCoarseGrouping(dicom_path = dicom,
                                    dataloader_cache = dataloader_cache)
                bar()
        pickle_dump(dataloader_cache, dataloader_cachefile_path)
    else:
        #data complete check
        dataloader_cache = pickle_load(dataloader_cachefile_path)
        # if len([val for key,val in ])
    studies = list(dataloader_cache.keys())
    if ignore_duplicated:
        studies = [item for item in list(dataloader_cache.keys()) if item not in studies_cache.keys()]
    logger.info(f"{len(list(dataloader_cache.keys()))} studies were found, {len(studies)} studies would be processed.")    
    #Main
    for studyInsUID in sorted(studies):
        logger.info(f'**************Processing study data-set with StudyInstanseUID:{studyInsUID}***************************')
        logger.info(f'//=============================Start==================================')
        dicoms = dataloader_cache[studyInsUID]
        study_cache = dict()
        raw_study_dataset = {}    #patient_dataset for one patient
        proc_study_dataset = {}
        raw_dicoms = {}
        logger.info(f"***************{len(dicoms)} dicom files are found, start loading dicoms**********************")
        dicoms_bar = alive_it(dicoms)
        for dicom in dicoms_bar:
            dicoms_bar.text("Processing dicom: " + os.path.basename(dicom))
            if not PyDicomExtractingEngine_main(dicom_path = dicom,
                                                raw_dicoms = raw_dicoms,
                                                study_dataset = raw_study_dataset,
                                                dicomStandardTemplateCache = dicomStandardTemplateCache,
                                                IODFilters = IODFilters):
                logger.warning(f"Error in de-coding dicom {dicom}.")
        logger.info("***************loading dicoms finished**********************")
        # raw_study_dataset = pickle_load("pydicom_test.pkl")
        # dicomStandardTemplateCache = pickle_load("dicomStandardTemplateCache.pkl")
        # proc_study_dataset = pickle_load("proc_study_dataset")
        logger.info(f"***************{len(raw_study_dataset.keys())} dicom series are found, start stacking dicoms series**********************")
        PyDicomGroupingEngine_main(raw_study_dataset = raw_study_dataset,
                                    proc_study_dataset = proc_study_dataset)
        logger.info(f"***************dicom series stacking finished**********************")
        # pickle_dump(raw_study_dataset, "pydicom_test.pkl")
        # pickle_dump(dicomStandardTemplateCache, "dicomStandardTemplateCache.pkl")
        # pickle_dump(raw_dicoms, "raw_dicoms.pkl")
        # pickle_dump(proc_study_dataset, "proc_study_dataset")
        #after patient-MRI scan data processing complete, start data storage engine
        # #TODO: both raw dicom and splited nifti should be stored.
        PyDicomGroupingSummary_main(proc_study_dataset=proc_study_dataset,
                                    study_cache = study_cache)
        logger.info(f"***************{len(proc_study_dataset.keys())} completed dicom series are found, start saving dicoms series**********************")
        PyDicomStorageEngine_main(proc_study_dataset=proc_study_dataset,
                                  raw_dicoms = raw_dicoms,
                                  save_path = os.path.join(save_path, studyInsUID))
        logger.info(f"***************completed dicom series saving finished**********************")
        study_cache["study_save_path"] = save_path
        #update studies_cache for every MRIstudies
        studies_cache = pickle_load(studies_cache_path)
        if studyInsUID not in studies_cache.keys():
            studies_cache[studyInsUID] = study_cache
        else:
            logger.warning(f"Duplicated StudyInsUID was found in studies_cache, and the original study will be updated.")
            studies_cache[studyInsUID].update(study_cache)
        pickle_dump(studies_cache,studies_cache_path)

        aborted_sequences = []
        for key in raw_study_dataset.keys():
            if key not in proc_study_dataset.keys():
                aborted_sequences.append(key)
        logger.info(f'Processing finished in Study {studyInsUID}.')
        logger.info(f'//*****************************Summary********************************')
        logger.info(f'{len(raw_study_dataset.keys())} sequences are extracted and {len(aborted_sequences)} sequences are aborted.')
        for sequence in aborted_sequences:
            logger.warning(f'{sequence} is aborted.')
        logger.info(f'//=============================End====================================')

    #save survey dict to excel by pd
    pd.DataFrame(mergeParsDict([studies_cache[key]["study_pars"] for key in studies_cache.keys()], None, False)).to_excel(survey_excel_path)
    print('dirty trick')


def PyDicomCoarseGrouping(dicom_path: Union[str, Path, os.PathLike],
                          dataloader_cache: dict):
    #function used for coarsely grouping dicom files according to studyUID
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        StudyInstanceUID = pydicom.dcmread(dicom_path, specific_tags = [[0x0020,0x000D]])[0x0020,0x000D].value # this tag is consistant in all CIODs
        if StudyInstanceUID not in dataloader_cache.keys():
            dataloader_cache[StudyInstanceUID] = []
        else:
            dataloader_cache[StudyInstanceUID].append(dicom_path)
    except:
        logger.warning(f'Error occured in processing {dicom_path}.')
    
def PyDicomSurvey(dcmdata,
                  dicomStandardDict: dict,
                  dicomStandardTemplateCache: DicomStandardTemplate = None,
                  IODFilters: List = None):
    #function used for survey dcmdata according to dicomStandardTemplate
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        if not dicomStandardTemplateCache:
            dicomStandardTemplateCache = DicomStandardTemplate()
        FMIHeader_dict = dict()
        dicomStandardTemplateCache.getFMIHeaderTreeNode().dicomSurvey(FMIHeader_dict,dcmdata.file_meta)
        SOPClassUID = FMIHeader_dict['FileMetaInformation']['MediaStorageSOPClassUID']
        if (IODFilters and dicomStandardTemplateCache.getIODSpecificationByMediaStorageSOPClassUID(SOPClassUID) in IODFilters) or\
            not IODFilters:
            #check if DicomStandard is alreadly load in caches
            if SOPClassUID not in dicomStandardTemplateCache.SOPClassUIDList:
                dicomStandardTemplateCache.loadBySOPClassUID(SOPClassUID)
            #extract dicom pars
            dicomStandardTemplateCache.getIODTreeNodeByMediaStorageSOPClassUID(SOPClassUID).dicomSurvey(dicomStandardDict, dcmdata)
            return True
        else:
            return False
    except:
        logger.warning(f"Error occured in PyDicomSurvey.")
        return False

def PyDicomExtractingEngine_main(dicom_path: Union[str, Path, os.PathLike],
                                 raw_dicoms: dict,
                                 study_dataset: dict,
                                 dicomStandardTemplateCache: DicomStandardTemplate,
                                 IODFilters: List = None):
    # dicoms-in -> dictionary out
    # for sequence_storage_mode == seperate, the num_slice is inferenced from dicom files number
    #
    # if patientID or RISID is not given, use the information from dicom, otherwise, use the given one
    # print('processing dicom files:' + os.path.basename(dicom_path))
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        dicomStandardDict = dict()
        #dicom filetype check
        try:
            dcmdata = pydicom.dcmread(dicom_path)
        except:
            logger.error(f"Error in decoding dicom file {dicom_path}, we skip this dicom file.")
            raise ValueError
        # check if pixel array is existed.
        try:
            pixel_array = dcmdata.pixel_array
        except:
            logger.error(f'Can not load pixel array from dicom file, we skip this dicom file.')
            raise ValueError
        #Mapping dcmdata Tags to standard dicom tag dict
        if not PyDicomSurvey(dcmdata = dcmdata,
                               dicomStandardDict = dicomStandardDict,
                               dicomStandardTemplateCache = dicomStandardTemplateCache,
                               IODFilters = IODFilters):
            #if dicom file is not decoded correctly, skip
            raise ValueError
        CIODKeyWord = list(dicomStandardDict.keys())[0]
        #remove pixel data
        if dicomStandardDict[CIODKeyWord]["ImagePixel"]["PixelData"] != "":
            dicomStandardDict[CIODKeyWord]["ImagePixel"]["PixelData"] = ""
        manufacturer = None
        protocol = None
        if CIODKeyWord == 'MRImage':
            #In CIOD of MRImage, we make manufacturer check first
            manufacturer = dicomStandardDict[CIODKeyWord]['GeneralEquipment']['Manufacturer']
            if manufacturer and 'GE' not in manufacturer and 'Philips' not in manufacturer and 'UIH' not in manufacturer and 'SIEMENS' not in manufacturer:
                logger.warning(f'un-supported manufacturer {manufacturer}, dicom file is skipped.')
                raise ValueError
        elif CIODKeyWord == 'CTImage':
            #In CIOD of CTImage, we make manufacturer check first
            manufacturer = dicomStandardDict[CIODKeyWord]['GeneralEquipment']['Manufacturer']
            if manufacturer and 'GE' not in manufacturer and 'Philips' not in manufacturer and 'UIH' not in manufacturer and 'SIEMENS' not in manufacturer:
                logger.warning(f'un-supported manufacturer {manufacturer}, dicom file is skipped.')
                raise ValueError
        try:
            #get protocol
            series_date = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesDate"]
            series_time = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesTime"]
            series_time_str = datetime.strptime(series_date+series_time[:6],r'%Y%m%d%H%M%S').strftime(r'%Y_%m_%d_%H_%M_%S')
            series_desc = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
            if series_desc and series_desc != '':
                protocol = series_time_str + '_' + series_desc.replace(' ','').replace('(','_').replace(')','').replace('\\','_').replace('/','_').replace(':','_').replace('<','_').replace('>','_').replace('^','_').replace('-','_').replace('*','_').replace('?','').replace("'",'')
        except:
            logger.warning(f"Extracting series time error, we use SeriesInstanceUID instead.")
            protocol = dicomStandardDict[CIODKeyWord]["GeneralSeries"]["SeriesInstanceUID"]
        #extract Vendor specific Module
        VerdorPrivateTagDict = dict()
        VendorPrivateTreeNode = globals()["_".join(["retrieveVendorPrivateTreeNode",CIODKeyWord])](manufacturer = manufacturer)
        VendorPrivateTreeNode.dicomSurvey(VerdorPrivateTagDict, dcmdata)
        dicomStandardDict[CIODKeyWord][VendorPrivateTreeNode.keyWord()] = VerdorPrivateTagDict[VendorPrivateTreeNode.keyWord()]
        RescaleSlope = float(VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleSlope"]) if VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleSlope"] != "" else 1.0
        RescaleIntercept = float(VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleIntercept"]) if VerdorPrivateTagDict[list(VerdorPrivateTagDict.keys())[0]]["RescaleIntercept"] != "" else 0.0
        pixel_array = dcmdata.pixel_array * RescaleSlope + RescaleIntercept
        #update RescaleSlope and RescaleIntercept
        if RescaleSlope != VerdorPrivateTagDict[VendorPrivateTreeNode.keyWord()]["RescaleSlope"]:
            dicomStandardDict[CIODKeyWord][VendorPrivateTreeNode.keyWord()]["RescaleSlope"] = RescaleSlope
        if RescaleIntercept != VerdorPrivateTagDict[VendorPrivateTreeNode.keyWord()]["RescaleIntercept"]:
            dicomStandardDict[CIODKeyWord][VendorPrivateTreeNode.keyWord()]["RescaleIntercept"] = RescaleIntercept
        #save data and parameters to study dataset
        if protocol not in study_dataset.keys():
            study_dataset[protocol] = dict()
            raw_dicoms[protocol] = []
            study_dataset[protocol]["data"] = []
            study_dataset[protocol]["pars"] = []
            study_dataset[protocol]["data"].append(pixel_array)
            study_dataset[protocol]["pars"].append(dicomStandardDict)
        else:
            study_dataset[protocol]["data"].append(pixel_array)
            study_dataset[protocol]["pars"].append(dicomStandardDict)
            raw_dicoms[protocol].append((dicom_path, dicomStandardDict[CIODKeyWord]["SOPCommon"]["SOPInstanceUID"]))
        # make-sure everything has been processed correctly
        return True
    except:
        return False

def PyDicomGroupingEngine_main(raw_study_dataset: dict,
                               proc_study_dataset: dict):
    # PyDoGE: dicom-in, dictionary out
    # for sequence_storage_mode == seperate, the num_slice is inferenced from dicom files number
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    logger.info(f"{len(raw_study_dataset.keys())} sequences found.")
    
    bar = alive_it(sorted(raw_study_dataset.keys()))
    for idx, protocol in enumerate(bar):
        bar.text("Stacking series: " + protocol)
        #consistent CIOD class check, all the image in one sequence should be same
        CIODKeyWords = [list(item.keys())[0] for item in raw_study_dataset[protocol]['pars']]
        unique_CIODKeyWord = np.unique(CIODKeyWords)
        if len(unique_CIODKeyWord) > 1:
            logger.error(f"more than one CIOD was found in {idx}th protocol: {protocol}")
            continue
        CIODKeyWord = unique_CIODKeyWord[0]
        logger.info(f"Stacking the {idx}-th sequence: {protocol}")
        if not globals()["_".join(["PyDicomGroupingEngine",CIODKeyWord])](study_dataset_dict = raw_study_dataset,
                                                                protocol = protocol,
                                                                proc_study_dataset = proc_study_dataset):
            logger.error(f"Error in packing procotol {idx}th protocol: {protocol}")
            continue

        
        # sorted_dict = dict()
        # #sort by instance number or acq time
        # instance_numbers = [item[list(item.keys())[0]]["GeneralImage"]["InstanceNumber"] for item in study_dataset_raw[protocol]['pars']]
        # idx_list = np.argsort(instance_numbers)
        # sorted_dict['pars'] = [study_dataset_raw[protocol]['pars'][idx] for idx in idx_list]
        # sorted_dict['data'] = [study_dataset_raw[protocol]['data'][idx] for idx in idx_list]

        
        # try:
        #     image_positions = [item[list(item.keys())[0]]["ImagePlane"]["ImagePositionPatient"] for item in sorted_dict['pars']]
        #     image_orientations = [item[list(item.keys())[0]]["ImagePlane"]["ImageOrientationPatient"] for item in sorted_dict['pars']]
        #     slice_locations = [item[list(item.keys())[0]]["ImagePlane"]["SliceLocation"] for item in sorted_dict['pars']]
        # except:
        #     logger.warning(f'Exception occured in {protocol}, we skip this series.')
        #     continue
        # #################################
        # #
        # # Slice orientation check
        # #
        # #################################
        # unique_image_orientation, slice_packages_indexs = extractUniqueSliceOrientation(image_orientations)
        # for slice_packages_index, slice_package_indexs in enumerate(slice_packages_indexs):
        #     #retrieve unique slice number
        #     unique_image_position = []
        #     unique_slice_location = []
        #     #get unique slice_location and image position
        #     for slice_index in slice_package_indexs:
        #         if image_positions[slice_index] not in unique_image_position:
        #             unique_image_position.append(image_positions[slice_index])
        #         if slice_locations[slice_index] not in unique_slice_location:
        #             unique_slice_location.append(slice_locations[slice_index])
        #     #sorting image position
        #     ori_str, norm_vec = calc_image_ori(unique_image_orientation[slice_packages_index])
        #     slice_pos_dot_prod = [np.dot(image_position, norm_vec) for image_position in unique_image_position]
        #     unique_image_position, unique_slice_location, slice_pos_dot_prod = zip(*sorted(zip(unique_image_position,unique_slice_location, slice_pos_dot_prod), key = lambda x:x[2]))
        #     #unique slice gap check  ---> make sure continous slices
        #     slice_gaps = [item[list(item.keys())[0]]["ImagePlane"]["SpacingBetweenSlices"] for item in sorted_dict['pars']]
        #     diff_image_position = [np.sqrt(np.sum(np.square(np.array(unique_image_position[slice_id]) - np.array(unique_image_position[slice_id - 1])))) for slice_id in range(1, len(unique_image_position))]
        #     if len(np.unique(slice_gaps)) > 1:
        #         logger.warning(f"spacing between slices is expected to be same, we skip this series.")
        #         continue
        #     elif len(diff_image_position) > 1:
        #         if np.sum([(np.array(diff_image_position[slice_id]) - np.array(diff_image_position[slice_id - 1]))>1e-1 for slice_id in range(1, len(diff_image_position))]) > 0:
        #             logger.warning(f"spacing between slices is expected to be same, we skip this series.")
        #             continue
        #     num_slice = len(unique_slice_location)
        #     slice_package_pars['unique_slice_locations'] = unique_slice_location
        #     slice_package_pars['unique_image_positions'] = unique_image_position
        #     slice_package_pars['num_slices'] = len(slice_package_pars['unique_slice_locations'])
        #     if study_dataset_raw[protocol]['common_pars']['Modality'] == 'CT':
        #         #introduce fake modality_num and modality ID
        #         slice_package_pars['num_modality'] = 1
        #         slice_package_pars['num_temporal_position'] = 1
        #         for slice_index in slice_package_indexs:
        #             sorted_dict['pars'][slice_index]['modality_id'] = 0
        #             sorted_dict['pars'][slice_index]['temporal_position_idx'] = 0
        #     elif study_dataset_raw[protocol]['common_pars']['Modality'] == 'MR':
        #         #update modality_num and modality_idx
        #         if 'image_type' in slice_package_pars.keys():
        #             if 'ORIGINAL' in slice_package_pars['image_type'][0]:
        #                 #################################
        #                 #
        #                 #  Multi-echo routine scan, same data type
        #                 #
        #                 #################################
        #                 if 'echo_time' in diff_keys:
        #                     unique_echo_time = []
        #                     for slice_index in slice_package_indexs:
        #                         if sorted_dict['pars'][slice_index]['echo_time'] not in unique_echo_time:
        #                             unique_echo_time.append(sorted_dict['pars'][slice_index]['echo_time'])
        #                     unique_echo_time = sorted(unique_echo_time)
        #                     #update T2map modality index
        #                     for slice_index in slice_package_indexs:
        #                         sorted_dict['pars'][slice_index]['modality_id'] = unique_echo_time.index(sorted_dict['pars'][slice_index]['echo_time'])
        #                     #update num_modality
        #                     slice_package_pars['unique_echo_time'] = unique_echo_time
        #                     slice_package_pars['num_modality'] = len(unique_echo_time)
        #             #################################
        #             #
        #             #  DWI scan
        #             #
        #             #################################
        #             if 'dwi_scan_flag' in slice_package_pars.keys():
        #                 if slice_package_pars['dwi_scan_flag']:
        #                     unique_dwi_pars = []
        #                     for slice_index in slice_package_indexs:
        #                         if  sorted_dict['pars'][slice_index]['dwi_pars'] not in unique_dwi_pars:
        #                             unique_dwi_pars.append(sorted_dict['pars'][slice_index]['dwi_pars'])
        #                     if len(unique_dwi_pars) > 1:
        #                         #update T1map modality index
        #                         if isinstance(unique_dwi_pars[0]['b_value'],pydicom.multival.MultiValue):
        #                             unique_dwi_pars = sorted(unique_dwi_pars,key = lambda x:x['b_value'][0])
        #                         elif isinstance(unique_dwi_pars[0]['b_value'], float):
        #                             unique_dwi_pars = sorted(unique_dwi_pars,key = lambda x:x['b_value'])
        #                         for slice_index in slice_package_indexs:
        #                             sorted_dict['pars'][slice_index]['modality_id'] = unique_dwi_pars.index(sorted_dict['pars'][slice_index]['dwi_pars'])
        #                         #update num_modality
        #                         slice_package_pars['unique_dwi_modality'] = unique_dwi_pars
        #                         slice_package_pars['num_modality'] = len(unique_dwi_pars)
        #                     else:
        #                         slice_package_pars['dwi_scan_flag'] = False #close the dwi flag
        #         elif 'image_type' in diff_keys:
        #             if 'Philips' in study_dataset_raw[protocol]['common_pars']['manufacturer']:
        #                 unique_image_type = []
        #                 for slice_index in slice_package_indexs:
        #                         if sorted_dict['pars'][slice_index]['image_type'][0] not in unique_image_type:
        #                             unique_image_type.append(sorted_dict['pars'][slice_index]['image_type'][0])
        #                 if 'ORIGINAL' in unique_image_type and 'DERIVED' in unique_image_type:
        #                     #multi echo check
        #                     #################################
        #                     #
        #                     #  Philips multi-echo or quant mapping
        #                     #
        #                     #################################
        #                     if 'echo_time' in diff_keys:
        #                         unique_image_modality = []
        #                         for slice_index in slice_package_indexs:
        #                             if sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] not in unique_image_modality:
        #                                 unique_image_modality.append(sorted_dict['pars'][slice_index]['PhilipsMRIImageType'])
        #                         #T2 mapping sequence
        #                         if ('T2' in unique_image_modality or 
        #                             'R2' in unique_image_modality or
        #                             'T2_STAR' in unique_image_modality or
        #                             'R2_STAR' in unique_image_modality) and 'M' in unique_image_modality:
        #                             unique_T2map_time = []
        #                             for slice_index in slice_package_indexs:
        #                                 if (sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] + '_echo_time_' + str(sorted_dict['pars'][slice_index]['echo_time'])) not in unique_T2map_time:
        #                                     unique_T2map_time.append((sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] + '_echo_time_' + str(sorted_dict['pars'][slice_index]['echo_time'])))
        #                             slice_package_pars['T2Mapping_flag'] = True
        #                             unique_T2map_time = sorted(unique_T2map_time)
        #                             #update T2map modality index
        #                             for slice_index in slice_package_indexs:
        #                                 sorted_dict['pars'][slice_index]['modality_id'] = unique_T2map_time.index((sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] + '_echo_time_' + str(sorted_dict['pars'][slice_index]['echo_time'])))
        #                             #update num_modality
        #                             slice_package_pars['unique_T2map_modality'] = unique_T2map_time
        #                             slice_package_pars['num_modality'] = len(unique_T2map_time)
        #                     #################################
        #                     #
        #                     #  Philips MR-T1 mapping
        #                     #
        #                     #################################
        #                     if 'T1Mapping_flag' in slice_package_pars.keys():
        #                         if slice_package_pars['T1Mapping_flag']:
        #                             unique_T1map_modality = []
        #                             for slice_index in slice_package_indexs:
        #                                 if (sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] + '_' + str(sorted_dict['pars'][slice_index]['MOLLI_InvTimeID'])) not in unique_T1map_modality:
        #                                     unique_T1map_modality.append((sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] + '_' + str(sorted_dict['pars'][slice_index]['MOLLI_InvTimeID'])))
        #                             #update T1map modality index
        #                             unique_T1map_modality = sorted(unique_T1map_modality)
        #                             for slice_index in slice_package_indexs:
        #                                 sorted_dict['pars'][slice_index]['modality_id'] = unique_T1map_modality.index(sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] + '_' + str(sorted_dict['pars'][slice_index]['MOLLI_InvTimeID']))
        #                             #update num_modality
        #                             slice_package_pars['unique_T1map_modality'] = unique_T1map_modality
        #                             slice_package_pars['num_modality'] = len(unique_T1map_modality)        
        #                 elif len(unique_image_type) == 1 and 'DERIVED' in unique_image_type:
        #                     #################################
        #                     #
        #                     #  Philips Dixon quant
        #                     #
        #                     #################################
        #                     PhilipsDixonModalityList = ['W','F','IP','OP','T2_STAR','R2_STAR','FF']
        #                     dixon_flag = False
        #                     unique_dixon_modality = []
        #                     for slice_index in slice_package_indexs:
        #                         if sorted_dict['pars'][slice_index]['PhilipsMRIImageType'] not in unique_dixon_modality:
        #                             unique_dixon_modality.append(sorted_dict['pars'][slice_index]['PhilipsMRIImageType'])
        #                     if np.sum([item in PhilipsDixonModalityList for item in unique_dixon_modality]) > 0:
        #                         sorted_unique_modality = []
        #                         for modality in PhilipsDixonModalityList:
        #                             if modality in unique_dixon_modality:
        #                                 sorted_unique_modality.append(modality)
        #                         #update Dixon modality index
        #                         if len(sorted_unique_modality) > 1:
        #                             for slice_index in slice_package_indexs:
        #                                 sorted_dict['pars'][slice_index]['modality_id'] = sorted_unique_modality.index(sorted_dict['pars'][slice_index]['PhilipsMRIImageType'])
        #                             #update num_modality
        #                             slice_package_pars['unique_Dixon_modality'] = sorted_unique_modality
        #                             slice_package_pars['num_modality'] = len(sorted_unique_modality)
        #                             slice_package_pars['dixon_scan_flag'] = True
        #     #shrink dimension to temporal position
        #     if len(slice_package_indexs) != (slice_package_pars['num_slices'] * slice_package_pars['num_modality'] * slice_package_pars['num_temporal_position']):
        #         if len(slice_package_indexs) % (slice_package_pars['num_slices'] * slice_package_pars['num_modality']) == 0:
        #             reshape_flag = True
        #             slice_package_pars['num_temporal_position'] = int(len(slice_package_indexs) / (slice_package_pars['num_slices'] * slice_package_pars['num_modality']))
        #         else:
        #             #with some missed slice in GE
        #             tolerate_missed_slice = int(missed_slice_percent * slice_package_pars['num_slices']) * 2
        #             under_limit_tempo_pos = len(slice_package_indexs) / (slice_package_pars['num_slices'] * slice_package_pars['num_modality'])
        #             if np.ceil(under_limit_tempo_pos) == np.floor((tolerate_missed_slice * slice_package_pars['num_modality'] + len(slice_package_indexs)) / (slice_package_pars['num_slices'] * slice_package_pars['num_modality'])):
        #                 missed_slice_flag = True
        #                 slice_package_pars['num_temporal_position'] = int(np.ceil(len(slice_package_indexs) / (slice_package_pars['num_slices'] * slice_package_pars['num_modality'])))
        #             else:
        #                 logger.warning(f'dataset is incomplete in Patient dataset: {patientID}-{RISID}, slice-package{slice_packages_index}.')
        #                 continue
        #     rows = slice_package_pars['rows']
        #     cols = slice_package_pars['cols']
        #     num_slices = slice_package_pars['num_slices']
        #     num_modality = slice_package_pars['num_modality']
        #     num_temporal_position = slice_package_pars['num_temporal_position']
        #     if slice_package_pars['PhotometricInterp'] == 'MONOCHROME2':
        #         slice_package_data = np.zeros((rows, cols, num_slices, num_modality, num_temporal_position)) # we force the data should be 5d
        #         slice_package_data_marker = np.ones((num_slices,num_modality,num_temporal_position))
        #     elif slice_package_pars['PhotometricInterp'] == 'RGB':
        #         slice_package_data = np.zeros((rows, cols, 3, num_slices, num_modality, num_temporal_position)) # 3 for RGB, 6-d here
        #         slice_package_data_marker = np.ones((num_slices,num_modality,num_temporal_position))               
        #     #Initialization of diff_dict
        #     if diff_keys:
        #         diff_dict = dict()
        #         for key in diff_keys:
        #             diff_dict[key] = [[['' for _ in range(num_temporal_position)] for _ in range(num_modality)] for _ in range(num_slices)]
        #     for slice_index in slice_package_indexs:
        #         slice_id = slice_package_pars['unique_slice_locations'].index(float(sorted_dict['pars'][slice_index]['slice_location']))
        #         modality_id = sorted_dict['pars'][slice_index]['modality_id']
        #         if not reshape_flag and not missed_slice_flag:
        #             temporal_position_idx = sorted_dict['pars'][slice_index]['temporal_position_idx']
        #         else:
        #             nonzeros_idxs = np.nonzero(slice_package_data_marker[slice_id,modality_id,:])[0]
        #             if nonzeros_idxs.size > 0:
        #                 temporal_position_idx = nonzeros_idxs[0]
        #             else:
        #                 logger.warning(f'dataset is already filled in Patient dataset: {patientID}-{RISID}, slice-package{slice_packages_index}, we ignore instance id{slice_index}.')
        #                 continue
        #         if slice_package_data_marker[slice_id,modality_id,temporal_position_idx] == 1:
        #             slice_package_data_marker[slice_id,modality_id,temporal_position_idx] = 0
        #             slice_package_data[...,slice_id,modality_id,temporal_position_idx] = sorted_dict['data'][slice_index]
        #             if diff_keys:
        #                 for key in diff_keys:
        #                     diff_dict[key][slice_id][modality_id][temporal_position_idx] = sorted_dict['pars'][slice_index][key]
        #         else:
        #             logger.warning(f'slice-modality-temporl:{slice_id}-{modality_id}-{temporal_position_idx} has already filled.')
        #             continue
        #     if not missed_slice_flag:
        #         if np.sum(slice_package_data_marker) > 0:
        #             logger.warning(f'dataset:{patientID}-{RISID}-{protocol} is incomplete.')
        #             continue
        #     else:
        #         if np.sum(slice_package_data_marker[int(tolerate_missed_slice / 2) : int(slice_package_data_marker.shape[0] - tolerate_missed_slice/2), :, :]) > 0:
        #             logger.warning(f'dataset:{patientID}-{RISID}-{protocol} is incomplete.')
        #             missed_slice_id = np.where(slice_package_data_marker[int(tolerate_missed_slice / 2) : int(slice_package_data_marker.shape[0] - tolerate_missed_slice/2), :, :] == 1)
        #             for i in range(len(missed_slice_id[0])):
        #                 logger.warning(f'Slice ID: {missed_slice_id[0][i]}, Modality ID: {missed_slice_id[1][i]}, temporal ID: {missed_slice_id[2][i]} is missed.')
        #             continue
        #     #Merge diff_dict
        #     if diff_keys:
        #         slice_package_pars.update(diff_dict)
        #     slice_package['pars'] = slice_package_pars
        #     slice_package['data'] = slice_package_data
        #     slice_package['data_marker'] = slice_package_data_marker
        #     slice_packages.append(slice_package)
        # study_dataset[protocol] = dict()
        # study_dataset[protocol]['slice_packages'] = slice_packages
        # study_dataset[protocol]['common_pars'] = study_dataset_raw[protocol]['common_pars']

def PyDicomGroupingEngine_MRImage(study_dataset_dict: dict,
                                  protocol: str,
                                  proc_study_dataset: dict):
        try:
            CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
            logger = logging.getLogger(inspect.currentframe().f_code.co_name)
            sorted_dict = dict()
            instance_numbers = [item[CIODKeyWord]["GeneralImage"]["InstanceNumber"] for item in study_dataset_dict[protocol]['pars']]
            idx_list = np.argsort(instance_numbers)
            sorted_dict['pars'] = [study_dataset_dict[protocol]['pars'][idx] for idx in idx_list]
            sorted_dict['data'] = [study_dataset_dict[protocol]['data'][idx] for idx in idx_list]
            image_orientations = [item[CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] for item in sorted_dict['pars']]
            #################################
            #
            # Slice orientation check
            #
            #################################
            unique_image_orientation, slice_packages_indexs = extractUniqueSliceOrientation(image_orientations)
            slice_packages = []
            for slice_packages_index, slice_package_indexs in enumerate(slice_packages_indexs):
                slice_package = dict()
                parsDicts = [sorted_dict['pars'][index] for index in slice_package_indexs]
                dataList = [sorted_dict['data'][index] for index in slice_package_indexs]
                merged_pars_dict = mergeParsDict(parsDicts)
                #ImagePositionPatient and SliceLocation are mandatory 
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"] == "":
                    raise ValueError
                #retrieve unique slice position and location
                if isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], List):
                    unique_image_position = [list(item) for item in dict.fromkeys(tuple(item) for item in merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"])]
                elif isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], pydicom.multival.MultiValue):
                    unique_image_position = [merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]]           
                #sorting image position
                ori_str, norm_vec = calc_image_ori(unique_image_orientation[slice_packages_index])
                unique_slice_location = [np.dot(image_position, norm_vec) for image_position in unique_image_position]
                unique_image_position, unique_slice_location = zip(*sorted(zip(unique_image_position, unique_slice_location), key = lambda x:x[1]))
                #unique slice gap check  ---> make sure continous slices
                slice_gaps = [item[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] for item in parsDicts]
                diff_image_position = [np.sqrt(np.sum(np.square(np.array(unique_image_position[slice_id]) - np.array(unique_image_position[slice_id - 1])))) for slice_id in range(1, len(unique_image_position))]
                if len(np.unique(slice_gaps)) > 1:
                    logger.warning(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                    continue
                elif len(diff_image_position) > 1:
                    if np.sum([(np.array(diff_image_position[slice_id]) - np.array(diff_image_position[slice_id - 1]))>1e-1 for slice_id in range(1, len(diff_image_position))]) > 0:
                        logger.warning(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                        continue
                #Spacing between slice check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] == "":
                    if len(unique_slice_location) > 1:
                        #update parsDict
                        for parsDict in parsDicts:
                            parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = np.mean(diff_image_position)
                    elif len(unique_slice_location) == 1:
                        if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] != "":
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] # use slice thickness
                        else:
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = 1 # default 1
                    logger.warning(f"Since empty SpacingBetweenSlices are found, we use the derived one instead.")
                #Slice Location check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceLocation"] == "":
                    for parsDict in parsDicts:
                        parsDict[CIODKeyWord]["ImagePlane"]["SliceLocation"] = np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)
                    logger.warning(f"Since empty SliceLocation are found, we use the derived one instead.")
                num_slice = len(unique_slice_location)
                num_modality = 1 #default value
                num_temporal_position = 1 #default value
                stackingOrders = []
                #unique row check
                Rows = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Rows"]
                Columns = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Columns"]
                PhotometricInterpretation = merged_pars_dict[CIODKeyWord]["ImagePixel"]["PhotometricInterpretation"]
                Manufacturer = merged_pars_dict[CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
                ImageTypes = merged_pars_dict[CIODKeyWord]["GeneralImage"]["ImageType"]
                if isinstance(Rows, List):
                    logger.warning(f"{protocol} length of unique row is larger than 1.")
                    continue
                if isinstance(Columns, List):
                    logger.warning(f"{protocol} length of unique column is larger than 1.")
                    continue
                if isinstance(PhotometricInterpretation, List):
                    logger.warning(f"{protocol} length of unique photometricInterp is larger than 1.")
                    continue
                if isinstance(Manufacturer, List):
                    logger.warning(f"{protocol} length of unique manufacturer is larger than 1.")
                    continue
                if np.mod(len(slice_package_indexs), num_slice) == 0:
                    if len(slice_package_indexs)/num_slice == 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        #stacking by image position, in case of one imagetype and 1 modality, one repetation
                        modality_idx = 0
                        temporal_position_index = 0
                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                            modality_idx, \
                                                temporal_position_index] for idx in slice_package_indexs]
                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        # if len()
                        #DWI?multi-echo?
                        if "Philips" in Manufacturer:
                            # ImageType check for DWI, same Philips ImageType has been found for raw DWI scan and Reg_DWI scan
                            if isinstance(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], list):
                                unique_BVal = sorted(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"])
                                num_modality = int(len(unique_BVal))
                                num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                                if not num_temporal_position.is_integer():
                                    logger.warning(f"{protocol} length of num_temporal_position is not integer.")
                                    continue
                                else:
                                    num_temporal_position = int(num_temporal_position)
                                    temporal_position_idx = 0
                                    for idx in slice_package_indexs:
                                        slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                        modality_idx = unique_BVal.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"])
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        if temp_stackingOrder not in stackingOrders:
                                            stackingOrders.append(temp_stackingOrder)
                                        else:
                                            temporal_position_idx = temporal_position_idx + 1
                                            if temporal_position_idx >= num_temporal_position:
                                                logger.warning(f"{protocol} temporal_position_idx is larger than max dim of temporal_position.")
                            # Multiple dynamic scan
                            else:
                                num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                                if not num_temporal_position.is_integer():
                                    logger.warning(f"{protocol} length of num_temporal_position is not integer.")
                                    continue
                                modality_idx = 0
                                # TemporalPositionIdentifier already known
                                if merged_pars_dict[CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"] != "" and merged_pars_dict[CIODKeyWord]["MRImage"]["NumberOfTemporalPositions"] != "" and \
                                    int(num_temporal_position) == int(merged_pars_dict[CIODKeyWord]["MRImage"]["NumberOfTemporalPositions"]) and \
                                        int(num_temporal_position) == int(len(merged_pars_dict[CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"])):
                                        num_temporal_position = int(merged_pars_dict[CIODKeyWord]["MRImage"]["NumberOfTemporalPositions"])
                                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                            merged_pars_dict[CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"].index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["TemporalPositionIdentifier"])] \
                                                                  for idx in slice_package_indexs]
                                else:
                                    # TemporalPositionIdentifier unknown
                                    logger.warning(f"{protocol} derived num_temporal_position is not equal to acquired NumberOfTemporalPositions in dicoms, we use derived instead.")
                                    num_temporal_position = int(num_temporal_position)
                                    temporal_position_idx = 0
                                    for idx in slice_package_indexs:
                                        slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                        modality_idx = sorted_ImageType.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["ImageType"][3])
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        if temp_stackingOrder not in stackingOrders:
                                            stackingOrders.append(temp_stackingOrder)
                                        else:
                                            temporal_position_idx = temporal_position_idx + 1
                                            if temporal_position_idx >= num_temporal_position:
                                                logger.warning(f"{protocol} temporal_position_idx is larger than max dim of temporal_position.")
                                            temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                            stackingOrders.append(temp_stackingOrder)
                        elif "SIEMENS" in Manufacturer:
                            # a diffusion study
                            if "DIFFUSION" in ImageTypes:
                                if isinstance(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], List):
                                    DWIBValList = sorted(merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"])
                                    # exactly equal to b_val images, DWI scan
                                    if "ISOTROPIC" == merged_pars_dict[CIODKeyWord]["VendorPrivateModule"]["DWIDiffusionDirection"]:
                                        if len(DWIBValList) == len(slice_package_indexs)/num_slice:
                                            tempos_idx = 0
                                            num_modality = int(len(DWIBValList))
                                            stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                                tempos_idx] for idx in slice_package_indexs]
                                        #in multi-dynamic case, time are append at last
                                        elif np.mod(len(slice_package_indexs)/num_slice, len(DWIBValList)) == 0 and len(slice_package_indexs)/num_slice/len(DWIBValList) > 1:
                                            tempos_idx = 0
                                            num_modality = int(len(DWIBValList))
                                            num_temporal_position = int(len(slice_package_indexs)/num_slice/len(DWIBValList))
                                            for idx in slice_package_indexs:
                                                stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                                 DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                                    tempos_idx]
                                                if stackingOrder not in stackingOrders:
                                                    stackingOrders.append(stackingOrder)
                                                else:
                                                    tempos_idx = tempos_idx + 1
                                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                                    DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                                        tempos_idx]
                                                    stackingOrders.append(stackingOrder)
                            # original-primary image with multiple dynamics
                            else:
                                if isinstance(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"], List):
                                    if len(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"]) == len(slice_package_indexs)/num_slice:
                                        AcquisitionTimeList = sorted(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"])
                                        modality_idx = 0
                                        num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                                AcquisitionTimeList.index(sorted_dict['pars'][idx][CIODKeyWord]["GeneralAcquisition"]["AcquisitionTime"])] for idx in slice_package_indexs]
                                elif isinstance(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"], List):
                                    if len(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"]) == len(slice_package_indexs)/num_slice:
                                        AcquisitionNumberList = sorted(merged_pars_dict[CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"])
                                        modality_idx = 0
                                        num_temporal_position = int(len(slice_package_indexs)/num_slice)
                                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                            modality_idx, \
                                                                AcquisitionNumberList.index(sorted_dict['pars'][idx][CIODKeyWord]["GeneralAcquisition"]["AcquisitionNumber"])] for idx in slice_package_indexs]
                        elif "GE" in Manufacturer:
                            # dixon image with multiple-dynamics, EPI with multiple B-values or Dixon multiple-dynamics
                            ScanningSequence = merged_pars_dict[CIODKeyWord]["MRImage"]["ScanningSequence"]
                            ScanOptions = merged_pars_dict[CIODKeyWord]["MRImage"]["ScanOptions"]
                            if "EPI_GEMS" in ScanOptions and "EP" in ScanningSequence:
                                #DWI scan
                                if isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], float) or isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], str):
                                    DWIBValList = sorted(list(set([parsDict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"] for parsDict in parsDicts])))
                                elif isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], List) or isinstance(parsDicts[0][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], pydicom.multival.MultiValue):
                                    DWIBValList = sorted([list(item) for item in dict.fromkeys(tuple(parsDict[CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]) for parsDict in parsDicts)], key = lambda x: x[0])
                                num_modality = int(len(DWIBValList))
                                # shrink remained dimension to temposition
                                if np.mod(len(slice_package_indexs)/num_slice, num_modality) == 0:
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                else:
                                    logger.error(f"Incomplete dataset with whole slice package includes {len(slice_package_indexs)}, {num_slice} slices, and {num_modality} modality, but {len(slice_package_indexs)/num_slice/num_modality} dynamics.")
                                tempos_idx = 0
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        DWIBValList.index(sorted_dict['pars'][idx][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]), \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)
                            else:
                                #dynamics imaging
                                modality_idx = 0
                                tempos_idx = 0
                                if np.mod(len(slice_package_indexs)/num_slice, num_modality) == 0:
                                    num_temporal_position = int(len(slice_package_indexs)/num_slice/num_modality)
                                else:
                                    logger.error(f"Incomplete dataset with whole slice package includes {len(slice_package_indexs)}, {num_slice} slices, and {num_modality} modality, but {len(slice_package_indexs)/num_slice/num_modality} dynamics.")
                                for idx in slice_package_indexs:
                                    stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                     modality_idx, \
                                                        tempos_idx]
                                    if stackingOrder not in stackingOrders:
                                        stackingOrders.append(stackingOrder)
                                    else:
                                        tempos_idx = tempos_idx + 1
                                        stackingOrder = [unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                                        modality_idx, \
                                                            tempos_idx]
                                        stackingOrders.append(stackingOrder)

                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, List) and len(ImageTypes) > 1:
                        #dixon?
                        if "Philips" in Manufacturer:
                            PhilipsDixonQuantImageTypeList = ['W','F','IP','OP','T2_STAR','R2_STAR','FF']
                            #Image Type Check
                            if all([any([item in PhilipsDixonQuantImageTypeList for item in ImageType]) for ImageType in ImageTypes]) and all(["DERIVED" in ImageType for ImageType in ImageTypes]):
                                #this is a Philips Dixon sequence
                                unique_ImageType = [ImageType[3] for ImageType in ImageTypes]
                                sorted_ImageType = []
                                for modality in PhilipsDixonQuantImageTypeList:
                                    if modality in unique_ImageType:
                                        sorted_ImageType.append(modality)
                                num_modality = len(sorted_ImageType)
                                num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                                if not num_temporal_position.is_integer():
                                    logger.warning(f"{protocol} length of num_temporal_position is not integer.")
                                    continue
                                num_temporal_position = int(num_temporal_position)
                                stackingOrders = []
                                temporal_position_idx = 0
                                for idx in slice_package_indexs:
                                    slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                    modality_idx = sorted_ImageType.index(sorted_dict['pars'][idx][CIODKeyWord]["MRImage"]["ImageType"][3])
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    if temp_stackingOrder not in stackingOrders:
                                        stackingOrders.append(temp_stackingOrder)
                                    else:
                                        temporal_position_idx = temporal_position_idx + 1
                                        if temporal_position_idx >= num_temporal_position:
                                            logger.warning(f"{protocol} temporal_position_idx is larger than max dim of temporal_position.")
                                        temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                        stackingOrders.append(temp_stackingOrder)
                else:
                    logger.warning(f'{protocol} in-complete dataset was found')
                    continue

                if PhotometricInterpretation == "MONOCHROME2":
                    stack_data = np.zeros((Rows, Columns, num_slice, num_modality, num_temporal_position))
                elif PhotometricInterpretation == "RGB":
                    stack_data = np.zeros((Rows, Columns, 3, num_slice, num_modality, num_temporal_position))

                #stacking pars dict and data
                stack_parsDict = mergeParsDict(parsDicts, stackingOrders)
                # splitParsDict(stack_parsDict)
                for data, stackingOrder in zip(dataList, stackingOrders):
                    stack_data[...,stackingOrder[0], stackingOrder[1], stackingOrder[2]] = data
                slice_package['pars'] = stack_parsDict
                slice_package['data'] = stack_data
                slice_packages.append(slice_package)
            proc_study_dataset[protocol] = slice_packages
            return True
        except:
            return False

def PyDicomGroupingEngine_CTImage(study_dataset_dict: dict,
                                  protocol: str,
                                  proc_study_dataset: dict):
        try:
            CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
            logger = logging.getLogger(inspect.currentframe().f_code.co_name)
            sorted_dict = dict()
            instance_numbers = [item[CIODKeyWord]["GeneralImage"]["InstanceNumber"] for item in study_dataset_dict[protocol]['pars']]
            idx_list = np.argsort(instance_numbers)
            sorted_dict['pars'] = [study_dataset_dict[protocol]['pars'][idx] for idx in idx_list]
            sorted_dict['data'] = [study_dataset_dict[protocol]['data'][idx] for idx in idx_list]
            image_orientations = [item[CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] for item in sorted_dict['pars']]
            #################################
            #
            # Slice orientation check
            #
            #################################
            unique_image_orientation, slice_packages_indexs = extractUniqueSliceOrientation(image_orientations)
            slice_packages = []
            for slice_packages_index, slice_package_indexs in enumerate(slice_packages_indexs):
                slice_package = dict()
                parsDicts = [sorted_dict['pars'][index] for index in slice_package_indexs]
                dataList = [sorted_dict['data'][index] for index in slice_package_indexs]
                merged_pars_dict = mergeParsDict(parsDicts)
                #ImagePositionPatient and SliceLocation are mandatory 
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"] == "":
                    raise ValueError
                #retrieve unique slice position and location
                if isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], List):
                    unique_image_position = [list(item) for item in dict.fromkeys(tuple(item) for item in merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"])]
                elif isinstance(merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], pydicom.multival.MultiValue):
                    unique_image_position = [merged_pars_dict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]]           
                #sorting image position
                ori_str, norm_vec = calc_image_ori(unique_image_orientation[slice_packages_index])
                unique_slice_location = [np.dot(image_position, norm_vec) for image_position in unique_image_position]
                unique_image_position, unique_slice_location = zip(*sorted(zip(unique_image_position, unique_slice_location), key = lambda x:x[1]))
                #unique slice gap check  ---> make sure continous slices
                slice_gaps = [item[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] for item in parsDicts]
                diff_image_position = [np.sqrt(np.sum(np.square(np.array(unique_image_position[slice_id]) - np.array(unique_image_position[slice_id - 1])))) for slice_id in range(1, len(unique_image_position))]
                if len(np.unique(slice_gaps)) > 1:
                    logger.warning(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                    continue
                elif len(diff_image_position) > 1:
                    if np.sum([(np.array(diff_image_position[slice_id]) - np.array(diff_image_position[slice_id - 1]))>1e-1 for slice_id in range(1, len(diff_image_position))]) > 0:
                        logger.warning(f"spacing between slices is expected to be same, we skip this series with orientation {ori_str}.")
                        continue
                #Spacing between slice check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] == "":
                    if len(unique_slice_location) > 1:
                        #update parsDict
                        for parsDict in parsDicts:
                            parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = np.mean(diff_image_position)
                    elif len(unique_slice_location) == 1:
                        if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] != "":
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceThickness"] # use slice thickness
                        else:
                            for parsDict in parsDicts:
                                parsDict[CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"] = 1 # default 1
                    logger.warning(f"Since empty SpacingBetweenSlices are found, we use the derived one instead.")
                #Slice Location check
                if merged_pars_dict[CIODKeyWord]["ImagePlane"]["SliceLocation"] == "":
                    for parsDict in parsDicts:
                        parsDict[CIODKeyWord]["ImagePlane"]["SliceLocation"] = np.dot(parsDict[CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)
                    logger.warning(f"Since empty SliceLocation are found, we use the derived one instead.")
                num_slice = len(unique_slice_location)
                num_modality = 1 #default value
                num_temporal_position = 1 #default value
                stackingOrders = []
                #unique row check
                Rows = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Rows"]
                Columns = merged_pars_dict[CIODKeyWord]["ImagePixel"]["Columns"]
                PhotometricInterpretation = merged_pars_dict[CIODKeyWord]["ImagePixel"]["PhotometricInterpretation"]
                Manufacturer = merged_pars_dict[CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
                ImageTypes = merged_pars_dict[CIODKeyWord]["GeneralImage"]["ImageType"]
                if isinstance(Rows, List):
                    logger.warning(f"{protocol} length of unique row is larger than 1.")
                    continue
                if isinstance(Columns, List):
                    logger.warning(f"{protocol} length of unique column is larger than 1.")
                    continue
                if isinstance(PhotometricInterpretation, List):
                    logger.warning(f"{protocol} length of unique photometricInterp is larger than 1.")
                    continue
                if isinstance(Manufacturer, List):
                    logger.warning(f"{protocol} length of unique manufacturer is larger than 1.")
                    continue
                if np.mod(len(slice_package_indexs), num_slice) == 0:
                    if len(slice_package_indexs)/num_slice == 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        #stacking by image position, in case of one imagetype and 1 modality, one repetation
                        modality_idx = 0
                        temporal_position_index = 0
                        stackingOrders = [[unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec)), \
                                            modality_idx, \
                                                temporal_position_index] for idx in slice_package_indexs]
                    elif len(slice_package_indexs)/num_slice > 1 and isinstance(ImageTypes, pydicom.multival.MultiValue):
                        #muklti-dynamic image
                        num_modality = 1
                        num_temporal_position = len(slice_package_indexs)/num_slice/num_modality
                        if not num_temporal_position.is_integer():
                            logger.warning(f"{protocol} length of num_temporal_position is not integer.")
                            continue
                        else:
                            num_temporal_position = int(num_temporal_position)
                            temporal_position_idx = 0
                            modality_idx = 0
                            for idx in slice_package_indexs:
                                slice_idx = unique_slice_location.index(np.dot(sorted_dict['pars'][idx][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"], norm_vec))
                                temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                if temp_stackingOrder not in stackingOrders:
                                    stackingOrders.append(temp_stackingOrder)
                                else:
                                    temporal_position_idx = temporal_position_idx + 1
                                    if temporal_position_idx >= num_temporal_position:
                                        logger.warning(f"{protocol} temporal_position_idx is larger than max dim of temporal_position.")
                                        raise ValueError
                                    temp_stackingOrder = [slice_idx, modality_idx, temporal_position_idx]
                                    stackingOrders.append(temp_stackingOrder)
                else:
                    logger.warning(f'{protocol} in-complete dataset was found')
                    continue

                if PhotometricInterpretation == "MONOCHROME2":
                    stack_data = np.zeros((Rows, Columns, num_slice, num_modality, num_temporal_position))
                elif PhotometricInterpretation == "RGB":
                    stack_data = np.zeros((Rows, Columns, 3, num_slice, num_modality, num_temporal_position))

                #stacking pars dict and data
                stack_parsDict = mergeParsDict(parsDicts, stackingOrders)
                # splitParsDict(stack_parsDict)
                for data, stackingOrder in zip(dataList, stackingOrders):
                    stack_data[...,stackingOrder[0], stackingOrder[1], stackingOrder[2]] = data
                slice_package['pars'] = stack_parsDict
                slice_package['data'] = stack_data
                slice_packages.append(slice_package)
            proc_study_dataset[protocol] = slice_packages
            return True
        except:
            return False
    
def recursivelyMergeDict(src: List,
                         dst: dict,
                         stackingOrders: List = None,
                         MAXStackingOrder: List = None,
                         isMerge: bool = True):
    #key check
    for key, value in dst.items():
        if isinstance(value, dict):
            recursivelyMergeDict([item[key] for item in src],
                                 dst[key],
                                 stackingOrders,
                                 MAXStackingOrder,
                                 isMerge)
        elif not isinstance(value, dict):
            #uniquess_check
            if isMerge:
                if isinstance(value, pydicom.multival.MultiValue) or isinstance(value, List):
                    temp = [list(item) for item in dict.fromkeys(tuple(item[key]) for item in src)]
                else:
                    temp = list(dict.fromkeys([item[key] for item in src]))
            else:
                temp = [item[key] for item in src]
            if len(temp) > 1: # if more than one unique value existed, then update
                if isinstance(stackingOrders, List) and isinstance(MAXStackingOrder, List):
                    dst[key] = [[['' for _ in range(MAXStackingOrder[2])] for _ in range(MAXStackingOrder[1])] for _ in range(MAXStackingOrder[0])]
                    for idx, stackingOrder in enumerate(stackingOrders):
                        dst[key][stackingOrder[0]][stackingOrder[1]][stackingOrder[2]] = src[idx][key]
                else:
                    dst[key] = temp
                    
def mergeParsDict(parsDicts: dict,
                  stackingOrders: List = None,
                  isMerge: bool = True):
    if not stackingOrders:
        merged_pars_dict = copy.deepcopy(parsDicts[0])
        recursivelyMergeDict(parsDicts, merged_pars_dict, None, None, isMerge)
    else:
        assert len(parsDicts) == len(stackingOrders)
        stackingOrders = np.array(stackingOrders)
        MAXSlice = np.max(stackingOrders[:,0])
        MAXModality = np.max(stackingOrders[:,1])
        MAXTemporalPosition = np.max(stackingOrders[:,2])
        MAXStackingOrder = [MAXSlice + 1, MAXModality + 1, MAXTemporalPosition + 1]
        assert len(parsDicts) == (MAXSlice + 1) * (MAXModality + 1) * (MAXTemporalPosition + 1)
        merged_pars_dict = copy.deepcopy(parsDicts[0])
        recursivelyMergeDict(parsDicts,
                             merged_pars_dict,
                             list(stackingOrders),
                             MAXStackingOrder,
                             isMerge)
    return merged_pars_dict

def recursivelyParseDict(src: dict,
                         dst: dict,
                         SliceIndex: int,
                         ModalityIndex: int,
                         TemposIndex: int):
    for key, value in src.items():
        if isinstance(src[key], dict) and key not in dst.keys():
            dst[key] = dict()
            recursivelyParseDict(value,
                                 dst[key],
                                 SliceIndex,
                                 ModalityIndex,
                                 TemposIndex)
        elif isinstance(src[key], List) and len(np.array(src[key]).shape) >= 3:
            dst[key] = value[SliceIndex][ModalityIndex][TemposIndex]
        else:
            dst[key] = src[key]

def recursivelyEvalStackingOrder(src: dict):
    global target_shape
    for key, value in src.items():
        if isinstance(src[key], dict):
            recursivelyEvalStackingOrder(src[key])
        elif isinstance(src[key], List) and len(np.array(src[key]).shape) >= 3:
            #flatten list
            if not target_shape:
                target_shape = list(np.array(src[key]).shape)[:3]
            else:
                assert target_shape == list(np.array(src[key]).shape)[:3]

def extractStackingOrder(merged_pars_dict):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    global target_shape
    target_shape = None
    recursivelyEvalStackingOrder(merged_pars_dict)
    if target_shape:
        MAXSlice = target_shape[0]
        MAXModality = target_shape[1]
        MAXTemporalPosition = target_shape[2]
        return MAXSlice,MAXModality,MAXTemporalPosition
    else:
        logger.error(f"error in extract stacking order")

def splitParsDict(merged_pars_dict):
    MAXSlice,MAXModality,MAXTemporalPosition = extractStackingOrder(merged_pars_dict)
    parsDicts = []
    stackingOrders = []
    for iSlice in range(MAXSlice):
        for iModality in range(MAXModality):
            for iTemporalPosition in range(MAXTemporalPosition):
                parsDict = dict()
                recursivelyParseDict(merged_pars_dict,
                         parsDict,
                         iSlice,
                         iModality,
                         iTemporalPosition)
                parsDicts.append(parsDict)
                stackingOrders.append([iSlice, iModality, iTemporalPosition])
    return parsDicts, stackingOrders
    
def extractUniqueSliceOrientation(image_orientations,
                                  BIAS: float = 1e-5):
    unique_image_orientation = []
    slice_packages_indexs = []
    for idx in range(len(image_orientations)):
        if unique_image_orientation:
            if image_orientations[idx] not in unique_image_orientation:
                diff = np.sqrt(np.sum((np.array(unique_image_orientation) - np.array(image_orientations[idx]))**2, axis = 1))
                if diff[np.argmin(diff)] < BIAS: #should be the same orientation
                    slice_packages_indexs[np.argmin(diff)].append(idx)
                else:
                    unique_image_orientation.append(image_orientations[idx])
                    slice_packages_indexs.append([idx])
            else:
                slice_packages_indexs[unique_image_orientation.index(image_orientations[idx])].append(idx)
        else:
            unique_image_orientation.append(image_orientations[idx])
            slice_packages_indexs.append([idx])
    
    return unique_image_orientation, slice_packages_indexs

def PyDicomStorageEngine_main(proc_study_dataset: dict,
                         raw_dicoms: dict,
                         save_path: Union[str, Path, os.PathLike]):
        logger = logging.getLogger(inspect.currentframe().f_code.co_name)
        #double check
        bar = alive_it(sorted(proc_study_dataset.keys()))
        for protocol in bar:
            bar.text("Saving protocol: " + protocol)
            if proc_study_dataset[protocol] and raw_dicoms[protocol]:
                logger.info(f'Saving protocol {protocol}')
                #save raw dicoms
                saveRawDicoms(raw_dicom = raw_dicoms[protocol],
                              save_path = os.path.join(save_path, 'raw_dicoms', protocol))
                #save stacked nifti
                CIODKeyWord = list(proc_study_dataset[protocol][0]["pars"].keys())[0]
                globals()["_".join(["PyDicomStorageEngine",CIODKeyWord])](proc_seq_dataset = proc_study_dataset[protocol],
                                                                          save_path = os.path.join(save_path, 'stacked_nifti'),
                                                                          protocol = protocol)
                
def PyDicomStorageEngine_MRImage(proc_seq_dataset: List,
                                 save_path: Union[str, Path, os.PathLike],
                                 protocol: str):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    nifti_data_path = os.path.join(save_path, "data")
    nifti_pars_path = os.path.join(save_path, "pars")
    os.makedirs(nifti_data_path, exist_ok = True)
    os.makedirs(nifti_pars_path, exist_ok = True)
    for slice_package_idx, slice_package in enumerate(proc_seq_dataset):
        PixelSpacing = slice_package["pars"][CIODKeyWord]["ImagePlane"]["PixelSpacing"]
        ImageOrientationPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"]
        ImagePositionPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]
        SpacingBetweenSlices = slice_package["pars"][CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"]
        affine_matrix = np.zeros((4,4))
        affine_matrix[:3,0] = np.array(ImageOrientationPatient[:3]) * PixelSpacing[0]
        affine_matrix[:3,1] = np.array(ImageOrientationPatient[3:]) * PixelSpacing[1]
        affine_matrix[:3,2] = np.cross(ImageOrientationPatient[:3], ImageOrientationPatient[3:]) * SpacingBetweenSlices
        if isinstance(ImagePositionPatient, List):
            affine_matrix[:3,3] = np.array(ImagePositionPatient[0][0][0])
        elif isinstance(ImagePositionPatient, pydicom.multival.MultiValue):
            affine_matrix[:3,3] = np.array(ImagePositionPatient[0])
        affine_matrix[3,3] = 1
        affine_matrix = np.diag([-1,-1,1,1]).dot(affine_matrix)
        nifti_filename = protocol
        if len(proc_seq_dataset) > 1:
            nifti_filename = nifti_filename + '_spack' + str(slice_package_idx)
        #dump slice package data
        fileExistCheck(os.path.join(nifti_data_path, nifti_filename + '.nii.gz'), logger)
        dump_nifti(nifti_path = os.path.join(nifti_data_path, nifti_filename + '.nii.gz'),
                   affine_matrix = affine_matrix,
                   ndarray = slice_package["data"])
        #dump slice pars
        fileExistCheck(os.path.join(nifti_pars_path, nifti_filename + '.pkl'), logger)
        pickle_dump(obj = slice_package["pars"],
                  path = os.path.join(nifti_pars_path, nifti_filename + '.pkl'))

def PyDicomStorageEngine_CTImage(proc_seq_dataset: List,
                                 save_path: Union[str, Path, os.PathLike],
                                 protocol: str):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    nifti_data_path = os.path.join(save_path, "data")
    nifti_pars_path = os.path.join(save_path, "pars")
    os.makedirs(nifti_data_path, exist_ok = True)
    os.makedirs(nifti_pars_path, exist_ok = True)
    for slice_package_idx, slice_package in enumerate(proc_seq_dataset):
        PixelSpacing = slice_package["pars"][CIODKeyWord]["ImagePlane"]["PixelSpacing"]
        ImageOrientationPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"]
        ImagePositionPatient = slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImagePositionPatient"]
        SpacingBetweenSlices = slice_package["pars"][CIODKeyWord]["ImagePlane"]["SpacingBetweenSlices"]
        affine_matrix = np.zeros((4,4))
        affine_matrix[:3,0] = np.array(ImageOrientationPatient[:3]) * PixelSpacing[0]
        affine_matrix[:3,1] = np.array(ImageOrientationPatient[3:]) * PixelSpacing[1]
        affine_matrix[:3,2] = np.cross(ImageOrientationPatient[:3], ImageOrientationPatient[3:]) * SpacingBetweenSlices
        if isinstance(ImagePositionPatient, List):
            affine_matrix[:3,3] = np.array(ImagePositionPatient[0][0][0])
        elif isinstance(ImagePositionPatient, pydicom.multival.MultiValue):
            affine_matrix[:3,3] = np.array(ImagePositionPatient[0])
        affine_matrix[3,3] = 1
        affine_matrix = np.diag([-1,-1,1,1]).dot(affine_matrix)
        nifti_filename = protocol
        if len(proc_seq_dataset) > 1:
            nifti_filename = nifti_filename + '_spack' + str(slice_package_idx)
        #dump slice package data
        fileExistCheck(os.path.join(nifti_data_path, nifti_filename + '.nii.gz'), logger)
        dump_nifti(nifti_path = os.path.join(nifti_data_path, nifti_filename + '.nii.gz'),
                   affine_matrix = affine_matrix,
                   ndarray = slice_package["data"])
        #dump slice pars
        fileExistCheck(os.path.join(nifti_pars_path, nifti_filename + '.pkl'), logger)
        pickle_dump(obj = slice_package["pars"],
                  path = os.path.join(nifti_pars_path, nifti_filename + '.pkl'))
        
def PyDicomGroupingSummary_main(proc_study_dataset: dict,
                                study_cache: dict):
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    sequences_pars_list = []
    study_cache["sequences"] = dict()
    #double check
    for protocol in proc_study_dataset.keys():
        if proc_study_dataset[protocol]:
            logger.info(f'Summarizing protocol {protocol}')
            #save stacked nifti
            CIODKeyWord = list(proc_study_dataset[protocol][0]["pars"].keys())[0]
            sequence_pars = dict()
            sequence_pars = globals()["_".join(["PyDicomGroupingSummary",CIODKeyWord])](slice_packages = proc_study_dataset[protocol])
            if sequence_pars:
                sequences_pars_list.append(sequence_pars) #to be merged
            else:
                logger.error(f"error in generating grouping summary of protocol {protocol}")
                continue
            sequence_prop = globals()["_".join(["extractSequencesProperty",CIODKeyWord])](slice_packages = proc_study_dataset[protocol])
            if sequence_prop:
                study_cache["sequences"][protocol] = dict()
                study_cache["sequences"][protocol]["property"] = sequence_prop
            else:
                logger.error(f"error in extract sequence property of protocol {protocol}")
                continue
    study_pars = mergeParsDict(sequences_pars_list)
    study_cache["study_pars"] = study_pars
    return True

def PyDicomGroupingSummary_MRImage(slice_packages: List):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        slice_packages_pars_list = []
        for slice_package in slice_packages:
            slice_package_pars = dict()
            #patient Module
            slice_package_pars["PatientName"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientName"]
            slice_package_pars["PatientID"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientID"]
            slice_package_pars["PatientBirthDate"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientBirthDate"]
            slice_package_pars["PatientSex"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientSex"]
            #patientStudy Module
            slice_package_pars["PatientAge"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientAge"]
            slice_package_pars["PatientWeight"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientWeight"]
            slice_package_pars["PregnancyStatus"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PregnancyStatus"]
            #GeneralStudy Module
            slice_package_pars["StudyInstanceUID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyInstanceUID"]
            slice_package_pars["AccessionNumber"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["AccessionNumber"]
            slice_package_pars["StudyID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyID"]
            #GeneralSeries Module
            slice_package_pars["Modality"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["Modality"]
            slice_package_pars["BodyPartExamined"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["BodyPartExamined"]
            #GeneralEquipment Module
            slice_package_pars["Manufacturer"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
            slice_package_pars["InstitutionName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionName"]
            slice_package_pars["StationName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["StationName"]
            slice_package_pars["InstitutionalDepartmentName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionalDepartmentName"]
            slice_package_pars["ManufacturerModelName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["ManufacturerModelName"]
            #MRImage Module
            slice_package_pars["MagneticFieldStrength"] = slice_package["pars"][CIODKeyWord]["MRImage"]["MagneticFieldStrength"]
            slice_packages_pars_list.append(slice_package_pars)
        #merge slice-package dict
        sequence_pars = mergeParsDict(slice_packages_pars_list)
        for key, value in sequence_pars.items():
            if isinstance(value, List):
                raise ValueError
        return sequence_pars
    except:
        logger.error(f'{key} is expected to be same in slice-packages.')
        return False

def PyDicomGroupingSummary_CTImage(slice_packages: List):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    try:
        slice_packages_pars_list = []
        for slice_package in slice_packages:
            slice_package_pars = dict()
            #patient Module
            slice_package_pars["PatientName"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientName"]
            slice_package_pars["PatientID"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientID"]
            slice_package_pars["PatientBirthDate"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientBirthDate"]
            slice_package_pars["PatientSex"] = slice_package["pars"][CIODKeyWord]["Patient"]["PatientSex"]
            #patientStudy Module
            slice_package_pars["PatientAge"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientAge"]
            slice_package_pars["PatientWeight"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PatientWeight"]
            slice_package_pars["PregnancyStatus"] = slice_package["pars"][CIODKeyWord]["PatientStudy"]["PregnancyStatus"]
            #GeneralStudy Module
            slice_package_pars["StudyInstanceUID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyInstanceUID"]
            slice_package_pars["AccessionNumber"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["AccessionNumber"]
            slice_package_pars["StudyID"] = slice_package["pars"][CIODKeyWord]["GeneralStudy"]["StudyID"]
            #GeneralSeries Module
            slice_package_pars["Modality"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["Modality"]
            slice_package_pars["BodyPartExamined"] = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["BodyPartExamined"]
            #GeneralEquipment Module
            slice_package_pars["Manufacturer"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
            slice_package_pars["InstitutionName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionName"]
            slice_package_pars["StationName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["StationName"]
            slice_package_pars["InstitutionalDepartmentName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["InstitutionalDepartmentName"]
            slice_package_pars["ManufacturerModelName"] = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["ManufacturerModelName"]
            #MRImage Module
            slice_package_pars["SingleCollimationWidth"] = slice_package["pars"][CIODKeyWord]["CTImage"]["SingleCollimationWidth"]
            slice_package_pars["TotalCollimationWidth"] = slice_package["pars"][CIODKeyWord]["CTImage"]["TotalCollimationWidth"]
            slice_packages_pars_list.append(slice_package_pars)
        #merge slice-package dict
        sequence_pars = mergeParsDict(slice_packages_pars_list)
        for key, value in sequence_pars.items():
            if isinstance(value, List):
                raise ValueError
        return sequence_pars
    except:
        logger.error(f'{key} is expected to be same in slice-packages.')
        return False

def extractSequencesProperty_CTImage(slice_packages: List):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    slice_packages_property = dict()
    slice_packages_property["slice_package_property"] = []
    slice_package_property = None
    #configure standard dixon quant map
    for slice_package in slice_packages:
        slice_package_property = extractSequenceProperty_MRImage(slice_package)
        slice_packages_property["slice_package_property"].append(slice_package_property)
    if len(slice_packages) == 1:
        slice_packages_property["orientation"] = slice_package_property["orientation"]
        slice_packages_property["SliceThickness"] = slice_package_property["SliceThickness"]
        slice_packages_property["slice_package_type"] = slice_package_property["slice_package_type"]
    
    return slice_packages_property

def extractSequenceProperty_CTImage(slice_package: dict):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    #in case GE with similar image Orientation
    if isinstance(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"][0], List):
        # if multiple similar image orientation, we update to mean orientation
        slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] = np.mean(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"],axis = (0,1,2))

    image_oris = calc_image_ori(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"])[0]
    SliceThickness = slice_package["pars"][CIODKeyWord]["ImagePlane"]["SliceThickness"]
    #init output
    slice_package_property = dict()
    slice_package_property["orientation"] = image_oris
    slice_package_property["SliceThickness"] = SliceThickness
    if slice_package["data"].shape(4) > 1: # more than one dynamics
        slice_package_property["slice_package_type"] = "multi_dynamics"
    else:
        slice_package_property["slice_package_type"] = "single_dynamics"
    return slice_package_property

def extractSequencesProperty_MRImage(slice_packages: List):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    logger = logging.getLogger(inspect.currentframe().f_code.co_name)
    slice_packages_property = dict()
    slice_packages_property["slice_package_property"] = []
    slice_package_property = None
    #configure standard dixon quant map
    for slice_package in slice_packages:
        slice_package_property = extractSequenceProperty_MRImage(slice_package)
        slice_packages_property["slice_package_property"].append(slice_package_property)
    if len(slice_packages) > 1:
        MRAcquisitionTypes = list(set([slice_package_property["MRAcquisitionType"] for slice_package_property in slice_packages_property["slice_package_property"]]))
        slice_package_types = list(set([slice_package_property["slice_package_type"] for slice_package_property in slice_packages_property["slice_package_property"]]))
        orientations = list(set([slice_package_property["orientation"] for slice_package_property in slice_packages_property["slice_package_property"]]))
        if len(slice_packages) == 3 and len(orientations) == 3 and len(slice_package_types) == 1 and len(MRAcquisitionTypes) == 1:
            if sorted(orientations) == sorted(["Transverse", "Coronal", "Sagittal"]) and MRAcquisitionTypes[0] == "2D":
                slice_packages_property["orientation"] = orientations
                slice_packages_property["MRAcquisitionType"] = MRAcquisitionTypes[0]
                slice_packages_property["slice_package_type"] = "Localizer"
        else:
            if any(["MPR" in slice_package_type for slice_package_type in slice_package_types]):
                slice_packages_property["orientation"] = orientations
                slice_packages_property["MRAcquisitionType"] = MRAcquisitionTypes
                slice_packages_property["slice_package_type"] = "MPR"
    elif len(slice_packages) == 1:
        slice_packages_property["orientation"] = slice_package_property["orientation"]
        slice_packages_property["MRAcquisitionType"] = slice_package_property["MRAcquisitionType"]
        slice_packages_property["slice_package_type"] = slice_package_property["slice_package_type"]
    
    return slice_packages_property

def extractSequenceProperty_MRImage(slice_package: dict):
    CIODKeyWord = inspect.currentframe().f_code.co_name.split('_')[-1]
    #in case GE with similar image Orientation
    if isinstance(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"][0], List):
        # if multiple similar image orientation, we update to mean orientation
        slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"] = np.mean(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"],axis = (0,1,2))

    image_oris = calc_image_ori(slice_package["pars"][CIODKeyWord]["ImagePlane"]["ImageOrientationPatient"])[0]
    Manufacturer = slice_package["pars"][CIODKeyWord]["GeneralEquipment"]["Manufacturer"]
    ImageType = slice_package["pars"][CIODKeyWord]["GeneralImage"]["ImageType"]
    ScanningSequence = slice_package["pars"][CIODKeyWord]["MRImage"]["ScanningSequence"]
    MRAcquisitionType = slice_package["pars"][CIODKeyWord]["MRImage"]["MRAcquisitionType"]
    SequenceName = slice_package["pars"][CIODKeyWord]["MRImage"]["SequenceName"]
    ScanOptions = slice_package["pars"][CIODKeyWord]["MRImage"]["ScanOptions"]
    EchoTrainLength = slice_package["pars"][CIODKeyWord]["MRImage"]["EchoTrainLength"]
    StandardDixonQuantImageType = ["W","F","IP","OP","T2_STAR","R2_STAR","FF"]
    #init output
    slice_package_property = dict()
    slice_package_property["orientation"] = image_oris
    slice_package_property["MRAcquisitionType"] = MRAcquisitionType

    if isinstance(ImageType, pydicom.multival.MultiValue):
        if "Philips" in Manufacturer:
            PhilipsDixonQuantImageTypeList = ["W","F","IP","OP","T2_STAR","R2_STAR","FF"]
            # T2WI + DWI
            if "SE" in ImageType: # magnitude SE images
                if isinstance(slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], float) and \
                    slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"] == 0.0:
                    if "FS" in ScanOptions:
                        slice_package_property["slice_package_type"] = "FS-T2WI"
                    else:
                        slice_package_property["slice_package_type"] = "T2WI"
                elif isinstance(slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"], List) and \
                    np.max(slice_package["pars"][CIODKeyWord]["VendorPrivateModule"]["DWIBVal"]) > 0:
                    if "FS" in ScanOptions:
                        slice_package_property["slice_package_type"] = "FS-DWI"
                    else:
                        slice_package_property["slice_package_type"] = "DWI"
            elif "ADC" in ImageType:
                if "FS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-ADC"
                else:
                    slice_package_property["slice_package_type"] = "ADC"
            elif any([item in PhilipsDixonQuantImageTypeList for item in ImageType]) and "DERIVED" in ImageType:
                #Dixon scan
                slice_package_property["slice_package_type"] = "Dixon " + "[" +  ImageType[[item in PhilipsDixonQuantImageTypeList for item in ImageType].index(True)] + "]"
            elif "GR" in ScanningSequence:
                if "FS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-T1WI"
                else:
                    slice_package_property["slice_package_type"] = "T1WI"
            else:
                slice_package_property["slice_package_type"] = "unknow"
                raise ValueError
        elif "UIH" in Manufacturer:
            # GRE 3D and T2WI all have one imageType
            UIHQuantImageType = ["W", "F", "IP", "OP"]
            #scan option check
            if "GR" in ScanningSequence:
                #Image type check
                if any([item in UIHQuantImageType for item in ImageType]):
                    slice_package_property["slice_package_type"] = "Dixon " + "[" + ImageType[[item in UIHQuantImageType for item in ImageType].index(True)] + "]"
                else:
                    if "FS" in ScanOptions:
                        slice_package_property["slice_package_type"] = "FS-T1WI"
                    else:
                        slice_package_property["slice_package_type"] = "T1WI"
            #scan option check
            elif ScanningSequence == "SE" and "DWI" not in ImageType:
                if "FS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-T2WI"
                else:
                    slice_package_property["slice_package_type"] = "T2WI"
            elif "EP" in ScanningSequence:
                #ADC image type
                if "DWI" in ImageType:
                    if "ADC" in ImageType:
                        if "FS" in ScanOptions:
                            slice_package_property["slice_package_type"] = "FS-ADC"
                        else:
                            slice_package_property["slice_package_type"] = "ADC"
                #DWI image type
                    else:
                        if "FS" in ScanOptions:
                            slice_package_property["slice_package_type"] = "FS-DWI"
                        else:
                            slice_package_property["slice_package_type"] = "DWI"
            else:
                slice_package_property["slice_package_type"] = "unknow"
                raise ValueError
        elif "SIEMENS" in Manufacturer:
            SIEMENSQuantImageType = ["WATER", "FAT", "IN_PHASE", "OUT_PHASE"]
            #T2WI
            if "SE" in ScanningSequence and "EP" not in ScanningSequence and "DIFFUSION" not in ImageType:
                if "SFS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-T2WI"
                else:
                    slice_package_property["slice_package_type"] = "T2WI"
            #Dixon or T1WI
            elif any([item in SIEMENSQuantImageType for item in ImageType]):
                    slice_package_property["slice_package_type"] = "Dixon " + "[" + StandardDixonQuantImageType[SIEMENSQuantImageType.index(ImageType[[item in SIEMENSQuantImageType for item in ImageType].index(True)])] + "]"
            #2D T1WI
            elif "GR" in ScanningSequence:
                if "SAT2" in ScanOptions or "SFS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-T1WI"
                else:
                    slice_package_property["slice_package_type"] = "T1WI"
            #DWI
            elif "EP" in ScanningSequence and "DIFFUSION" in ImageType:
                if "ADC" in ImageType:
                    if "SFS" in ScanOptions:
                        slice_package_property["slice_package_type"] = "FS-ADC"
                    else:
                        slice_package_property["slice_package_type"] = "ADC"
                else:
                    if "SFS" in ScanOptions:
                        slice_package_property["slice_package_type"] = "FS-DWI"
                    else:
                        slice_package_property["slice_package_type"] = "DWI"
            else:
                slice_package_property["slice_package_type"] = "unknow"
                raise ValueError
        elif "GE" in Manufacturer:
            #multi-echo fse scan, i.e. T2WI
            if ("SE" in ScanningSequence or "RM" in ScanningSequence) and "EPI_GEMS" not in ScanOptions:
                if "FS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-T2WI"
                else:
                    slice_package_property["slice_package_type"] = "T2WI"
            #Dixon scan
            elif "FLEX_GEMS" in ScanOptions:
                SeriesDescription = slice_package["pars"][CIODKeyWord]["GeneralSeries"]["SeriesDescription"]
                GEQuantImageTypes = ["WATER", "FAT", "InPhase", "OutPhase"]
                if any([GEQuantImageType in  SeriesDescription for GEQuantImageType in GEQuantImageTypes]):
                    slice_package_property["slice_package_type"] = "Dixon " + "[" + StandardDixonQuantImageType[[GEQuantImageType in  SeriesDescription for GEQuantImageType in GEQuantImageTypes].index(True)] + "]"
            elif "EPI_GEMS" in ScanOptions:
                if "EP" in ScanningSequence:
                    if "ADC" in ImageType:
                        if "FS" in ScanOptions:
                            slice_package_property["slice_package_type"] = "FS-ADC"
                        else:
                            slice_package_property["slice_package_type"] = "ADC"
                    else:
                        if "FS" in ScanOptions:
                            slice_package_property["slice_package_type"] = "FS-DWI"
                        else:
                            slice_package_property["slice_package_type"] = "DWI"
            # lava imaging
            elif "GR" in ScanningSequence:
                if "FS" in ScanOptions:
                    slice_package_property["slice_package_type"] = "FS-T1WI"
                else:
                    slice_package_property["slice_package_type"] = "T1WI"
            else:
                slice_package_property["slice_package_type"] = "unknow"
                raise ValueError

        #if MPR or PROJECTION image existed, add MPR, add prefix
        if "MPR" in ImageType or "PROJECTION IMAGE" in ImageType:
            slice_package_property["slice_package_type"] = "MPR " + slice_package_property["slice_package_type"]
    elif isinstance(ImageType, List):
        if "Philips" in Manufacturer:
            PhilipsDixonQuantImageTypeList = ['W','F','IP','OP','T2_STAR','R2_STAR','FF']
            unique_ImageTypes = [list(item) for item in dict.fromkeys(tuple(item) for item in [temposition for slices in ImageType for modality in slices for temposition in modality])]
            if all([any([item in PhilipsDixonQuantImageTypeList for item in unique_ImageType]) for unique_ImageType in unique_ImageTypes]) and all(["DERIVED" in unique_ImageType for unique_ImageType in unique_ImageTypes]):
                    modality = [unique_ImageType[[ImageTypeItem in PhilipsDixonQuantImageTypeList for ImageTypeItem in unique_ImageType].index(True)] for unique_ImageType in unique_ImageTypes]
                    slice_package_property["slice_package_type"] = "Dixon " + "[" + ",".join(modality) + "]"
            else:
                slice_package_property["slice_package_type"] = "unknow"
    else:
        raise ValueError
    return slice_package_property


def fileExistCheck(file_path: Union[str, Path, os.PathLike],
                     logger):
    if os.path.exists(file_path):
        print(f'Warning: {os.path.basename(file_path)} is already existed in {os.path.dirname(file_path)}, file will be replaced.')
        logger.warning(f'{os.path.basename(file_path)} is already existed in {os.path.dirname(file_path)}, file will be replaced.')

def saveRawDicoms(raw_dicom: List,
                  save_path: Union[str, Path, os.PathLike]):
    os.makedirs(save_path, exist_ok = True)
    for raw_dicom_item in raw_dicom:
        src_path, SOPInstanceUID = raw_dicom_item
        shutil.copy(src_path, os.path.join(save_path, SOPInstanceUID + '.dcm')) # all the row dicoms will stored as SOPInstanceUID

#customized nifti reader and writer
def load_nifti(nifti_path: Union[str, Path, os.PathLike]):        
    #       
    nii_image = nib.load(nifti_path)
    ndarray = np.moveaxis(nii_image.get_fdata(),1,0)    
    return ndarray

def dump_nifti(nifti_path:Union[str, Path, os.PathLike],
               affine_matrix,
               ndarray):
    #save nifti image with nifti format. dicom -> LAS cordinate
    nii_image = nib.Nifti1Image(np.moveaxis(ndarray,0,1), affine=affine_matrix)
    nib.save(nii_image,nifti_path)

def calc_image_ori(image_ori_list: np.ndarray):
    #evaluate image_ori_str by using image_ori_list
    # in patient-based cordinate system, x-axis increasing to the left hand side of patient
    #                                    y-axis increasing to the posterior side of the patient
    #                                    z-axis increasing to the head of patient
    assert(len(image_ori_list) == 6)
    #
    ori_matrix = np.zeros((3,3))
    ori_matrix[0,0] = image_ori_list[0]
    ori_matrix[0,1] = image_ori_list[1]
    ori_matrix[0,2] = image_ori_list[2]
    ori_matrix[1,0] = image_ori_list[3]
    ori_matrix[1,1] = image_ori_list[4]
    ori_matrix[1,2] = image_ori_list[5]
    #calcualte frame norm
    ori_matrix[2,0] = ori_matrix[0,1] * ori_matrix[1,2] - ori_matrix[0,2] * ori_matrix[1,1]
    ori_matrix[2,1] = ori_matrix[0,2] * ori_matrix[1,0] - ori_matrix[0,0] * ori_matrix[1,2]
    ori_matrix[2,2] = ori_matrix[0,0] * ori_matrix[1,1] - ori_matrix[0,1] * ori_matrix[1,0]
    image_ori_str = []
    if (abs(ori_matrix[2,0]) > abs(ori_matrix[2,1])) and (abs(ori_matrix[2,0]) > abs(ori_matrix[2,2])):
        image_ori_str = 'Sagittal'
    elif (abs(ori_matrix[2,1]) > abs(ori_matrix[2,0])) and (abs(ori_matrix[2,1]) > abs(ori_matrix[2,2])):
        image_ori_str = 'Coronal'
    elif (abs(ori_matrix[2,2]) > abs(ori_matrix[2,0])) and (abs(ori_matrix[2,2] > ori_matrix[2,1])):
        image_ori_str = 'Transverse'
    return image_ori_str,ori_matrix[2,:]

def cal_mid_position(image_position,
                     rows,
                     cols,
                     pixel_space,
                     image_ori_list):
    # function for calculate middle position of dicom image
    #Input:
    #       image_position: position for 1st volume in slice
    #       rows: number of row
    #       col: number of col
    #       pixel_space: in mm
    #       image_ori_list: 6-element vector
    #Output:
    #       mid_pos: midle point position for slice
    #2024/01/02 in Canton by Kaixuan
    assert(len(image_ori_list) == 6)
    assert(len(image_position) == 3)
    mid_pos = np.zeros((3))
    mid_pos[0] = image_position[0] + (cols/2) * pixel_space[0] * image_ori_list[0] + (rows/2) * pixel_space[1] * image_ori_list[3]
    mid_pos[1] = image_position[1] + (cols/2) * pixel_space[0] * image_ori_list[1] + (rows/2) * pixel_space[1] * image_ori_list[4]
    mid_pos[2] = image_position[2] + (cols/2) * pixel_space[0] * image_ori_list[2] + (rows/2) * pixel_space[1] * image_ori_list[5]
    return mid_pos

def find_elements(parsDict: dict,
                  keyWord: str,
                  temp_path: List,
                  res_chain: List):
    for key, val in parsDict.items():
        if key != keyWord and isinstance(val, dict):
            find_elements(val, keyWord, [*temp_path, key], res_chain)
        elif key == keyWord:
            res_dict = dict()
            res_dict["val"] = val
            res_dict["key_chain"] = temp_path
            res_chain.append(res_dict)

def retrieveVendorPrivateTreeNode_MRImage(manufacturer: str,
                                          software_version: Optional[str] = None):
    VendorPrivateTreeNode = DicomStandardTreeNode(DicomModuleItem(**{"ModuleName":"VendorPrivateModule",
                                                                   "InformationEntity":"Image",
                                                                   "Usage":IODModuleUsage.Mandatory.description,
                                                                   "ConditionalStatement":"",
                                                                   "Interpretation":"Vendor specific private Tag module"}))
    #add rescale slop and rescale intercept
    VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Rescale Slope",
                                                "Tag":"(0028,1053)",
                                                "Type":DicomTagType.Optional.description,
                                                "Keyword":"RescaleSlope",
                                                "ValueMultiplicity":"1",
                                                "ValueRepresentation":"Decimal String (DS)",
                                                "ExampleValues":"",
                                                "Interpretation":""})))
    VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Rescale Intercept",
                                                "Tag":"(0028,1052)",
                                                "Type":DicomTagType.Optional.description,
                                                "Keyword":"RescaleIntercept",
                                                "ValueMultiplicity":"1",
                                                "ValueRepresentation":"Decimal String (DS)",
                                                "ExampleValues":"",
                                                "Interpretation":""})))
    if "UIH" in manufacturer:
        #UIH use standard DWI tags
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI B-Value",
                                                    "Tag":"(0018,9087)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIBVal",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Gradient Orientation",
                                                    "Tag":"(0018,9089)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIGradientOrientation",
                                                    "ValueMultiplicity":"3",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
    elif "Philips" in manufacturer:
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI B-Value",
                                                    "Tag":"(0018,9087)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIBVal",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Gradient Orientation",
                                                    "Tag":"(0018,9089)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIGradientOrientation",
                                                    "ValueMultiplicity":"3",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        #in some case, Philips use standard dwi tags, but in rare case, they use private tag
        #append DWI attributes
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI B-Value Alt",
                                                           "Tag":"(2001,1003)",
                                                           "Type":DicomTagType.Optional.description,
                                                           "Keyword":"DWIBValAlt",
                                                           "ValueMultiplicity":"1",
                                                           "ValueRepresentation":"Floating Point Single (FL)",
                                                           "ExampleValues":"",
                                                           "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Diffusion Direction",
                                                    "Tag":"(2001,1004)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIDiffusionDirection",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Code String (CS)",
                                                    "ExampleValues":"I",
                                                    "Interpretation":"The possible values for 2001,1004 are P (PreparationDirection), M (MeasurementDirection), S (Selection Direction),O(Oblique Direction), I (Isotropic)"})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Diffusion Direction RL",
                                                    "Tag":"(2005,10B0)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIDiffusionDirectionRL",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Floating Point Single (FL)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Diffusion Direction AP",
                                                    "Tag":"(2005,10B1)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIDiffusionDirectionAP",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Floating Point Single (FL)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Diffusion Direction FH",
                                                    "Tag":"(2005,10B2)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIDiffusionDirectionFH",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Floating Point Single (FL)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        #append T1 attributes
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Number Of Inversion Delays",
                                            "Tag":"(2005,1571)",
                                            "Type":DicomTagType.Optional.description,
                                            "Keyword":"NumberOfInversionDelays",
                                            "ValueMultiplicity":"1",
                                            "ValueRepresentation":"Floating Point Single (FL)",
                                            "ExampleValues":"",
                                            "Interpretation":"Total number of inversion delays"})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Inversion Delay Time",
                                    "Tag":"(2005,1572)",
                                    "Type":DicomTagType.Optional.description,
                                    "Keyword":"InversionDelayTime",
                                    "ValueMultiplicity":"1",
                                    "ValueRepresentation":"Floating Point Single (FL)",
                                    "ExampleValues":"",
                                    "Interpretation":"Inversion Delay Time Stamp"})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Inversion Delay Number",
                            "Tag":"(2005,1573)",
                            "Type":DicomTagType.Optional.description,
                            "Keyword":"InversionDelayNumber",
                            "ValueMultiplicity":"1",
                            "ValueRepresentation":"Floating Point Single (FL)",
                            "ExampleValues":"",
                            "Interpretation":"Index corresponding to Inversion"})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"MR Image Type MR",
                    "Tag":"(2005,1011)",
                    "Type":DicomTagType.Optional.description,
                    "Keyword":"MRImageTypeMR",
                    "ValueMultiplicity":"1-n",
                    "ValueRepresentation":"Code String (CS)",
                    "ExampleValues":"",
                    "Interpretation":"Philips MRI image type, W,F,IP,OP,'T2_STAR','FF'"})))
        #FAT saturation technique
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"MR Fat Saturation Technique",
                    "Tag":"(2005,141A)",
                    "Type":DicomTagType.Optional.description,
                    "Keyword":"MRFatSaturationTechnique",
                    "ValueMultiplicity":"1-n",
                    "ValueRepresentation":"Code String (CS)",
                    "ExampleValues":"SPAIR",
                    "Interpretation":"Fat saturation technique used in Philips"})))
        
    elif "GE" in manufacturer:
        #append DWI attributes
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI B-Value",
                                                            "Tag":"(0043,1039)",
                                                            "Type":DicomTagType.Optional.description,
                                                            "Keyword":"DWIBVal",
                                                            "ValueMultiplicity":"1",
                                                            "ValueRepresentation":"Integer String (IS)",
                                                            "ExampleValues":"",
                                                            "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Gradient Orientation Phase Encoding",
                                                    "Tag":"(0019,10BB)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIGradientOrientationPE",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Decimal String (DS)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Gradient Orientation Frequency Encoding",
                                                    "Tag":"(0019,10BC)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIGradientOrientationFE",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Decimal String (DS)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Gradient Orientation Selection Selection",
                                                    "Tag":"(0019,10BD)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIGradientOrientationSS",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Decimal String (DS)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
    elif "SIEMENS" in manufacturer:
        #append DWI attributes
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Private Creator",
                                                    "Tag":"(0019,0010)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"PrivateCreator",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Long String (LO)",
                                                    "ExampleValues":"SIEMENS MR HEADER",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"CSA Image Header Type",
                                                    "Tag":"(0019,1008)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"CSAImageHeaderType",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Code String (CS)",
                                                    "ExampleValues":"IMAGE NUM 4",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"CSA Image Header Version",
                                                    "Tag":"(0019,1009)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"CSAImageHeaderVersion",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Long String (LO)",
                                                    "ExampleValues":"1.0",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Number Of Images In Mosaic",
                                                    "Tag":"(0019,100A)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"NumberOfImagesInMosaic",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Unlimited Characters (UC)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Slice Measurement Duration",
                                                    "Tag":"(0019,100B)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"SliceMeasurementDuration",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Decimal String (DS)",
                                                    "ExampleValues":"228000.0",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI B-Value",
                                                            "Tag":"(0019,100C)",
                                                            "Type":DicomTagType.Optional.description,
                                                            "Keyword":"DWIBVal",
                                                            "ValueMultiplicity":"1",
                                                            "ValueRepresentation":"Integer String (IS)",
                                                            "ExampleValues":"",
                                                            "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"DWI Diffusion Direction",
                                                    "Tag":"(0019,100D)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"DWIDiffusionDirection",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Code String (CS)",
                                                    "ExampleValues":"I",
                                                    "Interpretation":"The possible values for 2001,1004 are P (PreparationDirection), M (MeasurementDirection), S (Selection Direction),O(Oblique Direction), I (Isotropic)"})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Diffusion Gradient Direction",
                                                            "Tag":"(0019,100E)",
                                                            "Type":DicomTagType.Optional.description,
                                                            "Keyword":"DiffusionGradientDirection",
                                                            "ValueMultiplicity":"3",
                                                            "ValueRepresentation":"Floating Point Double (FD)",
                                                            "ExampleValues":"",
                                                            "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Gradient Mode",
                                                            "Tag":"(0019,100F)",
                                                            "Type":DicomTagType.Optional.description,
                                                            "Keyword":"GradientMode",
                                                            "ValueMultiplicity":"1",
                                                            "ValueRepresentation":"Short String (SH)",
                                                            "ExampleValues":"",
                                                            "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Flow Compensation",
                                                    "Tag":"(0019,1011)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"FlowCompensation",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Short String (SH)",
                                                    "ExampleValues":"No",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Table Position Origin",
                                                    "Tag":"(0019,1012)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"TablePositionOrigin",
                                                    "ValueMultiplicity":"3",
                                                    "ValueRepresentation":"Signed Long (SL)",
                                                    "ExampleValues":"[0, 0, -1773]",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Image Abs Table Position",
                                                    "Tag":"(0019,1013)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"ImaAbsTablePosition",
                                                    "ValueMultiplicity":"3",
                                                    "ValueRepresentation":"Signed Long (SL)",
                                                    "ExampleValues":"[0, 0, -1732]",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Image Relative Table Position",
                                                    "Tag":"(0019,1014)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"ImaRelTablePosition",
                                                    "ValueMultiplicity":"3",
                                                    "ValueRepresentation":"Integer String (IS)",
                                                    "ExampleValues":"[0, 0, 41]",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Slice Position_PCS",
                                                    "Tag":"(0019,1015)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"SlicePosition_PCS",
                                                    "ValueMultiplicity":"3",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"[-184.21510029, -148.375, 103.98487854]",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Time After Start",
                                                    "Tag":"(0019,1016)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"TimeAfterStart",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Decimal String (DS)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Slice Resolution",
                                                    "Tag":"(0019,1017)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"SliceResolution",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Decimal String (DS)",
                                                    "ExampleValues":"1.0",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Real Dwell Time",
                                                    "Tag":"(0019,1018)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"RealDwellTime",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Integer String (IS)",
                                                    "ExampleValues":"1600",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"B_matrix",
                                                    "Tag":"(0019,1027)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"B_matrix",
                                                    "ValueMultiplicity":"6",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"",
                                                    "Interpretation":""})))
        VendorPrivateTreeNode.addChild(DicomStandardTreeNode(DicomAttributeItem(**{"AttributeName":"Bandwidth Per Pixel Phase Encode",
                                                    "Tag":"(0019,1028)",
                                                    "Type":DicomTagType.Optional.description,
                                                    "Keyword":"BandwidthPerPixelPhaseEncode",
                                                    "ValueMultiplicity":"1",
                                                    "ValueRepresentation":"Floating Point Double (FD)",
                                                    "ExampleValues":"29.435",
                                                    "Interpretation":""})))
    return VendorPrivateTreeNode
