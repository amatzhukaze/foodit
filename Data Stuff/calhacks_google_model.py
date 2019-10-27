# -*- coding: utf-8 -*-
"""CalHacks Google Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1grtjGTaZUHoH_t659nTHhDauSw9E5AJb

# YEEHAW
"""

# Commented out IPython magic to ensure Python compatibility.
def __main__(url):

  def script(user_uploaded_image_url):

    #!export GOOGLE_APPLICATION_CREDENTIALS="instafoody-3a8750af0e73.json"

    !pip install --upgrade google-cloud-vision
    from google.cloud import vision
    import io
    import os

    import pandas as po
    import numpy as np
    import re


    #GOOGLE_APPLICATION_CREDENTIALS
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']="instafoody-3a8750af0e73.json"

    #with open('instafoody-3a8750af0e73.json', 'r') as f:
    #    %env GOOGLE_APPLICATION_CREDENTIALS=f

#     %env GOOGLE_APPLICATION_CREDENTIALS=Miscellaneous/instafoody-3a8750af0e73.json

    def detect_labels(path):
        """Detects labels in the file."""
        the_labels = []

        client = vision.ImageAnnotatorClient()


        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        print(content)
        image = vision.types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels:')

        for label in labels:
            #print(label.description)
            the_labels.append(label)
        return the_labels




    """
    Arguments: the image url to a user-uploaded url xxxxxxxxxxx....xxxx.jpg

    Returns probability/score associated with match; image associated with the match; restaurant associated with match; address of restaurant as a JSON file
        # essentially a row in DATA
    """

    import random
    import string

    import numpy as np
    import pandas as po

    import re

    def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    path = "user_images/"+randomString()+".jpg"
    urllib.request.urlretrieve(user_uploaded_image_url, path)

    # Get labels of the user image
    labels = detect_labels(path = path)

    # Compare labels to all labels in dataset;

    ### Algorithm: MAX(sum(matching_labels) for each restaurant)
    ###### Reasoning: Null hypothesis: each restaurant equally likely to have this dish;
       ###### Any significant bias towards a restaurant will indicate association
        ###### The current restaurant selection covers a wide range of international cuisine,
          ###### so homogenous scoring items will be assumed to be garbage/not food


    user_img_dictionary = {}

    word_identifiers = re.findall(r'"(\w+)"\nscore', str(labels))
    word_scores = re.findall(r'score: (\d\.\d+)', str(labels))

    for id, score in zip(word_identifiers, word_scores):
      user_img_dictionary[id] = score


    def sum_function(g):
      summm = 0
      for row_dict in po.Series(g):
        shared_items = {k: row_dict[k] for k in row_dict if k in user_img_dictionary}
        summm+=sum(list(shared_items.values()))
      return summm

    DATA_grouped = DATA[["Restaurant name", "Label: Score"]].groupby("Restaurant name").agg(sum_function)


    ### 1 of 4: GOT RESTAURANT NAME
    winning_restaurant = DATA_grouped.iloc[:,0].idxmax() # recall, index is now restaurant name

    ### 2 of 4: GOT RESTAURANT ADDRESS
    winning_address = DATA[DATA["Restaurant name"] == winning_restaurant]['Address'].iloc[0]

    ### 3 of 4: GET IMAGE THAT LOOKS MOST LIKE THE IMAGE

    # Criteria 1: Shares the most/alot of keys

    max_shares = 0
    index_max = 0
    i = 0 # for index of row that has max
    for row_dict in DATA[DATA[winning_address]]["Label: Score"]:
      shared_items = {k: row_dict[k] for k in row_dict if k in user_img_dictionary}
      if len(shared_items) > max_shares:
        max_shares = len(shared_items)
        index_max = i 
      i+=1

    winning_image = DATA.loc[i, "Food image"]

    ### 4 of 4: IMAGE SCORE
    # average of matching labels scores

    score = np.mean(list(shared_items.values()))


    return {"best_score": score, "best_image": winning_image, "best_restaurant": winning_restaurant, "best_address": winning_address}
  
  
  
  
  
  script(url)