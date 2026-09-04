const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
  page.on('requestfailed', request => console.log('REQUEST FAILED:', request.url(), request.failure().errorText));

  // Navigate to login
  await page.goto('http://localhost:5173/login');
  await page.type('input[type="text"]', '2023CSE0001');
  await page.type('input[type="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  await page.waitForNavigation();
  
  // Navigate to the chat page
  await page.goto('http://localhost:5173/chat?branch=CSE&sem=Semester-3&subject=BSM-202', {waitUntil: 'networkidle0'});
  
  await browser.close();
})();
