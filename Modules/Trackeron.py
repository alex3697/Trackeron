import sys, cv2, datetime, numpy    #la version con mas contrib


class trackeron:


	def __init__(self, scale, step):

		self.scale, self.step = scale, int(step)


	def print_frames(self, video1, timecode, frame_idx):
		video = cv2.VideoCapture(video1)
		frames = []

		for i in range(16):

			video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx-8+i)

			_, img = video.read()

			img = cv2.resize(img, None, fx=0.3, fy=0.3, interpolation = cv2.INTER_LINEAR)

			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			frames.append(img)



		aux_list = []

		for i in range(0, 16, 4):

			vis = numpy.concatenate((frames[i], frames[i+1]), axis=1)

			vis = numpy.concatenate((vis, frames[i+2]), axis=1)

			vis = numpy.concatenate((vis, frames[i+3]), axis=1)

			aux_list.append(vis)



		vis = numpy.concatenate((aux_list[0], aux_list[1]), axis=0)

		vis = numpy.concatenate((vis, aux_list[2]), axis=0)

		vis = numpy.concatenate((vis, aux_list[3]), axis=0)

		cv2.imwrite('C:/Users/Alex/Desktop/Ugiat/object-tracker/boundary_frames/'+str(timecode)+'.png', vis)
		# cv2.imshow("hole",vis)
		# cv2.waitKey(0)



	def printresult(self, tc_detection, input_format, fps):

		detections = tc_detection
		if input_format == 's':
			print(f'First and last apparition detected by the KCF tracker are at: {detections[0]} - {detections[1]} seconds')

		elif input_format == 'ms':
			detections[0] = detections[0] * 1000
			detections[1] = detections[1] * 1000
			print(f'First and last apparition detected by the KCF tracker are at: {detections[0]} - {detections[1]} miliseconds')

		elif input_format == 'utc':
			print(f'First and last apparition detected by the KCF tracker are at: {datetime.timedelta(seconds=detections[0])} - {datetime.timedelta(seconds=detections[1])}')

		elif input_format == 'frame':
			tiempo1 = detections[0]
			horas1 = int(tiempo1/3600)
			minutos1 = int((tiempo1 - horas1*3600)/60)
			segundos1 = int(tiempo1 - horas1*3600 - minutos1*60)
			frame1 = int((tiempo1 - horas1*3600 - minutos1*60 - segundos1)* fps)

			tiempo2 = detections[1]
			horas2 = int(tiempo2/3600)
			minutos2 = int((tiempo2 - horas2*3600)/60)
			segundos2 = int(tiempo2 - horas2*3600 - minutos2*60)
			frame2 = int((tiempo2 - horas2*3600 - minutos2*60 - segundos2)* fps)
			
			print(f'First and last apparition detected by the KCF tracker are at: {horas1}:{minutos1}:{segundos1}.{frame1} - {horas2}:{minutos2}:{segundos2}.{frame2}')




	def call_trackeron(self, bbox, video, input_format, keyboardinput, entrada):
		video1 = cv2.VideoCapture(video)
		fps = video1.get(cv2.CAP_PROP_FPS)

		if input_format == 's':
			input_tcs = float(keyboardinput)

		if input_format == 'ms':
			input_tcs = keyboardinput/1000

		if input_format == 'utc':
			keyboardinput = keyboardinput.split(":")
			input_tcs = int(keyboardinput[0]) * 3600 + int(keyboardinput[1]) * 60 + float(keyboardinput[2])

		if input_format == 'frame':
			keyboardinput = keyboardinput.split(":")
			frame = keyboardinput[2].split(".")
			input_tcs = int(keyboardinput[0]) * 3600 + int(keyboardinput[1]) * 60 + int(frame[0]) + float(int(frame[1])/100 * fps)

		if entrada == 'output':
			video1 = cv2.VideoCapture(video)
			frame_escogido = input_tcs * fps
			increment = self.step
			tc_salida, self.bbox1 = self.track(bbox, video1, frame_escogido, increment)
			video1 = cv2.VideoCapture(video)
			tc_salida = tc_salida - 2*fps
			tc_salida, self.bbox1 = self.track(self.bbox1, video1, tc_salida, 1)
			tc_salida = tc_salida/fps
			frame_escogido = input_tcs * fps
			tc_detection = tc_salida


		if entrada == 'input':
			increment = -self.step
			frame_escogido = input_tcs * fps
			video1 = cv2.VideoCapture(video)
			tc_entrada, self.bbox1 = self.track(bbox, video1, frame_escogido, increment)
			video1 = cv2.VideoCapture(video)
			tc_entrada = tc_entrada + 2*fps
			tc_entrada, self.bbox1 = self.track(self.bbox1, video1, tc_entrada, -1)
			tc_entrada = tc_entrada/fps
			tc_detection = tc_entrada
			
		timecode = "00_24_34"
		framedetectado = round(tc_detection*fps)

		self.print_frames(video, timecode, framedetectado)
		#self.printresult(tc_detection, input_format, fps)
	
	
		#pregunta = input('quieres preguntar por un tiempo determinado? Y/N: ')

		# if pregunta == 'Y':
		# 	tiempo = int(input('pon el tiempo en segundos dentro del limite marcado anteriormente: '))
		# 	frame_escogido = round(input_tcs * fps)
		# 	frame_encuestion = round(tiempo * fps)
		# 	box = self.IsHere(bbox,video, frame_escogido, frame_encuestion,fps)
		# 	print(box)

		# elif pregunta == 'N':
		# 	print('okey then :)')


	def track(self, bbox, video, frame_escogido, increment):
		tracker = cv2.TrackerKCF_create()

		retries = 0
		iteration = 0
		frame_importante = frame_escogido
		while video.isOpened():
			if frame_escogido < 0:
				break
			video.set(cv2.CAP_PROP_POS_FRAMES, frame_escogido)
			ret, frame = video.read()
			if ret is False:
				print('video.read() es false')
				break
			frame = cv2.resize(frame, None, fx=self.scale, fy=self.scale, interpolation = cv2.INTER_LINEAR)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
			if iteration == 0:
				tracker.init(frame, bbox)
			elif iteration >= 1:
				(success, box) = tracker.update(frame)
				if success:
					
					(x, y, w, h) = [int(v*self.scale) for v in box]
					cv2.rectangle(frame,(x, y), (w + x, y + h),(255,0,0),5)
					frame_importante = frame_escogido
					self.bbox1 = box
					if retries > 0: 
						retries = 0
						print('object detected again :)')
				elif not success:
					retries += 1
					if retries > 10:
						break
				
				else:
					break
			cv2.imshow("Trackeron", frame)
			cv2.waitKey(1) & 0xFF
			frame_escogido += int(increment)
			iteration += 1
		video.release()
		cv2.destroyAllWindows()
		return(frame_importante, self.bbox1)       
	


	def IsHere(self, bbox, video_nombre, frame_escogido, frame_encuestion, fps):
		tracker = cv2.TrackerKCF_create()
		video = cv2.VideoCapture(video_nombre)
		video.set(cv2.CAP_PROP_POS_FRAMES, frame_escogido)
		ret, frame = video.read()
		if ret is False:
			print('video.read() es false')
			sys.exit()
 
		frame = cv2.resize(frame, None, fx=self.scale, fy=self.scale, interpolation = cv2.INTER_LINEAR)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				
		tracker.init(frame, bbox)

				
		cv2.imshow("Trackeron", frame)
		cv2.waitKey(1) & 0xFF
		video = cv2.VideoCapture(video_nombre)
		video.set(cv2.CAP_PROP_POS_FRAMES, frame_encuestion)
		ret, frame = video.read()
		if ret is False:
			print('video.read() es false')
 
		frame = cv2.resize(frame, None, fx=self.scale, fy=self.scale, interpolation = cv2.INTER_LINEAR)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		(success, box) = tracker.update(frame)
				
		cv2.imshow("Trackeron", frame)
		cv2.waitKey(1) & 0xFF

		video.release()
		cv2.destroyAllWindows()


		if success:        
			(x, y, w, h) = [int(v*self.scale) for v in box]
			cv2.rectangle(frame,(x, y), (w + x, y + h),(255,0,0),5)
			self.bbox1 = box
			cv2.imshow("Trackeron", frame)
			return self.bbox1

		elif not success:
			print('No object detection in that instant')
			return None
			
