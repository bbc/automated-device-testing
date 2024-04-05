# video-testing-automation

## Installing Video Detection Module
```
git submodule update --init --recursive
pip install -r ExplainableVQA/requirements.txt

sed -i "" "92s/return x\[0\]/return x/" ExplainableVQA/open_clip/src/open_clip/modified_resnet.py
pip install -e ExplainableVQA/open_clip

sed -i "" "4s/decord/eva-decord/" ExplainableVQA/DOVER/requirements.txt
pip install -e ExplainableVQA/DOVER
mkdir ExplainableVQA/DOVER/pretrained_weights
wget https://github.com/VQAssessment/DOVER/releases/download/v0.1.0/DOVER.pth -P ExplainableVQA/DOVER/pretrained_weights/
```
