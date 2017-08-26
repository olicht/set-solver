import cv2
import tests
import util

import numpy as np
import set_solver as ss

# open video feed, and solve for every frame

WINDOW_NAME = 'video'
PREV_FRAME_STACK_SIZE = 4
MOVEMENT_THRESHOLD = 4


def main():
	cv2.startWindowThread()
	cv2.namedWindow(WINDOW_NAME, flags=cv2.WINDOW_NORMAL)
	vc = cv2.VideoCapture(0)
	ch = 10

	if vc.isOpened():
		rval, frame = vc.read()
	else:
		rval = False

	prev_frames = []

	while rval:
		# if image has stabilized, solve
		if has_stabilized(prev_frames):
			try:
				_, rect_frame = tests.play_game(frame, pop_open=False)
			except Exception:
				rect_frame = frame

			cv2.imshow(WINDOW_NAME, rect_frame)
			ch = cv2.waitKey(1)
		if ch == 27:
			break
		# get new frame and add to stack of frames
		rval, frame = vc.read()

		if len(prev_frames) > PREV_FRAME_STACK_SIZE:
			prev_frames.pop(0)
		prev_frames.append(frame)


def has_stabilized(frames):
	if len(frames) < 1:
		return

	preprocessed = map(lambda x: util.preprocess(x), frames)
	sum_diff = 0

	# find sum of diff for each pair of consequent frames
	for i in range(len(preprocessed)):
		if i + 1 > len(preprocessed) - 1:
			break
		diff = cv2.absdiff(preprocessed[i], preprocessed[i + 1])
		sum_diff += np.sum(diff)

	# normalize diff by number of pixels and frames
	movement = sum_diff / len(preprocessed) / preprocessed[0].size
	return movement < MOVEMENT_THRESHOLD


def print_properties(props):
	if len(props) > 0:
		ss.pretty_print_properties(props)
		print('----')
