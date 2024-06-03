from visioncam.base import Base
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize

class HriesCAM(Base):
    
    def __init__(self, model, class_idx, layer_name=None):
        
        Base.__init__(self , model , layer_name )
        self.class_idx=class_idx

        
    def compute_cam_features(self, image):

        grad_model = tf.keras.models.Model(inputs=[self.model.inputs],
                                           outputs=[self.model.get_layer(self.layer_name).output, self.model.output])
        with tf.GradientTape() as tape:
            inputs = tf.cast(image, tf.float32)
            conv_outs, predictions = grad_model(inputs)
            y_c = predictions[:, self.class_idx]

        grads = tape.gradient(y_c, conv_outs) 
        
        last_conv_layer_output = conv_outs[0]
       
        
        heatmap = last_conv_layer_output * grads
        heatmap = np.sum(heatmap, axis=-1)
        heatmap = tf.squeeze(heatmap)

        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        return heatmap.numpy()