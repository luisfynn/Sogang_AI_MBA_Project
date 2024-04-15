# pose-estimation
#device 0 : gpu
conda activate yolov7pose

>>> python bicepcounter.py --source "./input/bicep.mp4" --device 0 --curltracker=True 



To draw the skeleton:
>>> python bicepcounter.py --source "./input/bicep.mp4" --device 0 --curltracker=True --drawskeleton=True

PushUp & To draw the skeleton:
>>> python bicepcounter.py --source 0 --drawskeleton true --pushuptracker true

curl & To draw the skeleton:
>>> python bicepcounter.py --source 0 --drawskeleton true --curltracker true