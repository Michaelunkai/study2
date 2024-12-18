import os

# JavaScript bookmarklets and their names
bookmarklets = {
    "Toggle Grayscale Mode": "(function() { document.body.style.filter = 'grayscale(1)'; })();",
    "Blur All Images": "(function() { document.querySelectorAll('img').forEach(img => img.style.filter = 'blur(10px)'); })();",
    "Remove Videos": "(function() { document.querySelectorAll('video').forEach(video => video.remove()); })();",
    "Change All Links to Buttons": "(function() { document.querySelectorAll('a').forEach(link => { link.outerHTML = `<button>${link.textContent}</button>`; }); })();",
    "Scroll Down by 500px": "(function() { window.scrollBy(0, 500); })();",
    "Scroll Up by 500px": "(function() { window.scrollBy(0, -500); })();",
    "Count Number of Images on Page": "(function() { alert(`Number of images: ${document.querySelectorAll('img').length}`); })();",
    "Find Broken Images": "(function() { document.querySelectorAll('img').forEach(img => { if (!img.complete || img.naturalWidth === 0) console.log(img.src); }); })();",
    "Make All Links Absolute": "(function() { document.querySelectorAll('a').forEach(link => link.href = link.href); })();",
    "Convert All Images to Black and White": "(function() { document.querySelectorAll('img').forEach(img => img.style.filter = 'grayscale(100%)'); })();",
    "Show Hidden Text Inputs": "(function() { document.querySelectorAll('input[type=\"hidden\"]').forEach(input => input.type = 'text'); })();",
    "Remove Stylesheets": "(function() { document.querySelectorAll('link[rel=\"stylesheet\"]').forEach(link => link.remove()); })();",
    "Hide Footer": "(function() { document.querySelectorAll('footer').forEach(footer => footer.style.display = 'none'); })();",
    "Display Form Field Names": "(function() { document.querySelectorAll('input, select, textarea').forEach(el => el.placeholder = el.name || 'Unnamed'); })();",
    "Toggle Background Color": "(function() { document.body.style.backgroundColor = document.body.style.backgroundColor === 'black' ? '' : 'black'; })();",
    "Outline All Elements": "(function() { document.querySelectorAll('*').forEach(el => el.style.outline = '1px solid red'); })();",
    "Redirect to HTTP": "(function() { location.href = location.href.replace('https://', 'http://'); })();",
    "Toggle All Images Visibility": "(function() { document.querySelectorAll('img').forEach(img => img.style.display = img.style.display === 'none' ? '' : 'none'); })();",
    "Focus on First Input Field": "(function() { document.querySelector('input').focus(); })();",
    "Highlight Elements with Inline Styles": "(function() { document.querySelectorAll('*').forEach(el => { if (el.style.length) el.style.border = '2px solid blue'; }); })();",
    "Open Current Page in Wayback Machine": "(function() { window.open('https://web.archive.org/web/*/' + location.href); })();",
    "Redirect All Links to HTTPS": "(function() { document.querySelectorAll('a').forEach(link => link.href = link.href.replace('http://', 'https://')); })();",
    "Save All Text on Page to a File": "(function() { const text = document.body.innerText; const blob = new Blob([text], {type: 'text/plain'}); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'page_text.txt'; a.click(); })();",
    "Reverse Image Search": "(function() { let imgSrc = prompt('Enter image URL to reverse search:'); if (imgSrc) window.open('https://www.google.com/searchbyimage?image_url=' + encodeURIComponent(imgSrc)); })();",
    "Count All Buttons": "(function() { alert('Total buttons on page: ' + document.querySelectorAll('button').length); })();",
    "Disable All Links": "(function() { document.querySelectorAll('a').forEach(link => link.href = 'javascript:void(0)'); })();",
    "Replace All Text with Emojis": "(function() { document.body.innerHTML = document.body.innerHTML.replace(/\\w+/g, '😀'); })();",
    "Make Page Content Unselectable": "(function() { document.body.style.userSelect = 'none'; })();",
    "Show All Hidden Elements": "(function() { document.querySelectorAll('*').forEach(el => { if (el.style.display === 'none') el.style.display = ''; }); })();",
    "List All Media Files": "(function() { let media = [...document.querySelectorAll('img, video, audio')].map(el => el.src); alert(media.join('\\n')); })();",
    "Force Download Links": "(function() { document.querySelectorAll('a').forEach(link => link.download = true); })();",
    "Disable All Buttons": "(function() { document.querySelectorAll('button').forEach(btn => btn.disabled = true); })();",
    "Show Hidden iFrames": "(function() { document.querySelectorAll('iframe').forEach(frame => frame.style.display = 'block'); })();",
    "Redirect to Mobile Version": "(function() { location.href = location.href.replace('www.', 'm.'); })();",
    "Toggle Light/Dark Mode": "(function() { document.body.classList.toggle('dark-mode'); })();",
    "Highlight All Forms": "(function() { document.querySelectorAll('form').forEach(form => form.style.border = '2px solid green'); })();",
    "Remove All iframes": "(function() { document.querySelectorAll('iframe').forEach(frame => frame.remove()); })();",
    "Mute All Audio": "(function() { document.querySelectorAll('audio').forEach(audio => audio.muted = true); })();",
    "Display Image Dimensions": "(function() { document.querySelectorAll('img').forEach(img => console.log(`Image: ${img.src}, Width: ${img.width}, Height: ${img.height}`)); })();",
    "Highlight H1 Tags": "(function() { document.querySelectorAll('h1').forEach(h1 => h1.style.backgroundColor = 'yellow'); })();",
    "List All JavaScript Files": "(function() { let scripts = [...document.querySelectorAll('script[src]')].map(s => s.src); alert(scripts.join('\\n')); })();",
    "Sort List Items Alphabetically": "(function() { document.querySelectorAll('ul').forEach(ul => { let items = [...ul.children]; items.sort((a, b) => a.textContent.localeCompare(b.textContent)); ul.innerHTML = ''; items.forEach(item => ul.appendChild(item)); }); })();",
    "Toggle Visibility of Headers": "(function() { document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => h.style.display = h.style.display === 'none' ? '' : 'none'); })();",
    "Make All Buttons Red": "(function() { document.querySelectorAll('button').forEach(btn => btn.style.backgroundColor = 'red'); })();",
    "Find External Links": "(function() { document.querySelectorAll('a').forEach(link => { if (!link.href.includes(location.hostname)) console.log(link.href); }); })();",
    "Disable Scrolling": "(function() { document.body.style.overflow = 'hidden'; })();",
    "Count All Paragraphs": "(function() { alert('Number of paragraphs: ' + document.querySelectorAll('p').length); })();",
    "Sort Table Rows Alphabetically": "(function() { document.querySelectorAll('table').forEach(table => { let rows = Array.from(table.rows).slice(1); rows.sort((a, b) => a.cells[0].textContent.localeCompare(b.cells[0].textContent)); rows.forEach(row => table.tBodies[0].appendChild(row)); }); })();",
    "Highlight Inline Scripts": "(function() { document.querySelectorAll('script:not([src])').forEach(script => script.style.backgroundColor = 'yellow'); })();",
    "Random Background Color": "(function() { document.body.style.backgroundColor = '#' + Math.floor(Math.random()*16777215).toString(16); })();"
}

# Create the files
for name, code in bookmarklets.items():
    # Replace invalid characters in file names with underscores
    file_name = f"{name.replace(' ', '_').replace('/', '_')}.txt"
    with open(file_name, "w") as file:
        file.write(code)

print("50 JavaScript files have been created in the current directory.")
