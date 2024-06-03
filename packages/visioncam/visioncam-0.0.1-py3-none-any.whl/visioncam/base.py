import tensorflow as tf
from tensorflow.keras.applications import imagenet_utils
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import keras
from IPython.display import Image, display
import matplotlib as mpl
import keras


class Base:
    def __init__(self, model, layer_name=None):
        self.model = model
        self.layer_name = layer_name

        
        if not layer_name:
            self.layer_name = self.find_target_layer()

    def find_target_layer(self):
        for layer in reversed(self.model.layers):
            if len(layer.output_shape) == 4:
                return layer.name
        raise ValueError('Could not find 4D layer. Cannot apply CAM .')
    
    @staticmethod
    def get_img_array(img_path, target_size = (299,299,3)):
        img = keras.utils.load_img(img_path, target_size=target_size)
        array = keras.utils.img_to_array(img)
        array = np.expand_dims(array, axis=0)
        return array

    def compute_cam_features(self, image):
        cam_model = tf.keras.models.Model(inputs=[self.model.inputs],
                                          outputs=[self.model.get_layer(self.layer_name).output, self.model.output])
        features, outputs = cam_model.predict(image)
        global_avg_pool_weights = self.model.layers[-1].get_weights()[0]
        image_feature = features[0]
        cam_features = resize(image_feature, (224, 224))
        pred = np.argmax(outputs[0])
        cam_weights = global_avg_pool_weights[:, pred]
        heatmap = np.dot(cam_features, cam_weights)
        return heatmap

    
    @staticmethod
    def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
        img = keras.utils.load_img(img_path)
        img = keras.utils.img_to_array(img)

        heatmap = np.uint8(255 * heatmap)

        jet = mpl.colormaps["jet"]

        jet_colors = jet(np.arange(256))[:, :3]
        jet_heatmap = jet_colors[heatmap]

        jet_heatmap = keras.utils.array_to_img(jet_heatmap)
        jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
        jet_heatmap = keras.utils.img_to_array(jet_heatmap)

        superimposed_img = jet_heatmap * alpha + img
        superimposed_img = keras.utils.array_to_img(superimposed_img)

        superimposed_img.save(cam_path)

        display(Image(cam_path))
