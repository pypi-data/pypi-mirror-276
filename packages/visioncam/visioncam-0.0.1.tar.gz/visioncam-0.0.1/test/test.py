# Import libraries
from visioncam.xgradcam import XgradCAM
import keras
from keras.applications import Xception
import matplotlib.pyplot as plt

# Build Your Model
model = Xception(weights="imagenet")

# Preapare Images
image = XgradCAM.get_img_array(img_path = '/content/sample.jpg',target_size = (299,299,3) )

# Model Predcition
preds = model.predict(image)
class_idx = np.argmax(preds[0])

# Define index for your classes
class_index = {'tiger_cat': 282, 'beagle': 162 ,'african_elephant' : 386 , 'bird' : 10 }

# For All Methods
grad_cam = XgradCAM(model ,class_index['tiger_cat'] )

# For AblationCAM
last_conv_l_name = "block14_sepconv2_act"
classifier_l_names = ["avg_pool","predictions"]
grad_cam = AblationCAM(model,last_conv_layer_name = last_conv_l_name, classifier_layer_names = classifier_l_names )

preprocess_input = keras.applications.xception.preprocess_input
img_array = preprocess_input(image)
grad_heatmap = grad_cam.compute_cam_features(img_array)
plt.imshow(grad_heatmap)

XgradCAM.save_and_display_gradcam('/content/sample.jpg', grad_heatmap)