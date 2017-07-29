import util, os
import set_solver as s
from set_solver import NoCardException
import set_constants as sc
import cv2
from set_test import game
from collections import Counter
import numpy as np
import base64, StringIO
import random


def test():
    # 3 cards on flat table
    cards_3 = cv2.imread('images/set-3-texture.jpg')

    # 5 cards at an angle
    cards_5 = cv2.imread('images/set-5-random.jpg')

    thresh_3 = s.get_binary(cards_3)
    contours = s.find_contours(thresh_3, 3)

    assert len(s.transform_cards(cards_3, contours, 3)) == 3

    res5 = s.detect_cards(cards_5)
    assert res5 is not None and len(res5) == 5

    res3 = s.detect_cards(cards_3)
    assert res3 is not None and len(res3) == 3

    for i in range(len(res5)):
        c = res5[i]
        # util.show(c, 'card')
        cv2.imwrite('images/cards/card-5-%d.jpg' % i, c)

    for i in range(len(res3)):
        c = res3[i]
        # util.show(c, 'card')
        cv2.imwrite('images/cards/card-3-%d.jpg' % i, c)

    # for cards detected, get properties
    for link in os.listdir('images/cards'):
        img = cv2.imread('images/cards/%s' % link)
        test_props(img)
    print 'tests pass'


def test_props(img):
    color = sc.PROP_COLOR_MAP[s.get_card_color(img)]
    shape = sc.PROP_SHAPE_MAP[s.get_card_shape(img, s.get_training_set())]
    num = s.get_card_number(img)
    texture = sc.PROP_TEXTURE_MAP[s.get_card_texture(img)]

    print '%d %s %s %s' % (num, color, shape, texture)
    print('---')

    util.show(img)


def main():
    # # 3 of the 12 set that's bad
    # cards_3_bad = cv2.imread('images/set-3-bad.jpg')
    # thresh_3bad = s.get_binary(cards_3_bad)
    # res3bad = s.detect_cards(cards_3_bad)
    # assert res3bad is not None and len(res3bad) == 3

    # # 12 cards
    # cards_12 = cv2.imread('images/set-12-random-2sets.jpg')

    # thresh_12bad = s.get_binary(cards_12)
    # res12bad = s.detect_cards(cards_12, draw_rects=True)
    # util.show(cards_12)

    # # Subset of 3, with the 1 problem card
    # cards = res12bad
    # for i in range(len(cards)):
    #     card = cards[i]
    #     # test_props(card)
    #     cv2.imwrite('images/cards/card-12-%02d.jpg' % i, card)
    play_game(cv2.imread("images/set-12-random-2sets.jpg"))

    # props = s.get_cards_properties(res12bad)
    # s.pretty_print_properties(props)

    # g = game(cards=props)
    # sets = g.play(True)

    # if sets:
    #     print '\nFound sets:'
    #     for st in sets:
    #         just_props = [e for i, e in st]
    #         print just_props
    #         s.pretty_print_properties(just_props)
    #         print('---')
    # else:
    #     print 'no sets :('

    print 'tests pass'


def play_game(frame, printall=False, \
              draw_contours=True, resize_contours=True, \
              draw_rects=False, sets_or_no=False, \
              pop_open=True):
    """Takes in an image path (to local file), finds all sets, and pretty prints them to screen.
    if printall - prints the identities of all cards in the image
    if draw_contours - outlines the cards belonging to each set
    if resize_contours - enlarges contours for cards belonging to multiple sets to avoid overlay
    if draw_rects - draws box rects around cards belonging to each set
    if sets_or_no - outlines the image in green or red, depending on whether there are any sets present"""
    
    img = s.resize_image(frame, 1200)
    # util.show(img)

    try:
        contours, drawn, detected = s.detect_cards(img, draw_rects=True, return_contours=True)
        props = s.get_cards_properties(detected)
    except NoCardException as e:
        raise e

    if printall:
        s.pretty_print_properties(props)

    g = game(cards=props)
    sets = g.play(idx=True)

    # # RED, ORANGE, YELLOW, GREEN, BLUE, //INDIGO,// VIOLET
    # BGR_RAINBOW = [ (0, 0, 255), (0, 127, 255), (0, 255, 255), \
    #                (0, 255, 0), (255, 0, 0), (130, 0, 75),
    #                (255, 0, 139) ]

    if sets:
        # choose a group of colors at random to represent the set of sets
        # COLORS = random.sample(BGR_RAINBOW, len(sets))
        COLORS = util.random_color_palette(len(sets))

        if resize_contours:
            # count number of sets that each winning card index belongs to
            counter = Counter( card[0] for st in sets for card in st )

        for i, st in enumerate(sets):
            print ('---')
            color = COLORS[i]
            st_indices, st_props = zip(*st)
            s.pretty_print_properties(st_props)

            if draw_contours or draw_rects:
                winning_contours = [ contours[c] for c in st_indices ]
                if draw_contours:
                    if resize_contours:
                        for idx in st_indices:
                            # set base thickness
                            thickness = 7
                            count = counter[idx]
                            if count > 1:
                                thickness += 14*counter[idx]
                            counter[idx] -= 1
                            cv2.drawContours(img, contours, idx, color, thickness)

                    else:
                        cv2.drawContours(img, winning_contours, -1, color, 3)

                if draw_rects:
                    # get bounding rectangles
                    winning_rects = [ cv2.minAreaRect(c) for c in winning_contours ]
                    for rect in winning_rects:
                        # convert to ints
                        r = [ (int(x), int(y)) for x,y in cv.BoxPoints(rect) ]
                        cv2.rectangle(img, r[0], r[2], color)

    else:
        print 'no sets :('

    if sets_or_no:
        height, width, _ = img.shape
        BORDER_SCALAR = 0.01
        border_h, border_w = ( int(dim*BORDER_SCALAR) for dim in (height, width))

        # indices 0 or 1 correspond to bool for if no sets (BGR for red) or sets (green)
        BORDER_COLORS = [ (19,19,214), (94,214,19) ]

        img_outlined = cv2.copyMakeBorder(img, border_h, border_h, \
                                          border_w, border_w, \
                                          cv2.BORDER_CONSTANT,
                                          value = BORDER_COLORS[bool(sets)])

    processed_img = (img_outlined if sets_or_no else img)

    final_img = s.resize_image(processed_img, 1200)

    if pop_open: util.show(final_img)

    num_sets = ( len(sets) if sets else 0 )

    # # convert image array to string representing JPEG of image (in RGB)
    # image = Image.fromarray( cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB) )
    # output = StringIO.StringIO()
    # image.save(output, format='JPEG')
    # mystr = output.getvalue()
    # output.close()
    #cv2.imwrite('tmp.jpeg', final_img)
    #l = len(final)
    #print 'length is {}'.format(l)
    #print 'size is {} bytes'.format((l-814)/1.37)
    # N.B.
    # length is 123932
    # size is 89867.1532847 bytes

    return (num_sets, final_img)


