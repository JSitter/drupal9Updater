chmod 755 ./updater.py
allparams=${@}
scl enable rh-python35 "./updater.py $allparams"