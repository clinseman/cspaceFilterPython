import cv2
import numpy as np


"""Private helper functions"""


def __cspaceSwitch(img, cspace):
    """Coverts the colorspace of img from BGR to cspace

    Parameters
    ----------
    img : array_like
        the image to convert
    cspace : int
        the colorspace to convert to; see keys below

    Returns
    -------
    img : ndarray
        img with the converted colorspace

    Colorspace Keys
    ---------------
    0 -- BGR        1 -- HSV        2 -- HLS        3 -- Lab
    4 -- Luv        5 -- YCrCb      6 -- XYZ        7 -- Grayscale

    """
    if cspace is 0:
        return img
    convert_code = {
        1: cv2.COLOR_BGR2HSV,
        2: cv2.COLOR_BGR2HLS,
        3: cv2.COLOR_BGR2Lab,
        4: cv2.COLOR_BGR2Luv,
        5: cv2.COLOR_BGR2YCrCb,
        6: cv2.COLOR_BGR2XYZ,
        7: cv2.COLOR_BGR2GRAY
    }[cspace]
    img = cv2.cvtColor(img, convert_code)

    return img


def __cspaceBounds(cspace, slider_pos):
    """Calculates the lower and upper bounds for thresholding a
    colorspace based on the thresholding slider positions.

    Parameters
    ----------
    cspace : int
        the colorspace to find bounds of; see keys in __cspaceSwitch()
    slider_pos : array_like
        the positions of the thresholding trackbars; length 6 list

    Returns
    -------
    lowerb : array_like
        contains the lower bounds for each channel
    upperb : array_like
        contains the upper bounds for each channel

    """
    min_dict = {3: np.array([0, 1, 1])}
    max_dict = {1: np.array([180, 255, 255]), 2: np.array([180, 255, 255])}

    mins = min_dict.get(cspace, np.array([0, 0, 0]))
    maxs = max_dict.get(cspace, np.array([255, 255, 255]))

    lowerb = np.array([slider_pos[0], slider_pos[2], slider_pos[4]])
    upperb = np.array([slider_pos[1], slider_pos[3], slider_pos[5]])
    lowerb = lowerb * (maxs - mins) / 100 + mins  # put in the correct range
    upperb = upperb * (maxs - mins) / 100 + mins

    if cspace is 7: lowerb, upperb = lowerb[0], upperb[0]

    return lowerb, upperb


def __cspaceRange(img, cspace, lowerb, upperb):
    """Thresholds img in cspace with lowerb and upperb

    Parameters
    ----------
    img : array_like
        the image to be thresholded
    cspace : int
        the colorspace to threshold in; see keys in __cspaceSwitch()

    Returns
    -------
    bin_img : ndarray
        a binary image that has been thresholded

    """
    img = __cspaceSwitch(img, cspace)
    bin_img = cv2.inRange(img, lowerb, upperb)

    return bin_img


"""Main public function"""


def main(img, cspace_label, slider_pos):
    """Computes the colorspace thresholded image based on
    slider positions and selected colorspace.

    Parameters
    ----------
    img : array_like
        input image
    cspace_label : string
        colorspace to threshold in; one of the following:
        BGR, HSV, HLS, Lab, Luv, YCrCb, XYZ, Grayscale
    slider_pos : array_like
        positions of the six sliders

    Returns
    -------
    bin_img : ndarray
        binary processed image
    cspace_label : string
        colorspace of the image
    lowerb : list
        threshold lower bound
    upperb : list
        threshold upper bound

    """

    # create colorspace labels to be displayed
    cspace_dict = {'BGR': 0, 'HSV': 1, 'HLS': 2, 'Lab': 3,
                   'Luv': 4, 'YCrCb': 5, 'XYZ': 6, 'Gray': 7}
    cspace = cspace_dict[cspace_label]

    # create thresholded image
    lowerb, upperb = __cspaceBounds(cspace, slider_pos)
    bin_img = __cspaceRange(img, cspace, lowerb, upperb)

    # output processing
    lowerb = lowerb.tolist()
    upperb = upperb.tolist()

    return bin_img, cspace_label, lowerb, upperb
