import joblib
import pathlib

pipe = joblib.load(str(pathlib.Path(__file__).parent).replace('\\','/')+'/Dormant/pipe')