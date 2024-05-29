from imgaug import augmenters as iaa

basic_aug = [iaa.Affine(rotate=45),
             iaa.AdditiveGaussianNoise(scale=0.2 * 255),
             iaa.Add(50, per_channel=True),
             iaa.Sharpen(alpha=0.5)]

