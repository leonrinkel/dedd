# dirty helper adapted from pipeline.py, use somewhat like this:
#
# docker run \
# --rm -it \
# -v somepath:/input \
# -v somepath:/output \
# -v `pwd`/helper:/helper \
# mesonet \
# python3.5 MesoNetHelper.py meso.json 100

import os
import sys
import glob
import json
import time
import numpy as np

sys.path.append("/app")
from classifiers import *
from pipeline import *

models = [
    (Meso4, ["weights/Meso4_DF.h5", "weights/Meso4_F2F.h5"]),
    (MesoInception4, ["weights/MesoInception_DF.h5", "weights/MesoInception_F2F.h5"]),
]
outputs = []

def predict(model, input_path, stop):
    face_finder = FaceFinder(input_path, load_first_face=False)
    face_finder.find_faces(resize=0.5, skipstep=0, stop=stop)
    gen = FaceBatchGenerator(face_finder)
    return predict_faces(gen, model)

def main(predictions_file_name, number_of_frames):
    for model_class, weights_files in models:
        model = model_class()
        model_name = model_class.__name__

        for weights_file in weights_files:
            model.load(weights_file)

            for input_path in glob.glob("/input/*.MP4"):
                start_time = time.time()
                predictions = predict(model, input_path, number_of_frames)
                end_time = time.time()

                output_item = {
                    "modelName": model_name,
                    "weightsFile": weights_file,
                    "inputPath": input_path,
                    "predictions": np.squeeze(predictions).tolist(),
                    "secondsTime": end_time - start_time,
                }
                outputs.append(output_item)

    predictions_path = os.path.join("/output", predictions_file_name)
    with open(predictions_path, "w") as output_file:
        json.dump(outputs, output_file, indent=4)

if __name__ == "__main__":
    main(
        predictions_file_name=sys.argv[1],
        number_of_frames=int(sys.argv[2]))
