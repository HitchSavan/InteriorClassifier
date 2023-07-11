def progressbar(total_items, iter, bar_len = 40):
    filled_len = int(round(bar_len * iter / float(total_items)))
    percents = round(100.0 * iter / float(total_items), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    print(f'[{bar}] {percents}%\r', end='\r')
    return iter+1