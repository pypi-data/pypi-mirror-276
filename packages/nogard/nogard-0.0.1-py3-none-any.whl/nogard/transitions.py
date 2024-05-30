def modifications(instance):
    print(f'In class: {instance.__annotations__}')
    
    for var, _type in instance.__annotations__.items():
        _t = get_bare_type(_type)

        if _t and not re.search('__main__.*', str(_t)):
            print(var, _t)
        else:
            base = getattr(instance, var)
            # Only one-layer of indirect for now
            # Remember tuples can have multiple type parameters
            ## Important to note it doesn't support unions
            if (res := get_bare_type(type(base))) not in base_types:
                match res:
                    case 'tuple':
                        types = []
                        
                        for item in base:
                            types.append(get_bare_type(type(item)))
                        print(f'{var} is of type {res} {types}')
                        
                        instance.__annotations__[var] = tuple[int]
                    case re.search('__main__.*', str(res)):
                        print('CLASS')
                    case _:
                        print(f'{var} is of type {res} {type(base[0])}')#, var.__type_params__) 
            else:
                print(var, res)
