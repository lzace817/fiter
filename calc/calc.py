from prefixed import Float

def calc():
    #TODO: better way to decide what is shown
    ignore =['i', 'j', 'x', 'y']
    #============================ PLAYGROUND ==================================







    x = 17
    c = x + 3
    a = 2*c
    b = 3*c

    del c # do not show c











    #==========================================================================
    print('\nResults:')
    vars = locals()
    for n in vars:
        if n not in ignore and n != 'ignore':
            print(f'{n} = {vars[n]}')


if __name__ == "__main__":
    calc()
