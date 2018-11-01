const puppeteer = require('puppeteer');
function sleep(ms){
    return new Promise(resolve=>{
        setTimeout(resolve,ms)
    })
    }

(async () => {
  const browser = await puppeteer.launch();
   while(true){
  const page = await browser.newPage();


  await page.goto('http://localhost:8080');

  await page.type( '#msg', 'message' );
  await page.type( '#flag', 'flag' );
  await page.click( '#submit' );

  // Get the "viewport" of the page, as reported by the page.


  console.log('completed');
   await sleep(5000)
 }
  await browser.close();
})();