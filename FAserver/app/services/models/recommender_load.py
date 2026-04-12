import os

import joblib
import numpy as np

from app.core.common_utils import CommonUtils
from app.core.settings import REC_NAME, WEIGHTS_DIR


class RecommendationLoader:

    def __init__(self):
        """
              cwd = os.getcwd()
              cwd_ = cwd.split("\\")
              path = cwd_[0]
              for c in cwd_[1:-3]:
                  path = path + "\\" + c
              """
        #path = CommonUtils.get_global_project_root()
        #texts_file_path = path + "\\weights_for_ML\\" + REC_NAME
        texts_file_path = os.path.join(WEIGHTS_DIR, REC_NAME)
        if not os.path.exists(texts_file_path):
            raise FileNotFoundError(f"Weights not found: {texts_file_path}")
        else:
            print(f"Loading weights from: {texts_file_path}")

        data = joblib.load(texts_file_path)
        self.embeddings = []
        for item in data["data"]:
            self.embeddings.append(item)

        self.embeddings = np.asarray(self.embeddings)

