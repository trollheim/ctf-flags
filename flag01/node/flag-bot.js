const puppeteer = require('puppeteer');


const fs = require('fs');
const readline = require('readline');

var path = process.cwd();
var buffer = fs.readFileSync(path + "//flag.txt");
var flag = buffer.toString().trim();

const readInterface = readline.createInterface({
    input: fs.createReadStream('users.txt'),
    output: process.stdout,
    console: false
});

var usercount = 0;

readInterface.on('line', function(line) {
    if (line.trim().length >0) usercount++;
});


function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
    }

(async () => {
  const browser = await puppeteer.launch({
  args : [ '--no-sandbox', '--disable-setupid-sandbox','--disable-de-shm-usage']
  });




   while(true) {


       for (var  i = 0; i < usercount; i++)
       {

       try {


           const page = await browser.newPage();

           var request = 'http://localhost:8080/bot/' + i;
           console.log('request [%s]', request);
           response = await page.goto(request );

           await page.waitFor('#msg');
           await page.type('#msg', 'message @'+Date.now());
           await page.waitFor('#flag');
           await page.type('#flag', flag);
           await page.waitFor('#userid');
           await page.type('#userid', ""+i);
           await page.waitFor('#submit');
           await page.click('#submit');
           await page.close()
       } catch (e) {
           console.log(e);
       }
       // Get the "viewport" of the page, as reported by the page.
   }

  console.log('completed');
   await sleep(5000)
 }
  await browser.close();
})();