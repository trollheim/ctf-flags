from flag2.webapp import  Flag02;

flag = Flag02();

assert flag.filter("a<script>a") == 'aa'
assert flag.filter("a<scri<scri<script>pt>pt>a") == 'aa'
assert flag.filter("a<SCri<scri<script>pt>pt>a") == 'a<SCript>a'

