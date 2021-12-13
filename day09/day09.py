import numpy as np


def load_input(input_path):
    """Return 2D array of sea floor heights."""
    height_array = []
    with open(input_path) as file_obj:
        for line in file_obj:
            vals = [int(val) for val in line.strip()]
            height_array.append(vals)
    return np.array(height_array)


def get_low_points_mask(height_array):
    """Return boolean array indicating location of low points.

    Array shape is the same as height array, and a value of True indicates a
    low point.
    """
    n_rows, n_cols = height_array.shape
    lowest = np.zeros_like(height_array, dtype=bool)
    for irow in range(n_rows):
        for icol in range(n_cols):
            val = height_array[irow, icol]
            compare_vals = []
            if irow > 0:
                compare_vals.append(height_array[irow - 1, icol])
            if icol > 0:
                compare_vals.append(height_array[irow, icol - 1])
            if irow < n_rows - 1:
                compare_vals.append(height_array[irow + 1, icol])
            if icol < n_cols - 1:
                compare_vals.append(height_array[irow, icol + 1])
            if np.all(val < np.array(compare_vals)):
                lowest[irow, icol] = True
    return lowest


def day09a(input_path):
    """Return the sum of risk levels for all low points."""
    height_array = load_input(input_path)
    lowest = get_low_points_mask(height_array)
    # risk level for each low point is its height plus 1, so sum of risk levels
    # is the sum of heights plus the number of low points
    risk_level = np.sum(height_array[lowest]) + np.sum(lowest)
    return risk_level


def test09a():
    score = day09a('test_input.txt')
    assert 15 == score


def day09b(input_path):
    """Return the product of the three largest basin sizes."""
    height_array = load_input(input_path)
    lowest = get_low_points_mask(height_array)

    # for each low point, get the size of the corresponding basin
    basin_sizes = []
    lowest_inds = np.where(lowest)
    for irow, icol in zip(*lowest_inds):
        basin = np.zeros_like(height_array, dtype=bool)
        basin[irow, icol] = True
        update_basin(basin, height_array, irow, icol)
        basin_sizes.append(np.sum(basin))

    basin_sizes = np.sort(basin_sizes)
    return np.prod(basin_sizes[-3:])


def update_basin(basin, height_array, irow, icol):
    """For a point in a basin, check to see if neighboring points have height 9,
    and expand the basin if they are lower than 9.
    """
    n_rows, n_cols = height_array.shape
    if irow > 0 and not basin[irow - 1, icol]:
        if height_array[irow - 1, icol] < 9:
            basin[irow - 1, icol] = True
            update_basin(basin, height_array, irow - 1, icol)
    if icol > 0 and not basin[irow, icol - 1]:
        if height_array[irow, icol - 1] < 9:
            basin[irow, icol - 1] = True
            update_basin(basin, height_array, irow, icol - 1)
    if irow < n_rows - 1 and not basin[irow + 1, icol]:
        if height_array[irow + 1, icol] < 9:
            basin[irow + 1, icol] = True
            update_basin(basin, height_array, irow + 1, icol)
    if icol < n_cols - 1 and not basin[irow, icol + 1]:
        if height_array[irow, icol + 1] < 9:
            basin[irow, icol + 1] = True
            update_basin(basin, height_array, irow, icol + 1)


def test09b():
    score = day09b('test_input.txt')
    assert 1134 == score


if __name__ == '__main__':
    test09a()
    print('Day 09a:', day09a('day09_input.txt'))
    test09b()
    print('Day 09b:', day09b('day09_input.txt'))
