from visioncam.base import Base
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize

class SmoothGradCAMPlusPlus(Base):
    
    def init(self, model, class_idx, layer_name=None):
        
        Base.init(self , model , layer_name )
        self.class_idx=class_idx
        
        
    def get_grad_cam_plus_plus(self, image):

        grad_model = tf.keras.models.Model(inputs=[self.model.inputs],
                                           outputs=[self.model.get_layer(self.layer_name).output, self.model.output])
        with tf.GradientTape() as gtape1:
          with tf.GradientTape() as gtape2:
            with tf.GradientTape() as gtape3:
                img_tensor = tf.cast(image, tf.float32)
                conv_output, predictions = grad_model(img_tensor)
                output = predictions[:, self.class_idx]
                conv_first_grad = gtape3.gradient(output, conv_output)
            conv_second_grad = gtape2.gradient(conv_first_grad, conv_output)
        conv_third_grad = gtape1.gradient(conv_second_grad, conv_output)

        global_sum = np.sum(conv_output, axis=(0, 1, 2))
        alpha_num = conv_second_grad[0]
        alpha_denom = conv_second_grad[0]*2.0 + conv_third_grad[0]*global_sum
        alpha_denom = np.where(alpha_denom != 0.0, alpha_denom, 1e-10)

        alphas = alpha_num/alpha_denom
        alpha_normalization_constant = np.sum(alphas, axis=(0,1))
        alphas /= alpha_normalization_constant

        weights = np.maximum(conv_first_grad[0], 0.0)

        deep_linearization_weights = np.sum(weights*alphas, axis=(0,1))
        grad_cam_map = np.sum(deep_linearization_weights*conv_output[0], axis=2)

        heatmap = np.maximum(grad_cam_map, 0)
        max_heat = np.max(heatmap)
        if max_heat == 0:
           max_heat = 1e-10
        heatmap /= max_heat
        return heatmap
        
    def compute_cam_features(self, image,n_samples=25, stdev_spread=0.15):
        stdev = stdev_spread / (image.max() - image.min())
        std_tensor = np.ones_like(image) * stdev
        total_cams = 0

        for i in range(n_samples):
            x_with_noise = image + np.random.normal(0, stdev, image.shape)
            smg_cam = self.get_grad_cam_plus_plus(x_with_noise)
            total_cams += smg_cam

        total_cams /= self.n_samples
        return total_cams