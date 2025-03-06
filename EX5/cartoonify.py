##############################################################################
# FILE: cartoonify.py
# EXERCISE: Intro2cs ex5 2021-2022
# WRITER: Yotam Gaosh, [REDACTED] Gaash
# DESCRIPTION:A helper file for ex5 that masks handling with images
# STUDENTS I DISCUSSED THE EXERCISE WITH: none
# WEB PAGES I USED: None
# NOTES: ...
##############################################################################

""" imports """
import sys

from ex5_helper import *
from copy import deepcopy
from math import floor, ceil
from typing import List, Union

""" Constants """

RED_TO_BW = 0.299
GREEN_TO_BW = 0.587
BLUE_TO_BW = 0.114

MAX_PIXEL_VAL = 255
MIN_PIXEL_VAL = 0

USER_ARGS_NUM = 8
ARG_NUM_ERROR_MESSAGE = "Incorrect number of arguments has been entered. Exiting the program."

LEFT = 'L'
RIGHT = 'R'

MULTI_CHANNEL_IMAGE_TYPE = List[List[List[int]]]
GRAYSCALE_IMAGE_TYPE = List[List[int]]
UNSPECIFIED_IMAGE_TYPE = Union[GRAYSCALE_IMAGE_TYPE, MULTI_CHANNEL_IMAGE_TYPE]
KERNEL_MATRIX_TYPE = List[List[float]]

""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ helper functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def convert_to_nice_number(ugly_number: float) -> int:
    """
    This function converts float numbers to integers and makes sure they are within the legal range
    of 0 to 255
    :param ugly_number: a float number
    :return: a legal int number
    """

    nice_number = round(ugly_number)
    if nice_number > MAX_PIXEL_VAL:
        return MAX_PIXEL_VAL
    if nice_number < MIN_PIXEL_VAL:
        return MIN_PIXEL_VAL

    return nice_number


def grayscale_average(RGB_list: List[int]) -> int:
    """
    this function converts a list of Red, Green and blue channel values to the corresponding Greyscale value.
    :param RGB_list: list of Red, Green, Blue values
    :return: Greyscale number
    """
    return convert_to_nice_number((RGB_list[0] * RED_TO_BW) + (RGB_list[1] * GREEN_TO_BW) + (RGB_list[2] * BLUE_TO_BW))


def kernel_sum(image: GRAYSCALE_IMAGE_TYPE, kernel: KERNEL_MATRIX_TYPE, row_cord: int, col_cord: int) -> int:
    """
    this function sums up the value for all the pixels in a kernel matrix range
    :param image: greyscale image
    :param kernel: the kernel matrix
    :param row_cord: current row of the pixel
    :param col_cord: current column of the pixel
    :return: kernel_sum: the sum of all the values of the nearby pixels affected by the kernel
    """

    # the distance from the coordinate location to the edge of the kernel matrix
    kernel_radius = len(kernel) // 2
    max_row = len(image)
    max_column = len(image[0])
    kernels_sum = 0
    for row in range(row_cord - kernel_radius, row_cord + kernel_radius + 1):
        for column in range(col_cord - kernel_radius, col_cord + kernel_radius + 1):
            # if the coordinates are out of bounds the original pixel value is added instead to the sum
            if (0 <= row < max_row) and (0 <= column < max_column):
                kernels_sum += (image[row][column]) * \
                               kernel[row - (row_cord - kernel_radius)][column - (col_cord + kernel_radius + 1)]
            else:
                kernels_sum += (image[row_cord][col_cord]) * \
                               kernel[row - (row_cord - kernel_radius)][column - (col_cord + kernel_radius + 1)]
    return kernels_sum


def block_average(image: GRAYSCALE_IMAGE_TYPE, block_size: int, row_cord: int, col_cord: int) -> float:
    """
    this function return the value of the neighbors to a pixel in a given block area
    :param image: the image in which we search
    :param block_size: the size of the search block
    :param row_cord: row of the pixel
    :param col_cord: column of the pixel
    :return: average of the values of the pixel's neighbors
    """
    block_matrix = [[1 for _ in range(block_size)] for _ in range(block_size)]
    block_sum = kernel_sum(image, block_matrix, row_cord, col_cord)
    return block_sum / (block_size * block_size)


def list_merger(pixel1: list, pixel2: list, mask: int) -> List[int]:
    """
    this function gets two lists (or ints) and a mask value and combines them to a single list
    :param pixel1: pixel from image 1
    :param pixel2: pixel image 2
    :param mask: a mask value (either 0 or 1)
    :return: list (or int) of the combined values
    """

    merged_list = []
    for channel in range(len(pixel1)):
        merged_list.append(convert_to_nice_number(((pixel1[channel]) * mask) + ((pixel2[channel]) * (1 - mask))))
    return merged_list


def normalize_image(image: GRAYSCALE_IMAGE_TYPE) -> KERNEL_MATRIX_TYPE:
    """
    this function normalize a black and white image to values between zero and one.
    :param image: a greyscale image
    :return: image with normalized values between zero and one
    """
    normal_image = deepcopy(image)
    for row in range(len(normal_image)):
        for column in range(len(normal_image[0])):
            normal_image[row][column] = (normal_image[row][column]) / MAX_PIXEL_VAL
    return normal_image


def resize_by_factor(image: UNSPECIFIED_IMAGE_TYPE, max_size: int) -> UNSPECIFIED_IMAGE_TYPE:
    """
    this function resize an image by a factor while keeping the original proportions
    :param image: an unspecified image
    :param max_size: the factor by which the image is resized
    :return: a resized image
    """

    resized_image =[]
    image_height = len(image)
    image_width = len(image[0])
    new_height = max_size
    new_width = round(image_width * (image_height / max_size))

    if image_width > image_height:
        # if the width of the image is larger than its height we calculate the new height
        # with accordance to the ratio between the original width and the max size value
        new_width = max_size
        new_height = round(image_height * (image_width / max_size))

    if (type(image[0][0]) is int) or (type(image[0][0]) == int):
        return resize(image, new_height, new_width)
    else:
        sep_channels_list = separate_channels(image)
        for channel_image in sep_channels_list:
            channel_image = resize(channel_image, new_height, new_width)
        return combine_channels(sep_channels_list)

    return


""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


def separate_channels(image: MULTI_CHANNEL_IMAGE_TYPE) -> List[GRAYSCALE_IMAGE_TYPE]:
    """
    A function that receives a multi-channel image and convert it to separate a list of greyscale images for each
    channel in the image
    :param image: A matrix (2D list array) of "pixels" - a.k.a list of different channels
    :return: A list of different matrices for each separate channel in the channels
    """

    image_height = len(image)
    image_width = len(image[0])
    num_of_channels = len(image[0][0])

    separated_image = []
    for channel in range(num_of_channels):
        separated_image.append([])
        for row in range(image_height):
            separated_image[channel].append([])
            for col in range(image_width):
                separated_image[channel][row].append(image[row][col][channel])

    return separated_image


def combine_channels(channels: List[GRAYSCALE_IMAGE_TYPE]) -> MULTI_CHANNEL_IMAGE_TYPE:
    """
    This function combine an image from a list of greyscale images into one single image with multi channels
    :param channels: a list of single channel images
    :return: an image made out of a list of lists of channels
    """
    image_height = len(channels[0])
    image_width = len(channels[0][0])
    num_of_channels = len(channels)

    combined_image = []
    for row in range(image_height):
        combined_image.append([])
        for col in range(image_width):
            combined_image[row].append([])
            for channel in range(num_of_channels):
                combined_image[row][col].append(channels[channel][row][col])

    return combined_image


def RGB2grayscale(colored_image: MULTI_CHANNEL_IMAGE_TYPE) -> GRAYSCALE_IMAGE_TYPE:
    """
    This function receives an RGB image and converts it a single channel grayscale image
    :param colored_image: an RGB image
    :return: a greyscale_image
    """

    grayscale_image = []
    for row in range(len(colored_image)):
        grayscale_image.append([])
        for column in range(len(colored_image[0])):
            grayscale_image[row].append(grayscale_average(colored_image[row][column]))

    # greyscale_image = [grayscale_average(colored_image[row][col])
    #                    for row in range(len(colored_image)) for col in range(len(colored_image[0]))]

    return grayscale_image


def blur_kernel(size: int) -> KERNEL_MATRIX_TYPE:
    """
    This function return a  blur kernel matrix of size x size with the value of size**(-2)
    :param size: the kernel size
    :return: the kernel matrix
    """
    return [[size ** (-2) for _ in range(size)] for _ in range(size)]


def apply_kernel(image: GRAYSCALE_IMAGE_TYPE, kernel: KERNEL_MATRIX_TYPE) -> GRAYSCALE_IMAGE_TYPE:
    """
    this function applies a kernel matrix on an image in order to "blur" it
    :param image: a greyscale image
    :param kernel: a kernel matrix
    :return: new_image: A new image on which the kernel was applied.
    """
    new_image = deepcopy(image)

    for row in range(len(image)):
        for column in range(len(image[0])):
            new_image[row][column] = convert_to_nice_number(kernel_sum(image, kernel, row, column))
    return new_image


def bilinear_interpolation(image: GRAYSCALE_IMAGE_TYPE, y: float, x: float) -> int:
    """
    this function calculates a value for a pixel based on the x,y coordinates based on the values of it's neighboring
    pixels in the original image, using a bilinear interpolation
    in the original image
    :param image: a greyscale image
    :param y: the parameter for the row of the pixel
    :param x: the parameter for the column of the pixel
    :return: the value of the new pixel calculated by the bilinear interpolation equation
    """

    min_y, max_y = floor(y), ceil(y)  # the min and max values are the closest whole values in the source image
    if max_y > len(image) - 1:
        max_y = min_y
    min_x, max_x = floor(x), ceil(x)
    if max_x > len(image[0]) - 1:
        max_x = min_x

    reminder_y, reminder_x = y - min_y, x - min_x

    a = int(image[min_y][min_x])
    b = int(image[max_y][min_x])
    c = int(image[min_y][max_x])
    d = int(image[max_y][max_x])

    return convert_to_nice_number((a * ((1 - reminder_x) * (1 - reminder_y))) +
                                  (b * (reminder_y * (1 - reminder_x)) +
                                  (c * (reminder_x * (1 - reminder_y))) +
                                  (d * (reminder_x * reminder_y))))


def resize(image: UNSPECIFIED_IMAGE_TYPE, new_height: int, new_width: int) -> UNSPECIFIED_IMAGE_TYPE:
    """
    this function resizes an image to a new given size by height and length, using bilinear interpolation.
    :param image: either a greyscale or multi-channel image
    :param new_height: new given height for the resized image
    :param new_width: new given width for the resized image
    :return: a new resized image
    """
    original_height = len(image)
    original_width = len(image[0])

    height_factor = (original_height - 1) / (new_height - 1)
    width_factor = (original_width - 1) / (new_width - 1)

    resized_image = []

    for row in range(new_height):
        resized_image.append([])
        for column in range(new_width):
            resized_image[row].append(bilinear_interpolation(image, row * height_factor, column * width_factor))

    return resized_image


def rotate_90(image: UNSPECIFIED_IMAGE_TYPE, direction: str) -> UNSPECIFIED_IMAGE_TYPE:
    """
    this function rotates an image by 90 degrees to a given direction
    :param image: greyscale or multi-channel image
    :param direction: direction of rotation, either 'L' for left or 'R' for right
    :return: the rotated image
    """
    rotated_image = []
    for row in range(len(image[0])):
        rotated_image.append([])
        for column in range(len(image)):
            if direction == RIGHT:
                rotated_image[row].append(image[len(image) - 1 - column][row])
            elif direction == LEFT:
                rotated_image[row].append((image[column][len(image[0]) - 1 - row]))
    return rotated_image


def get_edges(image: GRAYSCALE_IMAGE_TYPE, blur_size: int, block_size: int, c: int) -> GRAYSCALE_IMAGE_TYPE:
    """
    this function converts an image to a BW representation of it's edges. first the function blurs the image
    to remove noise and then it assign a black or white value to a pixel according to a threshold.
    :param image: original greyscale image
    :param blur_size: size of the blur kernel we wish to apply
    :param block_size: the size of the block for the edge detection
    :param c: a given constant to be added to the threshold
    :return: BW image representing the edges in the original image.
    """

    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    edgy_image = deepcopy(blurred_image)

    for row in range(len(blurred_image)):
        for col in range(len(blurred_image[0])):
            threshold = block_average(blurred_image, block_size, row, col)
            # the pixel is painted black if it's value is below the threshold
            if blurred_image[row][col] < threshold - c:
                edgy_image[row][col] = MIN_PIXEL_VAL
            else:
                edgy_image[row][col] = MAX_PIXEL_VAL

    return edgy_image


def quantize(image: GRAYSCALE_IMAGE_TYPE, N: int) -> GRAYSCALE_IMAGE_TYPE:
    """
    this function reduces the number of shades in a greyscale image by dividing them into N separate
    shades out of 255
    :param image: a greyscale image
    :param N: desired number of shades
    :return: a greyscale image with #N shades
    """
    quantized_image = deepcopy(image)
    for row in range(len(image)):
        for col in range(len(image[0])):
            quantized_image[row][col] = \
                convert_to_nice_number(int(image[row][col] * (N / MAX_PIXEL_VAL)) * (MAX_PIXEL_VAL / N))
    return quantized_image


def quantize_colored_image(image: MULTI_CHANNEL_IMAGE_TYPE, N: int) -> MULTI_CHANNEL_IMAGE_TYPE:
    """
    this function quantize a multi-channel image to an image with N shades in each channel.
    :param image: a multi-channel image
    :param N: number of desired shades
    :return: a quantized multi-channel image
    """

    separated_channel_list = separate_channels(image)
    quantized_list = [quantize(single_channel_image, N) for single_channel_image in separated_channel_list]
    return combine_channels(quantized_list)


def add_mask(image1: UNSPECIFIED_IMAGE_TYPE, image2: UNSPECIFIED_IMAGE_TYPE, mask: KERNEL_MATRIX_TYPE) \
        -> UNSPECIFIED_IMAGE_TYPE:
    """
    this function combines two images using a mask layer
    :param image1: first image (either multi-channel or greyscale)
    :param image2: second image (either multi-channel or greyscale)
    :param mask: a mask image containing [0,1] values that is used for merging the images
    :return: a combination of the two images with the mask applied on them
    """

    def apply_mask(pixel1: int, pixel2: int, mask_pixel: float) -> int:
        """ this function is applying a mask value on two pixels"""
        return convert_to_nice_number((pixel1 * mask_pixel) + (pixel2 * (1 - mask_pixel)))

    def apply_colorful_mask(image1: MULTI_CHANNEL_IMAGE_TYPE, image2: MULTI_CHANNEL_IMAGE_TYPE,
                            mask: KERNEL_MATRIX_TYPE) -> MULTI_CHANNEL_IMAGE_TYPE:
        """ this function apply a mask on two multi-channel images"""
        new_image = deepcopy(image1)
        for row in range(len(image1)):
            for column in range(len(image1[0])):
                for channel in range(len(image1[0][0])):
                    new_image[row][column][channel] = apply_mask(image1[row][column][channel],
                                                                 image2[row][column][channel], mask[row][column])
        return new_image

    def apply_gray_mask(image1: GRAYSCALE_IMAGE_TYPE, image2: GRAYSCALE_IMAGE_TYPE,
                        mask: KERNEL_MATRIX_TYPE) -> GRAYSCALE_IMAGE_TYPE:
        """this function apply a mask on two grayscale images """
        new_image = deepcopy(image1)
        for row in range(len(image1)):
            for column in range(len(image1[0])):
                new_image[row][column] = apply_mask(image1[row][column], image2[row][column], mask[row][column])
        return new_image

    if type(image1[0][0]) is list:
        return apply_colorful_mask(image1, image2, mask)

    elif type(image1[0][0]) is int or type(image1[0][0] is float):
        return apply_gray_mask(image1, image2, mask)


def cartoonify(image: UNSPECIFIED_IMAGE_TYPE,
               blur_size: int, th_block_size: int, th_c: int, quant_num_shades: int) -> UNSPECIFIED_IMAGE_TYPE:
    """
    :param image: an RGB image
    :param blur_size: size of the blur kernel
    :param th_block_size: size of the kernel used to check the edge threshold
    :param th_c: the threshold constant for the get_edges function
    :param quant_num_shades: number of shade to be used in the quantize function
    :return:
    """
    quantized_image = quantize_colored_image(image, quant_num_shades)
    edge_image = get_edges(RGB2grayscale(image), blur_size, th_block_size, th_c)
    separated_channels_list = separate_channels(quantized_image)
    cartoon_channel_list = []
    for channel_image in separated_channels_list:
        cartoon_channel_list.append(add_mask(channel_image, edge_image, normalize_image(edge_image)))
    return combine_channels(cartoon_channel_list)


if __name__ == '__main__':

    if len(sys.argv) != USER_ARGS_NUM:
        # if the number of variables from the user is not equal to the required number, an error message
        # is printed and than the program exit.
        print(ARG_NUM_ERROR_MESSAGE)
        sys.exit()

    # arguments from the user:
    image_source = sys.argv[1]
    cartoon_dest = sys.argv[2]
    max_im_size = int(sys.argv[3])
    blur_size = int(sys.argv[4])
    th_block_size = int(sys.argv[5])
    th_c = int(sys.argv[6])
    quant_num_shades = int(sys.argv[7])

    # applying the cartoonify function on the image

    original_image = load_image(image_source)
    cartoon_image = cartoonify(resize_by_factor(original_image, max_im_size)
                               , blur_size, th_block_size, th_c, quant_num_shades)
    save_image(cartoon_image, cartoon_dest)

    # thank you for reviewing my code. btw this exercise didn't make me want to kill myself at all (NOT)
