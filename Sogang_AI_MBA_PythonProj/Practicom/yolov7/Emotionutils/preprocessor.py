import numpy as np
# from scipy.misc import imread, imresize
# from scipy.misc import imresize
# pip install imageio
# scipy.misc.imread 함수는 이전 버전의 SciPy에서 이미지를 읽기 위해 사용되었습니다. 그러나 SciPy 1.2.0 이후로 이 함수는 더 이상 사용되지 않으며 최종적으로 SciPy 1.3.0에서 제거되었습니다. 이미지를 읽기 위해 대신 imageio.imread를 사용하는 것이 권장됩니다.
import imageio
from skimage.transform import resize

def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x

def _imread(image_name):
        # return imread(image_name)
        return imageio.imread(image_name)

def _imresize(image_array, size):
        # return imresize(image_array, size)
        return resize(image_array, size)

def to_categorical(integer_classes, num_classes=2):
    integer_classes = np.asarray(integer_classes, dtype='int')
    num_samples = integer_classes.shape[0]
    categorical = np.zeros((num_samples, num_classes))
    categorical[np.arange(num_samples), integer_classes] = 1
    return categorical

