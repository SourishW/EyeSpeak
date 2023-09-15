def calibrate_point(input_point, smaller_vector, larger_vector):
    smaller_x_min = min(point[0] for point in smaller_vector)
    smaller_x_max = max(point[0] for point in smaller_vector)
    smaller_y_min = min(point[1] for point in smaller_vector)
    smaller_y_max = max(point[1] for point in smaller_vector)
    
    larger_x_min = min(point[0] for point in larger_vector)
    larger_x_max = max(point[0] for point in larger_vector)
    larger_y_min = min(point[1] for point in larger_vector)
    larger_y_max = max(point[1] for point in larger_vector)
    
    x_scale = (larger_x_max - larger_x_min) / (smaller_x_max - smaller_x_min)
    y_scale = (larger_y_max - larger_y_min) / (smaller_y_max - smaller_y_min)
    
    calibrated_x = larger_x_min + (input_point[0] - smaller_x_min) * x_scale
    calibrated_y = larger_y_min + (input_point[1] - smaller_y_min) * y_scale
    
    return (calibrated_x, calibrated_y)


if __name__ == "__main__":
    # Define the smaller value vector and the corresponding larger value vector
    # smaller_vector = [(0, 0), (48, 0), (96, 0), (144, 0), (192, 0), (0, 27), (48, 27), (96, 27), (144, 27), (192, 27),
    #                 (0, 54), (48, 54), (96, 54), (144, 54), (192, 54), (0, 81), (48, 81), (96, 81), (144, 81), (192, 81),
    #                 (0, 108), (48, 108), (96, 108), (144, 108), (192, 108)]

    # larger_vector = [(0, 0), (480, 0), (960, 0), (1440, 0), (1920, 0), (0, 270), (480, 270), (960, 270), (1440, 270),
    #                 (1920, 270), (0, 540), (480, 540), (960, 540), (1440, 540), (1920, 540), (0, 810), (480, 810),
    #                 (960, 810), (1440, 810), (1920, 810), (0, 1080), (480, 1080), (960, 1080), (1440, 1080), (1920, 1080)]

    smaller_vector = [(0, 0), (192, 0), (0, 108), (192, 108)]
    larger_vector = [(0, 0), (1920, 0), (0, 1080), (1920, 1080)]

    # Test calibration for an input point
    input_point = (190, 106)
    calibrated_point = calibrate_point(input_point, smaller_vector, larger_vector)
    print("Calibrated Point:", calibrated_point)
