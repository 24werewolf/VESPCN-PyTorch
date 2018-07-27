import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math

mean_RGB = np.array([123.68 ,  116.779,  103.939])

def preprocess(img):
    return (img - mean_RGB)/255

def postprocess(img):
    if img.shape[2] == 3:
        mean_RGB = np.array([123.68, 116.779, 103.939])
        out = img.squeeze(axis=0).transpose((1, 2, 0))
        out = np.round(np.clip(out * 255 + mean_RGB, 0, 255))
    else:
        mean_YCbCr = np.array([109])
        out = img.squeeze(axis=0).transpose((1, 2, 0))
        out = np.round(np.clip(out * 255 + mean_YCbCr, 0, 255))
    return out

def calc_PSNR(img1, img2):
    min_H = min(img1.shape[0], img2.shape[0])
    min_W = min(img1.shape[1], img2.shape[1])
    #assume RGB image
    target_data = np.array(img1[0:min_H, 0:min_W, :], dtype=np.float64)
    ref_data = np.array(img2[0:min_H, 0:min_W, :], dtype=np.float64)
    diff = ref_data - target_data
    diff = diff.flatten('C')
    rmse = math.sqrt(np.mean(diff ** 2.))
    if rmse == 0:
        return 100
    else:
        return 20*math.log10(255.0/rmse)