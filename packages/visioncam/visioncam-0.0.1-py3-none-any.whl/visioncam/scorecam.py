from visioncam.base import Base
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import cv2

class ScoreCaM(Base):
    
    def __init__(self, model, class_idx, layer_name=None):
        
        Base.__init__(self , model , layer_name )
        self.class_idx=class_idx


    def softmax(self,x):
      f = np.exp(x)/np.sum(np.exp(x), axis = 1, keepdims = True)
      return f   

    def compute_cam_features(self, image, max_N =-1):
        img_array = tf.cast(image, tf.float32)
        cls = np.argmax(self.model.predict(img_array))

        grad_model = tf.keras.models.Model(inputs=self.model.inputs,
                                           outputs=self.model.get_layer(self.layer_name).output)

        act_map_array  = grad_model.predict(img_array)
        if max_N != -1:
            act_map_std_list = [np.std(act_map_array[0,:,:,k]) for k in range(act_map_array.shape[3])]
            unsorted_max_indices = np.argpartition(-np.array(act_map_std_list), max_N)[:max_N]
            max_N_indices = unsorted_max_indices[np.argsort(-np.array(act_map_std_list)[unsorted_max_indices])]
            act_map_array = act_map_array[:,:,:,max_N_indices]

        input_shape = self.model.layers[0].output_shape[0][1:]  
        act_map_resized_list = [cv2.resize(act_map_array[0,:,:,k], input_shape[:2], interpolation=cv2.INTER_LINEAR) for k in range(act_map_array.shape[3])]
        act_map_normalized_list = []
        for act_map_resized in act_map_resized_list:
            if np.max(act_map_resized) - np.min(act_map_resized) != 0:
                act_map_normalized = act_map_resized / (np.max(act_map_resized) - np.min(act_map_resized))
            else:
                act_map_normalized = act_map_resized
            act_map_normalized_list.append(act_map_normalized)
        masked_input_list = []
        for act_map_normalized in act_map_normalized_list:
            masked_input = np.copy(img_array)
            for k in range(3):
                masked_input[0,:,:,k] *= act_map_normalized
            masked_input_list.append(masked_input)
        masked_input_array = np.concatenate(masked_input_list, axis=0)
        pred_from_masked_input_array = self.softmax(self.model.predict(masked_input_array))
        weights = pred_from_masked_input_array[:,cls]
        cam = np.dot(act_map_array[0,:,:,:], weights)
        cam = np.maximum(0, cam)  
        cam /= np.max(cam)  

        
        return cam