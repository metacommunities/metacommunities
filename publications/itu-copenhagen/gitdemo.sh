# make a directory or folder
mkdir demo
cd demo
# create a git repo
git init
# make some files
touch file1.txt
touch file2.txt
touch readme.md
# add files
git add *.*
# commit files
git commit -a -m 'setting up repo'
# add remote repository
git remote add origin https://github.com/rian39/demo
git push -u origin master

# clone the repository somewhere
cd ..
mkdir demo_clone
cd demo_clone
git clone https://github.com/rian39/demo

#cleanup 

cd ..
rm -Rf demo
rm -Rf demo_clone