for dir in */; do
    if [ -f "$dir/runCase.sh" ]; then
        echo "Running $dir/runCase.sh"
        bash "$dir/runCase.sh"
    fi
done
