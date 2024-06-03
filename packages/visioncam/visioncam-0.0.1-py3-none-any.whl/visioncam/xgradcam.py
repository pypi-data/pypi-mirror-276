from visioncam.base import Base
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize

class XgradCAM(Base):
    
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
      weights = tf.reduce_mean(grads, axis=(0, 1, 2))
      
      X_weights = tf.reduce_sum(grads * conv_outs, axis=(0, 1, 2))
      X_weights = X_weights / (tf.reduce_sum(conv_outs, axis=(0, 1, 2)) + 1e-8)

      last_conv_layer_output = conv_outs[0]
      X_cam = tf.matmul(last_conv_layer_output, X_weights[..., tf.newaxis])

      X_cam = tf.squeeze(X_cam)

      X_cam = tf.maximum(X_cam, 0) / tf.reduce_max(X_cam)

      return X_cam.numpy()
