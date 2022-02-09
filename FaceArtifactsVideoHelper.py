import os
import glob
import time

output_dir = 'C:\\Users\\leon\\Desktop\\facearttest'

path_pattern = 'X:\\FBCC\\*\\*\\*.MP4'
for input_path in glob.glob(path_pattern):
    output_path = os.path.join(output_dir, os.path.basename(input_path))
    trim_cmd = \
        f'ffmpeg.exe -i {input_path} ' \
        f'-vf select="between(n\,0\,100),setpts=PTS-STARTPTS" ' \
        f'-an {output_path}'
    predict_cmd = \
        f'docker run --rm -it -v {output_dir}:/data ' \
        f'leonrinkel/cvprw2019-face-artifacts ' \
        f'python ./demo.py --input_dir=/data'

    start = time.time()
    os.system(trim_cmd)
    log = os.popen(predict_cmd).read()
    stop = time.time()

    os.remove(output_path)

    subset = os.path.basename(os.path.abspath(os.path.join(input_path, os.path.pardir, os.path.pardir)))
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f'{subset}_{filename}.log')
    with open(output_path, 'w') as output_file:
        output_file.write(log)
        output_file.write(f'time it took: {stop - start}')
