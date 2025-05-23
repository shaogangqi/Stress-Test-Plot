const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

function getRandomUniqueInts(count, min, max) {
  const set = new Set();
  while (set.size < count) {
    set.add(Math.floor(Math.random() * (max - min + 1)) + min);
  }
  return Array.from(set);
}

test.describe.configure({ timeout: 30000000 });

test('Randomly test 1000 /plot/<n> endpoints from 1 to 99999 and save failed images', async ({ request }) => {
  const testCases = getRandomUniqueInts(1000, 1, 99999);
  const failedCases = [];

  // Create a folder to store failed plots if it doesn't exist
  const failedDir = path.join(__dirname, 'failed_plots');
  if (!fs.existsSync(failedDir)) {
    fs.mkdirSync(failedDir);
  }

  for (let n of testCases) {
    const url = `http://127.0.0.1:5000/plot/${n}`;
    const response = await request.get(url);

    const status = response.status();
    const contentType = response.headers()['content-type'];
    const buffer = await response.body();

    const isValid = status === 200 && contentType === 'image/png' && buffer.length >= 1000;

    if (!isValid) {
      // Save the failed image to disk
      const filePath = path.join(failedDir, `plot_${n}.png`);
      fs.writeFileSync(filePath, buffer);
      failedCases.push({ n, status, contentType, length: buffer.length });
      console.log(`❌ Failed at /plot/${n} — saved to failed_plots/plot_${n}.png`);
    } else {
      console.log(`✅ Passed /plot/${n}`);
    }
    const allPath = path.join(__dirname, 'all_plots', `plot_${n}.png`);
    fs.writeFileSync(allPath, buffer);
  }

  if (failedCases.length === 0) {
    console.log("All tests passed! The passing rate is 100%");
  }

  expect(failedCases.length, `Failures detected: ${JSON.stringify(failedCases, null, 2)}`).toBe(0);
});