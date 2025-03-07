#!\bin\sh

echo "Clearing the case using foam"
pyFoamClearCase.py .

echo "Removing base case"
rm -r 0

echo "Finding and removing directories matching the pattern processor[0-9]+"
find . -type d -regextype posix-extended -regex ".*/processor[0-9]+" -exec rm -r {} +

echo "Case cleaned"
