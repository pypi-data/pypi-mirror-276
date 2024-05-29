from .tool import *
import imgaug as ia
import numpy as np
import shutil
from tqdm import tqdm
from PIL import Image
from imgaug import augmenters as iaa

ia.seed(1)


def aug(IMG_DIR, XML_DIR, AUG_XML_DIR, AUG_IMG_DIR, AUGLOOP, AUGCONF):

    boxes_img_aug_list = []
    new_bndbox_list = []

    seq = iaa.Sequential(AUGCONF)

    try:
        desc = f'{os.path.normpath(IMG_DIR).split(os.sep)[-2]} Augmenting'
    except:
        desc = f'Augmenting'

    for name in tqdm(os.listdir(XML_DIR), desc=desc):

        bndbox = read_xml_annotation(XML_DIR, name)

        shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)

        og_img = Image.open(IMG_DIR + '/' + name[:-4] + '.jpg')
        og_img.convert('RGB').save(AUG_IMG_DIR + name[:-4] + '.jpg', 'JPEG')
        og_xml = open(os.path.join(XML_DIR, name))
        tree = ET.parse(og_xml)

        elem = tree.find('filename')
        elem.text = (name[:-4] + '.jpg')
        tree.write(os.path.join(AUG_XML_DIR, name))

        for epoch in range(AUGLOOP):
            seq_det = seq.to_deterministic()

            img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))

            img = np.asarray(img)

            for i in range(len(bndbox)):
                bbs = ia.BoundingBoxesOnImage([
                    ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                ], shape=img.shape)

                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                boxes_img_aug_list.append(bbs_aug)

                n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                if n_x1 == 1 and n_x1 == n_x2:
                    n_x2 += 1
                if n_y1 == 1 and n_y2 == n_y1:
                    n_y2 += 1
                if n_x1 >= n_x2 or n_y1 >= n_y2:
                    print('error', name)
                new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])

            image_aug = seq_det.augment_images([img])[0]
            path = os.path.join(AUG_IMG_DIR,
                                str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            image_auged = bbs.draw_on_image(image_aug, size=0)
            Image.fromarray(image_auged).convert('RGB').save(path)

            change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                       str(name[:-4]) + '_' + str(epoch))

            new_bndbox_list = []

