// Install puppeteer using `npm install puppeteer querystring`
const puppeteer = require('puppeteer');
const querystring = require('querystring');

(async () => {
  const browser = await puppeteer.launch({ headless: false }); // Set to true if you want headless browsing
  const page = await browser.newPage();

  // Intercept network requests
  await page.setRequestInterception(true);
  page.on('request', (request) => {
    if (request.url().includes('degree-search') && request.method() === 'POST') {
      const postData = request.postData();
      try {
        const parsedData = querystring.parse(postData);
        if (parsedData['ep.c_search_term']) {
          console.log('Search Term:', parsedData['ep.c_search_term']);
        }
      } catch (e) {
        console.error('Error parsing request payload:', e);
      }
    }
    request.continue();
  });

  // Navigate to the target URL
  await page.goto('https://degree-search.nau.edu/search/?ac=ugrd&dm=INPER,ONLIN', {
    waitUntil: 'networkidle2',
  });

  // Click on every div with the class 'listSegment'
  while (true) {
    const segments = await page.$$('.listSegment');
    if (segments.length === 0) break;

    for (const segment of segments) {
      try {
        await segment.click();
        // Wait for a short interval to ensure the request is captured
        await new Promise((resolve) => setTimeout(resolve, 1000));
      } catch (e) {
        console.error('Error clicking element:', e);
      }
    }

    // Refresh the list of elements in case DOM changes
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  await browser.close();
})();
