const puppeteer = require('puppeteer');

(async () => {
  try {
    console.log('Launching browser...');
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    console.log('Navigating to the page...');
    await page.goto('https://youtube.com');
    console.log('Taking screenshot...');
    await page.screenshot({ path: '/mnt/c/Users/micha/pictures/fullpage.png', fullPage: true });
    console.log('Screenshot saved as /mnt/c/Users/micha/pictures/fullpage.png');
    await browser.close();
    console.log('Browser closed.');
  } catch (error) {
    console.error('Error:', error);
  }
})();
