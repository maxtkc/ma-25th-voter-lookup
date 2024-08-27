---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

## See which of your Facebook friends are registered to vote in Evan's district

> Follow these instructions to see which of your Facebook friends vote in Evan's district. If you get stuck or have any trouble,
reach out to `maxkatzchristy@gmail.com`. Provide your phone number and I will
call you to help you make it work. Voting for this election has already started and will end Sept. 3 (the Tuesday after Labor Day)!

1. Log into Facebook and go to your friend list page: [https://www.facebook.com/friends/list](https://www.facebook.com/friends/list){:target="_blank"}
> Note: This has been tested in Chrome, Firefox, and Chromium. On safari this additional step must be taken before starting: [https://support.apple.com/guide/safari/use-the-developer-tools-in-the-develop-menu-sfri20948/mac](https://support.apple.com/guide/safari/use-the-developer-tools-in-the-develop-menu-sfri20948/mac). It may also work on other browsers.
2. Scroll all the way to the bottom of the page. Keep scrolling until you cannot scroll any further. (This will load all of your friends so you can export them to a file. I know, this is so tedious; you are so popular!)
3. Right click anywhere on the page and click `Inspect`, opening the developer tools (This might look scary, but hang in there!)
4. Click on `Console` (it should be one of the tabs next to `Elements` or `Inspector` in the popup that has just come up). You're going to see it say things like *STOP*, etc. Unfortunately Facebook doesn't make this easy for us, but what we're doing keeps all of your data on your computer, so it is very safe. 
5. If instructed (likely in Chrome), type the text "allow pasting" (without the quotes) and hit enter. You may be able to skip this step, but it won't break anything if you do it.
6. Copy and paste the following code into the text box at the very bottom of the page, past all of the messages, where you see a `>` or a `>>`. Press enter. You should see a file called `friendsList.json` downloaded into your `Downloads` folder.
```javascript
    var exportObj = [];
    for (var el of document.querySelectorAll('[data-visualcompletion="ignore-dynamic"]')) {
        var name = el.getAttribute("aria-label");
        if(name!= null && name != "null"){
            exportObj.push(name);
        }else{
            var a = el.getElementsByTagName("a")[0];
        }
    }

    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", "friendsList.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
```

7. Now you're ready to see which friends are in Evan's district. The file will
   be in your `Downloads` folder and named `friendsList.json`. Click `Browse...` below, and
   select that file. Then click `Search`. This search may take a few moments because you
   have so many friends. The file is never uploaded to a server or anything,
   all of your data will stay on your computer. Of course, use at your own risk.

<script src="https://cdn.jsdelivr.net/npm/fuse.js/dist/fuse.js"></script>
<form id="friends-lookup">
    <input id="friendslist" type="file" />
    <br>
    <button type="submit">Search!</button>
</form>

<ul id="output"></ul>

<script>
    async function sleep() {
      return new Promise((resolve) => setTimeout(resolve, 10));
    }

    const to_li = (result) => `<li>${result.item["Full Name"]}, age ${result.item.Age}</li>`;
    let fuse;
    function processForm(e) {
        if (e.preventDefault) e.preventDefault();

        try {
            const files = document.getElementById("friendslist").files;
            if (files.length === 0) {
                throw new Error("Please select a file to search");
            }
            const fr = new FileReader();
            fr.readAsText(files[0]);
            fr.addEventListener(
                "load",
                async () => {
                    const friends = JSON.parse(fr.result);
                    const matches = [];
                    let i = 0;
                    for (const friend of friends) {
                        document.getElementById("output").innerHTML = `Searching... (${Math.round(++i / friends.length * 100)}%)`;
                        await sleep();
                        const results = fuse.search(friend);
                        if (results.length > 0) {
                            matches.push(results[0]);
                        }
                    }
                    document.getElementById("output").innerHTML = matches.map(to_li).join("");
                },
                false,
            );
        } catch (error) {
            document.getElementById("output").innerHTML = `Something went wrong: ${error.message}`;
            console.error(error.message);
        }

        // You must return false to prevent the default form behavior
        return false;
    }

    var form = document.getElementById('friends-lookup');
    if (form.attachEvent) {
        form.attachEvent("submit", processForm);
    } else {
        form.addEventListener("submit", processForm);
    }


    async function getData() {
        const url = "voters.json";
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const list = await response.json();
            const options = {
                includeScore: true,
                // Search in `author` and in `tags` array
                keys: ['Full Name'],
                threshold: 0.2,
            }

            fuse = new Fuse(list, options)
        } catch (error) {
            document.getElementById("output").innerHTML = `Sorry messed up: ${error.message}`;
            console.error(error.message);
        }
    }
    getData();
</script>

> Note: Searches are based solely on first and last name and are not
necessarily accurate nor complete.

> These instructions have been adapted from: [https://stackoverflow.com/questions/50095522/how-to-get-whole-facebook-friends-list-from-api](https://stackoverflow.com/questions/50095522/how-to-get-whole-facebook-friends-list-from-api)

## Search for an individual name

> Not friends on Facebook? Maybe they are stealthy on Facebook and don't use
their full name? Maybe they are so cool that they don't use Facebook at all!
Look them up by name here.

<form id="name-lookup">
    <input id="name" type="text" name="in" placeholder="Full Name" />
    <br>
    <button type="submit">Search!</button>
</form>

<p id="name-output"></p>

<script>
    function processForm(e) {
        if (e.preventDefault) e.preventDefault();

        try {
            const results = fuse.search(document.getElementById('name').value);
            if (results.length === 0) {
                throw new Error("They are probably not in the district, name not matched");
            }
            document.getElementById("name-output").innerHTML = results.slice(0, 15).map(to_li).join("");
        } catch (error) {
            document.getElementById("name-output").innerHTML = `Sorry messed up: ${error.message}`;
            console.error(error.message);
        }

        // You must return false to prevent the default form behavior
        return false;
    }

    var form = document.getElementById('name-lookup');
    if (form.attachEvent) {
        form.attachEvent("submit", processForm);
    } else {
        form.addEventListener("submit", processForm);
    }
</script>

