def display_dicts(dicts):
    c=0
    for dictionary in dicts:
        c+=1
        print("Dictionary:")
        for key, value in dictionary.items():
            print(f"{key}: {value}")
        print()
    print(f"Total dictionaries: {c}")

a = [{"test_method":"","test_parameter_id":7050020,"parameter_name":"Prothrombin Time","parameter_value":"12","is_highlighted":True,"lower_bound":"11","display_value":"11.0 - 15.0","upper_bound":"15","impression":"H","unit":"","other_male_id":"188"}]
display_dicts(a)