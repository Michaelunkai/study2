const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ 
        headless: false,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        // Navigate to LinkedIn login page
        await page.goto('https://www.linkedin.com/login', { waitUntil: 'networkidle2', timeout: 60000 });

        // Log in
        await page.type('#username', 'yourmail@gmail.com', { delay: 100 });
        await page.type('#password', 'yourpassword!', { delay: 100 });
        await page.click('button[type="submit"]');

        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 });

        // Navigate to jobs section
        await page.goto('https://www.linkedin.com/jobs/', { waitUntil: 'networkidle2', timeout: 60000 });

        // Ensure the job search input is present before interacting
        await page.waitForSelector('input[placeholder="Search jobs"]', { timeout: 60000 });
        await page.waitForSelector('input[placeholder="Search location"]', { timeout: 60000 });

        // Search for jobs
        await page.type('input[placeholder="Search jobs"]', 'Software Engineer', { delay: 100 });
        await page.type('input[placeholder="Search location"]', 'New York, NY', { delay: 100 });
        await page.click('button.jobs-search-box__submit-button');

        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 });

        // Iterate through job listings and apply
        const jobListings = await page.$$('ul.jobs-search__results-list li');

        for (const job of jobListings) {
            await job.click();
            await page.waitForTimeout(2000); // Wait for the job details to load

            const applyButton = await page.$('button.jobs-apply-button');

            if (applyButton) {
                await applyButton.click();
                await page.waitForTimeout(2000); // Wait for the apply modal to load

                // Fill out the application form
                const submitButton = await page.$('button[data-control-name="submit_unify"]');
                if (submitButton) {
                    await submitButton.click();
                    await page.waitForTimeout(2000); // Wait for the application to submit
                }
            }
        }

    } catch (error) {
        console.error('Error during navigation:', error);
    } finally {
        await browser.close();
    }
})();
