from MesoNet.classifiers import *
import glob
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import lime
from lime import lime_image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

model = Meso4()
model.load('MesoNet/weights/Meso4_DF.h5')

images_path = '/images'
num_images = len(list(glob.glob(f'{images_path}/*/*.jpg')))

dataGenerator = ImageDataGenerator(rescale=1./255)
generator = dataGenerator.flow_from_directory(
    images_path,
    target_size=(256, 256),
    batch_size=1,
    class_mode='binary',
    subset='training',
)

for i in range(num_images):
    X, y = generator.next()

    label = 'Fake' if y[0] == 0 else 'Real'
    prediction = 'Fake' if model.predict(X)[0, 0] <= 0.5 else 'Real'

    plt.subplot(1, 2, 1)
    plt.title(label)
    plt.imshow(X.reshape((256, 256, 3)))

    explainer = lime_image.LimeImageExplainer()
    explanation = explainer.explain_instance(X[0].astype('double'), model.predict)    

    ind = explanation.top_labels[0]
    dict_heatmap = dict(explanation.local_exp[ind])
    heatmap = np.vectorize(dict_heatmap.get)(explanation.segments)
    
    plt.subplot(1, 2, 2)
    plt.title(f'Prediction: {prediction}')
    plt.imshow(heatmap, cmap='RdBu', vmin=-heatmap.max(), vmax=heatmap.max())
    plt.savefig(f'{images_path}/heatmap{i}.png')