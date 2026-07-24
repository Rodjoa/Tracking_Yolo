def get_date_and_time(self, frame):

        ROI_DateTime = frame[0:100, 0:550]
        #cv2.imshow("cut",ROI_DateTime) #Debug para ver si la ROI está acorde a las dimensiones del texto en la foto
        texto = pytesseract.image_to_string(ROI_DateTime).strip()
        

        if texto and texto != self.prev_texto:

            try:
                dt = datetime.strptime(texto, '%Y-%m-%d %H:%M:%S')

                self.current_date = dt.date()
                self.current_time = dt.time()

                self.prev_texto = texto

            except ValueError:
                pass

        return  self.current_time, self.current_date