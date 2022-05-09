def modify_input_for_multiple_img(product_id, img):
    img_dict = {}
    img_dict['product'] = product_id
    img_dict['image'] = img
    return img_dict
