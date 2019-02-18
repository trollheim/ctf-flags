from flag2.webapp import  HelloWorld;

hello = HelloWorld();

assert hello.filter("a<string>a") == 'aa'
assert hello.filter("a<str<stri<string>ng>ing>a") == 'aa'
assert hello.filter("a<str<stri<str<//string>ing>ng>ing>a") == 'aa'
