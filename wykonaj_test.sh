for test in "alfa_beta_test.py" "siatka_test.py" "wartosciowanie_test.py"
do
    python3 $test
    if [[ $? -ne 0 ]]; then break; fi 
done

    
