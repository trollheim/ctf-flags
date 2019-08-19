const puppeteer = require('puppeteer');


var fs = require('fs');
var path = process.cwd();
var buffer = fs.readFileSync(path + "//flag.txt");
var flag = buffer.toString().trim();


function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
    }

(async () => {
  const browser = await puppeteer.launch({
  args : [ '--no-sandbox', '--disable-setupid-sandbox','--disable-de-shm-usage']
  });




   while(true){
       try {


           const page = await browser.newPage();


           response = await page.goto('http://localhost:8080/bot');

           await page.waitFor('#msg');
           await page.type('#msg', 'message');
           await page.waitFor('#flag');
           await page.type('#flag', flag);
           await page.waitFor('#submit');
           await page.click('#submit');
       } catch (e) {
           console.log(e);
       }
  // Get the "viewport" of the page, as reported by the page.


  console.log('completed');
   await sleep(5000)
 }
  await browser.close();
})();