git status
git add .
git commit -m 'auto_commit'
git push origin server_version
pipenv run fab deploy
exit