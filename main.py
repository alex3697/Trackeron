import argparse
from Modules.Trackeron import trackeron



parser = argparse.ArgumentParser(description='')

parser.add_argument('--input_txt', '-i', required=False, help='Input metadata path, format first line path of the video, second line format, third line time in the format, fourth line bbox, last line step')

parser.add_argument('--format', '-f', default='utc', help='Input format, ms for miliseconds, s for seconds, utc for hour:minute:second')

parser.add_argument('--analyzed', '-a', default='C:/Users/Alex/Desktop/Ugiat/object-tracker/Trackeron/Canal24h_-_28_julio_2019_-_05-40-01__-_00022.mp4', help='Media to analyze')

parser.add_argument('--input_keyboard', '-k', default='0:23:33.025', help='Input from keyboard: time')

parser.add_argument('--bounding_box', '-b', default='108, 39, 309, 441', help='bounding box info')

parser.add_argument('--step', '-s', default=15, help='step size')




args = parser.parse_args()

#args.input_txt = 'C:/Users/Alex/Desktop/Ugiat/object-tracker/prueba.txt'


if args.input_txt:

	print(f'Reading input file...')
	
	f = args.input_txt
	with open(f) as f:
		for (i, line) in enumerate(f):
			if i == 0:
				args.analyzed = line[:-1]
				continue
			if i == 1:
				args.format = line[:-1]
				continue
			if i == 2:
				args.input_keyboard = line[:-1]
				continue
			if i == 3:
				args.bounding_box = line[:-1]
				continue
			if i == 4:
				args.step = line
				break
	
	

bbox = args.bounding_box.split(', ')

for idx, x in enumerate (bbox):

	bbox[idx] = int(x)

bbox = tuple(bbox)

step = args.step

video = args.analyzed



print(f'Running Trackeron...')

detections = []

scale = 1

detections = trackeron(scale, step)

input_format = args.format

keyboardinput = args.input_keyboard

detections.call_trackeron(bbox, video, input_format, keyboardinput, 'output')