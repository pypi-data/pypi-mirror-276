# processor-class
class ImageProcessor(object):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.brain_vol_dict = {}

    def convert_dicom_folder_to_nifti(self, dicom_directory, nifti_directory, *_):
        # load the data
        import os
        import time
        import dicom2nifti
        import dicom2nifti.settings as settings
        
        settings.disable_validate_orthogonal()
        settings.enable_resampling()
        settings.set_resample_spline_interpolation_order(1)
        settings.set_resample_padding(-1000)

        if not os.path.exists(nifti_directory): os.mkdir(nifti_directory)
    
        now = time.time()
        dicom2nifti.convert_directory(dicom_directory, nifti_directory)
        time_elapsed = time.time() - now
        print(f'Time elapsed:{time_elapsed}')

    def get_brain_vol_dict(self, nifti_file_paths_list, *_):
        import os
        for path in nifti_file_paths_list:
            brain_vol = self.get_brain_vol(path)
            _, tail = os.path.split(path)
            self.brain_vol_dict[tail] = brain_vol

    def get_brain_vol(self, nifti_path_brain_vol, *_):

        import nibabel as nib
        brain_vol = nib.load(nifti_path_brain_vol)
        brain_vol_data = brain_vol.get_fdata()

        return brain_vol_data












