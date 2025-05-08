with open('num_of_users.txt', 'r') as file:
    for line in file:
        user, access_count = line.split(', アクセス回数: ')
        if int(access_count) > 1000:
            print(user, access_count)