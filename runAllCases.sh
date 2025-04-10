for dir in *; do
    if [ -f "$dir/runCase.sh" ]; then
    	
    	cd $dir
        echo "Running $dir/runCase.sh"
        bash runCase.sh
        cd ..
    fi
done
