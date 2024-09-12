from datemath import datemath, __version__



print(f'datemath version is {__version__}')


print(f'Now is: {datemath("now")}')
print(f'1 hour was ago was: {datemath("now-1h")}')
print(f'1 week from now is {datemath("now+1w/w")}')
print(f'1 year from now is {datemath("+1y")}')

