import cv2, sys      #la version con mas contrib



class trackeron:

    def single_file(self, bbox, video, timecode_in):
        video = cv2.VideoCapture(timecode_in.video[0])
        fps = round(video.get(cv2.CAP_PROP_FPS))

        frame_escogido = timecode_in * fps
        increment = 1
        tc_salida = self.track(bbox, video, frame_escogido, increment)
        tc_salida = tc_salida/fps
        frame_escogido = timecode_in * fps
        increment = -1
        tc_entrada = self.track(bbox, video, frame_escogido, increment)
        tc_entrada = tc_entrada/fps
        tc_detection = []
        tc_detection[0] = tc_entrada
        tc_detection[1] = tc_salida
        return tc_detection


    def track(self, bbox, video, frame_escogido, increment):
        tracker = cv2.TrackerKCF_create()
        xa, xb, ya, yb = bbox
        bboxes = tuple([xa, ya, xb - xa, yb - ya])
    
        self.scale = 1
        retries = 0
        iteration = 0
        frame_importante = frame_escogido
        while video.isOpened():
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_escogido)
            ret, frame = video.read()
            if ret is False:
                print('video.read() es false')
                break
            frame = cv2.resize(frame, None, fx=self.scale, fy=self.scale, interpolation = cv2.INTER_LINEAR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BG2GRAY)
                
            if iteration == 0:
                tracker.init(frame, bboxes)
            elif iteration > 1:
                (success, box) = tracker.update(frame)
                if success:
                    (x, y, w, h) = [int(v*self.scale) for v in box]
                    cv2.rectangle(frame,(x, y), (w + x, y + h),(255,0,0),5)
                    frame_importante = frame_escogido
                    # if self.show_frames:
                    #     cv2.imshow(frame)
                    if retries > 0: 
                        retries = 0
                        print('object detected again :)')
                elif not success:
                    retries += 1
                else:
                    break
            frame_escogido += increment
            iteration += 1
        video.release()
        cv2.destroyAllWindows()
        return frame_importante


    
        


                