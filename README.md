# Discrimination Evaluation of Deepfake Detectors

`CsvAnalysis.ipynb` can be used to filter prediction results in the form of CSV files by labels.

## MesoNet

I used commit `f3aa786e8f87e0894dcf36f6dba2f77a25293566` of [DariusAf/MesoNet](https://github.com/DariusAf/MesoNet), as well as the `Dockerfile` and `requirements.txt` file in the `MesoNet` subdirectory to run the MesoNet model in a Docker container. The image can be built and run like so:

```
$ docker build -t mesonet .
$ docker run \
    --rm -it --gpus all \
    -v `pwd`/test_images:/app/test_images \
    -v `pwd`/test_videos:/app/test_videos \
    mesonet \
    python example.py
```

`MesoNetHelper.py` has been used to predict a bunch of videos using all four MesoNet variants. The `MesoNet` subdirectory also contains prediction results and a list of false positives in the form of CSV files. `ConvertMesoNetJsonsToCsvs.ipynb` has been used to produce this files.

## FaceArtifacts

I used commit `4f15d70485321179d3eafeb8718940d23f5b4b3b` of [yuezunli/CVPRW2019_Face_Artifacts](https://github.com/yuezunli/CVPRW2019_Face_Artifacts), as well as the `Dockerfile` and `requirements.txt` file in the `FaceArtifacts` subdirectory to run the FaceArtifacts model in a Docker container. The image can be built and run like so:

```
$ docker build -t cvprw2019-face-artifacts .
$ docker run \
    --rm -it \
    -v `pwd`/demo:/demo \
    cvprw2019-face-artifacts \
    python ./demo.py --input_dir=/demo
```

`FaceArtifactsFrameHelper.py` has been used to predict a bunch of cropped frames using the FaceArtifacts model. Faces were cropped out using a [dlib face detector](http://dlib.net/face_detector.py.html). `FaceArtifactsVideoHelper.py` has been used to trim and predict a bunch of videos. The `FaceArtifacts` subdirectory also contains prediction results and a list of false positives in the form of CSV files. `FaceArtifactsLogsToCsvs.ipynb` has been used to produce this files. `CroppedFaceArtifactsJsonsToCsvs.ipynb` has been used to produce this files for the cropped variant.

## Seferbekov

I used commit `89c6290490bac96b29193a4061b3db9dd3933e36` of [https://github.com/selimsef/dfdc_deepfake_challenge](selimsef/dfdc_deepfake_challenge). It already comes with a `Dockerfile`, but I added one line, to include weights in the image building. The customized `Dockerfile` is included in the `Seferbekov` subdirectory. The image can be built and run like so:

```
$ docker build -t dfdc-deepfake-challenge .
$ docker run \
    --rm -it --gpus all \
    -v `pwd`/videos:/videos \
    dfdc-deepfake-challenge \
    ./predict_submission.sh /videos /videos/result.csv
```

`MergeSeferbekovCsvFiles.ipynb` has been used to merge multiple CSV files that the Seferbekov detector produces.
