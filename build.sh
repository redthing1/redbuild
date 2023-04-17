# 2. build redbuild2
pushd . && poetry install && poetry run python script/build_native.py && popd