import napari
import torch
import sys
sys.path.append("/Users/whoisv/cell-AAP/cell_AAP/")
import numpy as np
import os
import re
import cv2
import pathlib
import tifffile as tiff
from detectron2.utils.logger import setup_logger
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from data_module import annotation_utils as au   # type: ignore
from magicclass import magicclass, field, MagicTemplate
from magicclass.widgets import PushButton, CheckBox, Slider, FileEdit, FloatSlider
from magicclass.utils import thread_worker


setup_logger()
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
model = "/Users/whoisv/cell-AAP/models/20240520_140429_1.8"
model_version = "final"
cfg = get_cfg()
cfg.merge_from_file(model + "/config.yaml")
cfg.MODEL.WEIGHTS = os.path.join(model, f"model_{model_version}.pth")
cfg.MODEL.DEVICE = "cpu"
cellseg_metadata = MetadataCatalog.get("cellseg_train_1.8")



@magicclass
class CCSN_GUI(MagicTemplate):
    """
    Napari GUI for CCSN instance segmentation algorithim
    -----------------------------------------------------
    """

    def __init__(self, viewer: napari.Viewer, cfg):
        super().__init__()
        self.viewer = viewer
        self.cfg = cfg


    @magicclass(layout="vertical")
    class Field_2:
        image_selector = field(FileEdit, name="Select Image")
        path_selector = field(FileEdit, name="Save Inference at", options = {"mode" : "d"})
        save_box = field(CheckBox, name="Save Inference")

    @magicclass
    class Field_1:
        threshold_slider = field(
            FloatSlider, name="Confidence Threshold", options={"min": 0, "max": 1}
        )
        confluency_estimate = field(
            Slider, name = 'Number of Cells (Approx.)', options = {"min":0, "max":2000}
        )
        display_button = field(PushButton, name="Display")
        inference_button = field(PushButton, name="Inference")


    def _configure(self):
        if self.Field_1.confluency_estimate.value:
            self.cfg.TEST.DETECTIONS_PER_IMAGE = self.Field_1.confluency_estimate.value
        if self.Field_1.threshold_slider.value:
            self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.Field_1.threshold_slider.value

        

    @Field_1.inference_button.connect
    @thread_worker(progress = {'desc' : 'Running Inference....'}, force_async=True)
    def _inference(self):
        """
        Runs inference on image returned by self._image_select(), saves inference result if self._save_select() == True
        ----------------------------------------------------------------------------------------------------------------
        """

        _, im_array = self._image_select()
        mask_array = []
        self._configure()
        self.predictor = DefaultPredictor(self.cfg)
        if len(im_array.shape) == 3:
            for frame in range(im_array.shape[0]):
                img = au.bw_to_rgb(im_array[frame].astype("float32"))
                output = self.predictor(img)
                segmentations = np.asarray(output["instances"].pred_masks.to("cpu"))
                num_masks = segmentations.shape[0]
                labels = np.linspace(1, num_masks, num_masks)
                segmentations = [l * m for l, m in zip(labels, segmentations)]
                segmentations = np.sum(segmentations, axis = 0)
                mask_array.append(segmentations.astype('uint8'))


        elif len(im_array.shape) == 2:
            img = au.bw_to_rgb(im_array.astype("float32"))
            output = self.predictor(img)
            segmentations = np.asarray(output["instances"].pred_masks.to("cpu"))
            num_masks = segmentations.shape[0]
            labels = np.linspace(1, num_masks, num_masks)
            segmentations = [l * m for l, m in zip(labels, segmentations)]
            segmentations = np.sum(segmentations, axis = 0)
            mask_array = segmentations.astype('uint8')


        save_mask, filepath = self._save_select()
        name, _ = self._image_select()
        name = name.replace(".", "/").split("/")[-2]
        if save_mask == True:
            if filepath == pathlib.Path("default/path"):
                filepath = os.getcwd()
            tiff.imwrite(
                os.path.join(filepath, f"{model}_{model_version}_{name}_.tif"),
                mask_array.astype("uint8"),
                compression="jpeg",
                compressionargs={"level": 20},
            )

        label_mapping = metadata_generator(output)


        mask_array = np.array(mask_array)
        return mask_array, name, label_mapping
    
 
    @_inference.returned.connect
    def _view_inference(self, output_tup):
        mask_array, name, label_mapping = output_tup
        inference_result = self.viewer.add_labels(mask_array, name=f"{name}_inference", metadata=label_mapping)
        return inference_result

    def _save_select(self):
        """
        Returns the truth value of the save box selector and the path for which the inference result should be saved to
        ---------------------------------------------------------------------------------------------------------------
        """
        return self.Field_2.save_box.value, self.Field_2.path_selector.value

    def _image_select(self):
        """
        Returns the path selected in the image selector box and the array corresponding the to path
        -------------------------------------------------------------------------------------------
        """
        if (
            re.search(
                r"^.+\.(?:(?:[tT][iI][fF][fF]?)|(?:[tT][iI][fF]))$",
                str(self.Field_2.image_selector.value),
            )
            == None
        ):
            layer_data = cv2.imread(
                                    str(self.Field_2.image_selector.value), 
                                    cv2.IMREAD_GRAYSCALE
                                    )
        else:
            layer_data = tiff.imread(
                                    self.Field_2.image_selector.value
                                    )


        return str(self.Field_2.image_selector.value), layer_data
    

    @Field_1.display_button.connect
    def _view_file(self):
        """
        Displays file in Napari gui if file has been selected, also returns the 'name' of the image file
        ------------------------------------------------------------------------------------------------
        """
        if self._image_select():
            name, layer_data = self._image_select()
            name = name.replace(".", "/").split("/")[-2]
            viewer.add_image(layer_data, name=name)
        else:
            raise ValueError
        


def metadata_generator(output):
    label_mapping = {}
    count = 0
    for label in np.array(output['instances'].pred_classes.to('cpu')):
        count += 1
        if label == 0:
            label_mapping.update({count : 'non-mitotic'})
        elif label == 1:
            label_mapping.update({count: 'mitotic'})

    return label_mapping

if __name__ == "__main__":
    viewer = napari.Viewer()
    viewer.window.add_dock_widget(CCSN_GUI(viewer, cfg), area="right")
    napari.run()
