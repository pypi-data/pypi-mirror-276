``` sh
# Installation for a package developer  
# this script installs package locally in the -e, or --editable mode

git clone https://gitlab.com/22kittens/pyvisjs.git
cd pyvisjs
git checkout dev
py -m venv .venv
.venv\\Scripts\\activate
py -m pip install -r requirements.txt
py -m pip install -e .
```

``` sh
# Installation for a package user

py -m venv .venv
.venv\\Scripts\\activate
py -m pip install pyvisjs
```
