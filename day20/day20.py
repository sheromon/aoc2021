import matplotlib.pyplot as plt
import numpy as np


def load_input(input_path):
    enhancement = []
    image = []
    enhancement_done = False
    with open(input_path) as file_obj:
        for line in file_obj:
            if not enhancement_done:
                enhancement += line.strip()
            else:
                image.append(list(line.strip()))
            if not line.strip():
                enhancement_done = True

    image_char_array = np.array(image)
    image = np.zeros_like(image_char_array, dtype=np.uint8)
    image[image_char_array == '#'] = 1

    enhancement_char_array = np.array(enhancement)
    enhancement = np.zeros_like(enhancement_char_array, dtype=np.uint8)
    enhancement[enhancement_char_array == '#'] = 1
    return enhancement, image


def day20a(input_path):
    enhancement, image = load_input(input_path)
    for ind in range(2):
        image = enhance_image(image, enhancement, pad_value=ind % 2)
        image = crop_image(image)
    return np.sum(image)


def enhance_image(image, enhancement, pad_size=5, pad_value=0):
    image = np.pad(image, ((pad_size, pad_size), (pad_size, pad_size)),
        constant_values=(pad_value, pad_value))
    new_image = np.zeros_like(image, dtype=np.uint8)
    for irow in range(image.shape[0] - 2):
        for icol in range(image.shape[1] - 2):
            block = image[irow:irow+3, icol:icol+3]
            enh_ind = sum(bit * 2**ind for ind, bit in enumerate(block.flatten()[::-1]))
            value = enhancement[enh_ind]
            new_image[irow+1, icol+1] = value
    return new_image


def crop_image(image):
    width = 10

    start_col = image.shape[0] // 2 - width // 2
    end_col = image.shape[0] // 2 + width // 2
    middle_cols = image[:, start_col:end_col]
    col_sums = np.sum(middle_cols, axis=1)
    col_sums[0] = col_sums[1]
    if col_sums[1]:
        col_ind = max(np.argmin(col_sums == col_sums[1]) - 2, 0)
    else:
        col_ind = max(np.argmin(col_sums == 0) - 2, 0)

    start_row = image.shape[0] // 2 - width // 2
    end_row = image.shape[0] // 2 + width // 2
    middle_rows = image[start_row:end_row, :]
    row_sums = np.sum(middle_rows, axis=0)
    row_sums[0] = row_sums[1]
    if row_sums[1]:
        row_ind = max(np.argmin(row_sums == row_sums[1]) - 2, 0)
    else:
        row_ind = max(np.argmin(row_sums == 0) - 2, 0)

    ind = min(col_ind, row_ind)
    if ind:
        image = image[ind:-ind, ind:-ind]
    return image


def test20a():
    assert 35 == day20a('test_input.txt')


def day20b(input_path):
    enhancement, image = load_input(input_path)
    for ind in range(50):
        image = enhance_image(image, enhancement, pad_value=ind % 2)
        image = crop_image(image)

    plt.imshow(image, cmap='gray')
    plt.savefig('image.png')
    plt.close()

    return np.sum(image)


def test20b():
    assert 3351 == day20b('test_input.txt')


if __name__ == '__main__':
    # test20a()
    print('Day 20a:', day20a('day20_input.txt'))
    # test20b()
    print('Day 20b:', day20b('day20_input.txt'))
