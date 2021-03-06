# -*- encoding: utf-8 -*-

import cv2
import os
import alpr
import sys
import gc

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)

def fail(message, code=None):
  print 'fail'
  print >> sys.stderr, message
  if code is not None:
    try:
      code=int(code)
    except:
      code=1
    finally:
      sys.exit(code)

if getattr(sys, 'frozen', False):
  #frozen
  exec_dir = os.path.dirname(sys.executable)
else:
  #unfrozen
  exec_dir = os.path.dirname(os.path.realpath(__file__))

try:
  crop_y=int(sys.argv[1])
  crop_x=int(sys.argv[2])
  crop_height=int(sys.argv[3])
  crop_width=int(sys.argv[4])
except:
  fail('Usage autonum_batch.py <crop_y> <crop_x> <crop_height> <crop_width>', -1)

datadir=os.path.join(exec_dir, 'data')

crop=((crop_y, crop_x), (crop_height, crop_width))
try:
  engine=alpr.Engine(datadir, crop, transform=None)
except Exception:
  fail('Coult not init ALPR engine', -1)

line = sys.stdin.readline()
while line:
  img_name=line.rstrip('\n\r')
  img = cv2.imread(img_name)

  if img is None:
    fail('Could not read '+img_name)
  else:
    try:
      plates=engine.detect(img, '')
      detected=(len(plates)>0)


      if detected:
        print "%s,%d,%d,%d,%d" % ((plates[0][0],)+plates[0][1])
      else:
        print '?'
    except:
      fail('General ALPR engine failure')

  #force garbage collection after engine.detect to avoid excessive memory usage
  gc.collect()
  line = sys.stdin.readline()
