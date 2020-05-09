echo "Cleaning"
make clean

echo "Generating pdf and md files"
make

echo "Start jekyll server"
make web
