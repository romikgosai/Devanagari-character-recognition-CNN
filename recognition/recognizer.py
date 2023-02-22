import tensorflow as tf
import numpy as np
from PIL import Image
import scipy.signal
import cv2
import os


def recognizer(image_data):
  file_name = os.path.dirname(__file__) +'\\model.h5'
  print(file_name)
  model = tf.keras.models.load_model(file_name)
  image  = Image.open(image_data)
  image_data = np.array(image)
  grayscale = np.zeros((image_data.shape[0], image_data.shape[1]))
  for i in range(len(image_data)):
      for j in range(len(image_data[i])):
          grayscale[i][j] = image_data[i][j][0]/3 + \
              image_data[i][j][1]/3 + image_data[i][j][2]/3
  filtered_image = scipy.signal.medfilt2d(grayscale, kernel_size=5)
  def binarized(image_data):
      row, column = image_data.shape
      for i in range(row):
          for j in range(column):
              if image_data[i][j] > 127:
                  image_data[i][j] = 0
              else:
                  image_data[i][j] = 255
      return image_data
  inverted_binarized_image = binarized(filtered_image)
  def universe_of_discourse(image_data):
      row, column = len(image_data), len(image_data[0])

      def minimumrow():
          for i in range(row):
              for j in range(column):
                  if image_data[i+5, j] == 255:
                      min_row = i+5
                      return min_row

      def minimumcolumn():
          for i in range(column):
              for j in range(row):
                  if image_data[j, i+5] == 255:
                      min_column = i+5
                      return min_column

      def maximumrow(row, column):
          i = 0
          while (1):
              row = row-1
              for i in range(column):
                  if image_data[row-5, i] == 255:
                      return row-5

      def maximumcolumn(row, column):
          i = 0
          while (1):
              column = column - 1
              for i in range(row):
                  if image_data[i, column-5] == 255:
                      return column-5
      min_row, min_column, max_row, max_column = int(minimumrow()), int(
          minimumcolumn()), int(maximumrow(row, column)), int(maximumcolumn(row, column))
      if min_row >= row//25:
          min_row = min_row - row//25
      if min_column >= column//25:
          min_column = min_column - column//25
      if max_row < 24*row//25:
          max_row = max_row + row//25
      if max_column < 24*column//25:
          max_column = max_column + column//25

      image_data = image_data[min_row:max_row, min_column:max_column]
      return image_data


  cropped_image = universe_of_discourse(inverted_binarized_image)

  im = Image.fromarray(cropped_image)
  normalized_image = im.resize((32, 32))

  normalized_image_data = np.array(normalized_image)

  normalized_image_data = normalized_image_data/255.0
  normalized_image_data = normalized_image_data.reshape(1, 32, 32, 1)
  predictions = model.predict(normalized_image_data)
  return np.argmax(predictions).item()
