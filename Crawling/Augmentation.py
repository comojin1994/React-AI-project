import cv2
from glob import glob
import numpy as np

def fill(img, h, w):
    img = cv2.resize(img, (h, w), cv2.INTER_CUBIC)
    return img

def rotate(img, angle):
    h, w, c = img.shape
    matrix = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    img = cv2.warpAffine(img, matrix, (w, h))
    img = fill(img, h, w)
    return img

def chageBright(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
    return img

def zoom(img, value):
    value = np.random.uniform(value, 1)
    h, w = img.shape[:2]
    h_taken = int(value * h)
    w_taken = int(value * w)
    h_start = np.random.randint(0, h - h_taken)
    w_start = np.random.randint(0, w - w_taken)
    img = img[h_start:h_start + h_taken, w_start:w_start + w_taken, :]
    img = fill(img, h, w)
    return img

def augmentation(path, p):
    img = cv2.imread(path)
    img = img.astype(np.float32)

    img = chageBright(img, np.random.randint(-50, 150)) if np.random.random(1) > p else img
    img = rotate(img, np.random.randint(-45, 45)) if np.random.random(1) > p else img
    img = cv2.flip(img, np.random.randint(-2, 2)) if np.random.random(1) > p else img
    img = zoom(img, np.random.uniform(0, 1)) if np.random.random(1) > p else img

    # plt.imshow(img/255.)
    # plt.show()
    return img

def main():
    TOTAL_DATA = 300
    IMAGE_PATH = f'./Data'
    FOODS = glob(f'{IMAGE_PATH}/*')

    for FOOD in FOODS:
        print('=' * 30)
        print(f'Start {FOOD}')
        flag = False
        idx = 0
        imageList = glob(f'{FOOD}/*.jpg')

        while len(glob(f'{FOOD}/*.jpg')) < TOTAL_DATA:
            for img_path in imageList:
                if len(glob(f'{FOOD}/*.jpg')) >= TOTAL_DATA:
                    print(f'STOP : ', len(glob(f'{FOOD}/*.jpg')))
                    flag = True
                    break
                img = augmentation(img_path, 0.5)
                cv2.imwrite('.' + img_path.split('.')[1] + '_' + str(idx) + '.jpg', img)
                idx += 1
                print('.', end='')
            if flag: break


        print(f'End {FOOD}')
        print('=' * 30)
        print('\n')

def test():
    IMAGE_PATH = f'./Data'
    FOODS = glob(f'{IMAGE_PATH}/*')

    for FOOD in FOODS:
        imageList = glob(f'{FOOD}/*.jpg')
        print(f'{FOOD} img numbers : ', len(imageList))

if __name__ == '__main__':
    main()
    test()