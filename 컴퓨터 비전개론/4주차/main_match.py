import hw_utils as utils
import matplotlib.pyplot as plt


def main():
    # Test run matching with no ransac
    # plt.figure(figsize=(20, 20))
    # im = utils.Match('./data/scene', './data/box', ratio_thres=0.6)
    # im.save("./scene-box.jpg")
    # plt.title('Match')
    # plt.imshow(im)

    # # Test run matching with ransac //// part 1-2
    plt.figure(figsize=(20, 20))
    im = utils.MatchRANSAC(
        './data/library', './data/library2',
        ratio_thres=0.6, orient_agreement=30, scale_agreement=0.5)
    im.save("./library-library2.jpg")
    plt.title('MatchRANSAC')
    plt.imshow(im)

if __name__ == '__main__':
    main()
