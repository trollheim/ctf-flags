from flag3.webapp import  HelloWorld;

hello = HelloWorld();

assert hello.filter("a<script>a") == 'aa'
assert hello.filter("a<scri<scri<script>pt>pt>a") == 'aa'
assert hello.filter("a<SCri<scri<script>pt>pt>a") == 'aa'