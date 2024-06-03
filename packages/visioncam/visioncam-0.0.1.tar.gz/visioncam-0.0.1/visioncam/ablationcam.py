import numpy as np
import tensorflow as tf
from keras.applications.xception import preprocess_input
from tensorflow.keras.preprocessing.image import load_img,img_to_array,array_to_img
from tensorflow import keras
from IPython.display import Image
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from visioncam.base import Base

class AblationCAM(Base):
    def __init__(self, model,last_conv_layer_name,classifier_layer_names):
        
        self.model = model
        self.last_conv_layer_name=last_conv_layer_name
        self.classifier_layer_names=classifier_layer_names
        
    def get_image(image_path,img_size):
        orig = load_img(image_path, target_size=img_size)
        image = img_to_array(orig)
        image = np.expand_dims(image, axis=0)
        img_array =preprocess_input(image)
        return img_array

    def compute_cam_features(self, img):
        preds = self.model.predict(img)
        last_conv_layer = self.model.get_layer(self.last_conv_layer_name)
        last_conv_layer_model = keras.Model(self.model.inputs, last_conv_layer.output)
        classifier_input = keras.Input(shape=last_conv_layer.output.shape[1:])
        x = classifier_input
        for layer_name in self.classifier_layer_names:
            x = self.model.get_layer(layer_name)(x)
        classifier_model = keras.Model(classifier_input, x)
        activations = last_conv_layer_model.predict(img) 
        last_layer_activation = activations[-1]

        

        last_layer_activation = np.expand_dims(last_layer_activation,axis=0)
        heatmap = np.mean(last_layer_activation, axis=-1)
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
        values = []
        
        for i in range(last_layer_activation.shape[-1]):
          activations = last_conv_layer_model.predict(img) 
          last_layer_activation = activations[-1]
          activation = last_layer_activation
          activation = np.expand_dims(activation,axis=0)
          jj = int(last_layer_activation.shape[0])
          kk = int(last_layer_activation.shape[1])
          
          for j in range(jj):
            for k in range(kk):
              activation[0][j][k][i]=0.
          prediction = classifier_model(activation)
          a= prediction[0][404]
          values.append(a.numpy())

        aero = 0.8209318
        aero = [aero]*last_layer_activation.shape[-1]
        weight_ratio = []
        for i in range(last_layer_activation.shape[-1]):
          b= (float(aero[i]) - float(values[i]))/float(aero[i])
          weight_ratio.append(b)
        last_layer_activation = np.expand_dims(last_layer_activation,axis=0)
        for i in range(last_layer_activation.shape[-1]):
          for  j in range(last_layer_activation.shape[1]):
            for k in range(last_layer_activation.shape[2]):
              last_layer_activation[0][j][k][i]=last_layer_activation[0][j][k][i]*weight_ratio[i]

        heatmap = np.mean(last_layer_activation, axis=-1)
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
        heatmap=heatmap[0,:,:,]
        
        return heatmap
