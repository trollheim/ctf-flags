from flag04.webapp import  HelloWorld;

hello = HelloWorld();

assert hello.filter("1+1") == '1+1'
assert hello.filter("1[ssss]1d+s1aaa") == '1[]1+1'
assert hello.filter("!@£$%^&*()_-+=") == '!@£$%^&*()_-+='
