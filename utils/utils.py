import matplotlib.pyplot as plt


def plot_img_and_mask(img, mask):
    # classes = mask.max() + 1
    # fig, ax = plt.subplots(1, classes + 1)
    # ax[0].set_title('Input image')
    # ax[0].imshow(img)
    # ax[0].imshow(mask, alpha=0.5)
    # for i in range(classes):
    #     ax[i + 1].set_title(f'Mask (class {i + 1})')
    #     ax[i + 1].imshow(mask == i)
    
    plt.imshow(img)
    plt.imshow(mask, alpha=0.5)

    plt.xticks([]), plt.yticks([])
    plt.show()
