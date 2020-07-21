安装依赖库:

pip install -r requirements.txt



导出本地依赖文件清单到文件:

pip freeze > requirements.txt



设置以解决超过100M的单文件提交失败

```
git lfs install
git lfs track "*.dll"
git add .gitattributes
git add test.dll
git commit -m "commit"
git push origin master
```

