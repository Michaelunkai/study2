// popup.js
document.addEventListener('DOMContentLoaded', function() {
    const captureBtn = document.getElementById('captureBtn');
    const status = document.getElementById('status');

    captureBtn.addEventListener('click', async () => {
        try {
            // Get the current active tab
            const [tab] = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            // Update status
            status.textContent = 'Taking screenshot...';

            // Capture the visible tab
            const screenshot = await chrome.tabs.captureVisibleTab(null, {
                format: 'png'
            });

            // Generate filename with timestamp
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const filename = `screenshot-${timestamp}.png`;

            // Download the screenshot
            await chrome.downloads.download({
                url: screenshot,
                filename: filename,
                saveAs: false
            });

            // Update status and close popup after successful capture
            status.textContent = 'Screenshot saved!';
            setTimeout(() => {
                window.close();
            }, 1000);

        } catch (error) {
            status.textContent = 'Error: ' + error.message;
            console.error('Screenshot error:', error);
        }
    });
});
