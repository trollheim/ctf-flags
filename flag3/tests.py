from flag3.webapp import  Flag03;

flag = Flag03();


assert flag.filter("a<script>a") == 'aa'
assert flag.filter("a<scri<scri<script>pt>pt>a") == 'aa'
assert flag.filter("a<SCri<scri<script>pt>pt>a") == 'aa'