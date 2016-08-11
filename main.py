from model.tfmodel import TFModel
from src.coinclasses.coinlabel import CoinLabel
from model import model3c2d
import cPickle as pickle
import os

def main():
        tfm = TFModel(model3c2d.encode_rad, 'rad_cropped_3c2d')
        coinlabel = CoinLabel('/data2/processed/cropped/', '/home/ubuntu/coin/data/IDlabel.csv',
                                'rad', 'grade_lbl', random_state = model3c2d.SEED)
        test = tfm.fit(coinlabel, 100)

        # tfm.evaluate(coinlabel)

if __name__ == '__main__':
    main()
