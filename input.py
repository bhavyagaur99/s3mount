import os


def get_int(start='>>> ', end='', min_range='-inf', max_range='+inf', autoclrscr=False, retryonerror=True,
            print_value=False):
    number = 'Err'
    while True:
        okay = True
        if autoclrscr:  # Clear the screen before printing anything on the screen
            os.system('cls' if os.name == 'nt' else 'clear')

        msg = input(start)
        print(end, end='')

        try:
            number = int(msg)
        except Exception as e:
            print('Err:', e)
            input('Hit enter to continue  .  .  .')
            okay = False

        if min_range != '-inf' and okay:
            if number < min_range:
                print('Number must be greater than or equal to:', min_range)
                input('Hit enter to continue  .  .  .')
                okay = False

        if max_range != '+inf' and okay:
            if number > max_range:
                print('Number must be smaller than or equal to:', max_range)
                input('Hit enter to continue  .  .  .')
                okay = False

        if not okay:
            if not retryonerror:
                break
        else:
            break

    if print_value:
        print('Last input:', number)
    return number


def get_float(start='>>> ', end='', min_range='-inf', max_range='+inf', autoclrscr=False, retryonerror=True,
              print_value=False):
    number = 'Err'
    while True:
        okay = True
        if autoclrscr:  # Clear the screen before printing anything on the screen
            os.system('cls' if os.name == 'nt' else 'clear')

        msg = input(start)
        print(end, end='')

        try:
            number = float(msg)
        except Exception as e:
            print('Err:', e)
            input('Hit enter to continue  .  .  .')
            okay = False

        if min_range != '-inf' and okay:
            if number < min_range:
                print('Number must be greater than or equal to:', min_range)
                input('Hit enter to continue  .  .  .')
                okay = False

        if max_range != '+inf' and okay:
            if number > max_range:
                print('Number must be smaller than or equal to:', max_range)
                input('Hit enter to continue  .  .  .')
                okay = False

        if not okay:
            if not retryonerror:
                break
        else:
            break

    if print_value:
        print('Last input:', number)
    return number


def get_string(start='>>> ', end='\n', min_len=0, max_len='+inf', autoclrscr=False, retryonerror=True,
               print_value=False):
    msg = 'Err'
    while True:
        okay = False
        if autoclrscr:  # Clear the screen before printing anything on the screen
            os.system('cls' if os.name == 'nt' else 'clear')

        msg = input(start)
        print(end, end='')

        if min_len <= len(msg) <= max_len:
            okay = True
        else:
            print(f'The string must be between {min_len} and {max_len}')

        if not okay:
            if not retryonerror:
                break
        else:
            break

    if print_value:
        print('Last input:', msg)
    return msg


#get_int(start='Enter Int between 0 and 100 >>> ', min_range=0, max_range=100, print_value=True, retryonerror=False)