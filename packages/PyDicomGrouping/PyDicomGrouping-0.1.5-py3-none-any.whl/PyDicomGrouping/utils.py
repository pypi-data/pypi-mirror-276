from typing import Union
import pickle
from pathlib import Path
import os
import numpy as np
import nibabel as nib

def pickle_load(path:Union[str, Path, os.PathLike]):
    with open(path, 'rb') as cache_f:
        res = pickle.load(cache_f)
    return res

def pickle_dump(obj, path:Union[str, Path, os.PathLike]):
    with open(path,'wb') as cache_f:
        pickle.dump(obj, cache_f)

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