# dirty helper adapted from demo.py, use somewhat like this:
#
# docker run \
# --rm -it \
# -v somepath:/data \
# -v `pwd`:/helper \
# cvprw2019-face-artifacts \
# python FaceArtifactsFrameHelper.py warp.json

import os
import cv2
import sys
import glob
import time
import json
import yaml
import dlib
import numpy as np
import tensorflow as tf
from easydict import EasyDict as edict

sys.path.append("/app")
from solver import Solver
from py_utils.face_utils import lib
from resolution_network import ResoNet

cfg_file = "cfgs/res50.yml"
with open(cfg_file, "r") as f:
    cfg = edict(yaml.load(f))

sample_num = 10
front_face_detector = dlib.get_frontal_face_detector()
lmark_predictor = dlib.shape_predictor("/app/dlib_model/shape_predictor_68_face_landmarks.dat")
tfconfig = tf.ConfigProto(allow_soft_placement=True)
tfconfig.gpu_options.allow_growth = True
sess = tf.Session(config=tfconfig)
reso_net = ResoNet(cfg=cfg, is_train=False)
reso_net.build()
solver = Solver(sess=sess, cfg=cfg, net=reso_net)
solver.init()

def main(predictions_file_name):
    output = {
        "modelName": "WarpRes50",
        "predictions": [],
    }
    start_time = time.time()

    for sample_path in glob.glob("/data/*.png"):
        sample_name = os.path.basename(sample_path)

        prob, max_prob = -1, -1
        sample = cv2.imread(sample_path)
        face_info = lib.align(sample[:, :, (2,1,0)], front_face_detector, lmark_predictor)
        for _, point in face_info:
            rois = []
            for i in range(sample_num):
                roi, _ = lib.cut_head([sample], point, i)
                rois.append(cv2.resize(roi[0], tuple(cfg.IMG_SIZE[:2])))
            prob = solver.test(rois)
            prob = np.mean(np.sort(prob[:, 0])[np.round(sample_num / 2).astype(int):])
            if prob >= max_prob: max_prob = prob

        prediction = {
            "sample": sample_name,
            "probability": str(prob),
        }
        output["predictions"].append(prediction)

    end_time = time.time()
    output["secondsTime"] = end_time - start_time

    predictions_path = os.path.join("/data", predictions_file_name)
    with open(predictions_path, "w") as output_file:
        json.dump(output, output_file, indent=4)

if __name__ == "__main__":
    main(predictions_file_name=sys.argv[1])
