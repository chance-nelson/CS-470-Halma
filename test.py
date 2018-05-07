from Halma import Halma
from Player import Node, MiniMax
import time

test = Halma(8, 0, 2)
timeStamp = time.time()
m = MiniMax(test, 9999999999)
print("Done! Took ", time.time() - timeStamp)
