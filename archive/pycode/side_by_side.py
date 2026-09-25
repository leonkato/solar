def side_by_side(*objs, **kwds):
    from pandas.io.formats.printing import adjoin
    space = kwds.get('space', 4)
    reprs = [repr(obj).split('\n') for obj in objs]
    print(adjoin(space, *reprs))

# tdf = pd.DataFrame(np.arange(12).reshape(4, 3), index=list ('abcd'), columns=list('wxy'))

# udf= pd.DataFrame(np.arange(100, 112).reshape(4, 3), index=list ('abcd'), columns=list('wxy'))

# side_by_side(tdf, udf)

