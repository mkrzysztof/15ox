for test in *_test.py
do
    python3 $test
    if [[ $? -ne 0 ]]; then break; fi 
done

    
