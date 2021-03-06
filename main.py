from src.model.tfmodel import TFModel
from src.coinclasses.coinlabel import CoinLabel
from src.model import model3c2d as model
import sys

#Main file for training different model variants

def train_model(label, save_name, coin_prop ):
    coinlabel = CoinLabel('/data', '/home/ubuntu/coin-ID/data/IDnamegrade.csv',
                                            coin_prop, label, random_state = model.SEED)
    if coin_prop == 'rad':
        tfm =  TFModel(model.encode_rad, '/home/ubuntu/coin-ID/data/saves/' + save_name)
    else:
        tfm =  TFModel(model.encode_img, '/home/ubuntu/coin-ID/data/saves/' + save_name)
    return tfm, coinlabel


if __name__ == '__main__':
    if sys.argv[1] == '1':
        tfm, coinlabel = train_model('grade_lbl', 'm_rad_v' + sys.argv[2], 'rad')
        if '-t' in sys.argv:
            tfm.fit(coinlabel)
        score = tfm.evaluate(coinlabel)
        print score
    if sys.argv[1] == '2':
        tfm, coinlabel = train_model('grade_lbl', 'm_cr_v' + sys.argv[2], 'cr')
        if '-t' in sys.argv:
            tfm.fit(coinlabel)
        score = tfm.evaluate(coinlabel)
        print score
    if sys.argv[1] == '3':
        tfm, coinlabel = train_model('grade_lbl', 'm_cr_log_v' + sys.argv[2], 'cr')
        if '-t' in sys.argv:
            tfm.fit(coinlabel, use_logit = True)
        score = tfm.evaluate(coinlabel,use_logit = True)
        print score
    if sys.argv[1] == '4':
        tfm, coinlabel = train_model('grade_lbl', 'm_cr_no_do_v' + sys.argv[2], 'cr')
        if '-t' in sys.argv:
            tfm.fit(coinlabel)
        score = tfm.evaluate(coinlabel)
        print score
    if sys.argv[1] == '5':
        tfm, coinlabel = train_model('grade_lbl', 'm_cr_nobalance_v' + sys.argv[2], 'cr')
        if '-t' in sys.argv:
            tfm.fit(coinlabel, balance_classes = False)
        score = tfm.evaluate(coinlabel)
        print score
    if sys.argv[1] == '6':
        tfm, coinlabel = train_model('name_lbl', 'm_cr_name_v' + sys.argv[2], 'cr')
        if '-t' in sys.argv:
            tfm.fit(coinlabel, grade = False)
        score = tfm.evaluate(coinlabel, grade = False)
        print score

    if sys.argv[1] == '7':
        tfm, coinlabel = train_model('name_lbl', 'm_img_name_v' + sys.argv[2], 'img')
        if '-t' in sys.argv:
            tfm.fit(coinlabel, grade = False)
        score = tfm.evaluate(coinlabel, grade = False)
        print score

    if sys.argv[1] == '8':
        tfm, coinlabel = train_model('grade_lbl', 'm_img_logit_v' + sys.argv[2], 'img')
        if '-t' in sys.argv:
            tfm.fit(coinlabel)
        score = tfm.evaluate(coinlabel)
        print score
