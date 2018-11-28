import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import json
import pickle

from analyze_detection import compute_precision_recall
from analyze_image_detection_one_guess_per_image import compute_precision_recall_with_images
from analyze_sequence_detection_one_guess_per_sequence import compute_precision_recall_with_sequences

det_folder = '/home/ubuntu/efs/models/train_on_eccv_and_imerit_2/predictions/'
#det_folder = '/home/ubuntu/efs/airsim_experiments/train_cct_and_airsim/exported_models/predictions/'
#exp_name = 'eccv_train'
exp_name = 'trans_test'
detection_file = det_folder + exp_name + '.p'

#db_file = '/ai4efs/databases/caltechcameratraps/eccv_train_and_imerit_2.json'
db_file = '/home/ubuntu/efs/databases/CaltechCameraTrapsFullAnnotations.json'


if __name__ == '__main__':
    detection_results = pickle.load(open(detection_file,'r'))
    prec, recall, ap = compute_precision_recall(detection_file, detection_results=detection_results)
    im_prec, im_recall, im_ap, im_scores = compute_precision_recall_with_images(detection_file, detection_results=detection_results)
    seq_prec, seq_recall, seq_ap = compute_precision_recall_with_sequences(detection_file, db_file, detection_results=detection_results)
    print('mAP: ', ap,', mAP with images: ',im_ap,', mAP with sequences: ', seq_ap)
    recall_thresh = 0.95
    recall_idx = np.argmin([np.abs(x-recall_thresh) for x in recall])
    print('Prec. at ',recall[recall_idx],' recall: ', prec[recall_idx])
    recall_idx = np.argmin([np.abs(x-recall_thresh) for x in im_recall])
    print('Prec. at ',im_recall[recall_idx],' recall with images: ', im_prec[recall_idx])
    recall_idx = np.argmin([np.abs(x-recall_thresh) for x in seq_recall])
    print('Prec. at ',seq_recall[recall_idx],' recall with sequences: ', seq_prec[recall_idx])
    plt.figure("Precision Recall Curve")
    plt.plot(recall, prec, 'g-', label='per object')
    plt.plot(im_recall, im_prec, 'b--', label = 'per image')
    plt.plot(seq_recall, seq_prec, 'r:', label='per sequence')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel("Precision")
    plt.xlabel("Recall")
    plt.legend()
    plt.title("%0.2f mAP per object, %0.2f mAP per image, %0.2f mAP per sequence" % (ap, im_ap, seq_ap))
    plt.savefig(det_folder + exp_name +'_PR_obj_im_seq.jpg')

    np.savez(det_folder + exp_name + '_obj_im_seq_prec_recall_data.npz', prec=prec, recall=recall, ap=ap, im_prec=im_prec, im_recall=im_recall, im_ap=im_ap, seq_prec=seq_prec, seq_recall=seq_recall, seq_ap=seq_ap)

