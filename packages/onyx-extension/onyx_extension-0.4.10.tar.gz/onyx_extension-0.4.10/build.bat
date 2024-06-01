#     conda activate jupyterlab-ext

pip install -ve .

jlpm install
jlpm run build

jupyter lab


Release:

python -m build
twine upload dist/* -u=__token__ -p=pypi-massive_token_code
