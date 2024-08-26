---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

Welcome. Type a name in the text box and press go to search for a **single name**, **OR** select Browse and upload a file with a list of names in JSON format and select Browse and upload a file with a list of names in JSON format and press go to search for **many people**.

<script src="https://cdn.jsdelivr.net/npm/fuse.js/dist/fuse.js"></script>
<form id="my-form">
    <input id="name" type="text" name="in" placeholder="Full Name" />
    <br>
    <input id="friendslist" type="file" />
    <br>
    <button type="submit">Search!</button>
</form>

<ul id="output"></ul>

<script>
    const to_li = (result) => `<li>${result.item["Full Name"]}, age ${result.item.Age} (${((1 - result.score) * 100).toPrecision(4)}% accuracy)</li>`;
    let fuse;
    function processForm(e) {
        if (e.preventDefault) e.preventDefault();

        try {
            document.getElementById("output").innerHTML = "Loading..."
            const files = document.getElementById("friendslist").files;
            if (files.length > 0) {
                const fr = new FileReader();
                fr.readAsText(files[0]);
                fr.addEventListener(
                    "load",
                    () => {
                        const friends = JSON.parse(fr.result);
                        const matches = [];
                        friends.forEach(friend => {
                            const results = fuse.search(friend);
                            if (results.length > 0) {
                                matches.push(results[0]);
                            }
                        });
                        document.getElementById("output").innerHTML = matches.map(to_li).join("");
                    },
                    false,
                );
            } else {
                const results = fuse.search(document.getElementById('name').value);
                document.getElementById("output").innerHTML = to_li(results[0]);
            }
        } catch (error) {
            document.getElementById("output").innerHTML = `Sorry messed up: ${error.message}`;
            console.error(error.message);
        }

        // You must return false to prevent the default form behavior
        return false;
    }

    var form = document.getElementById('my-form');
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
                threshold: 0.05,
            }

            fuse = new Fuse(list, options)

            const result = fuse.search('JEAN MASON')
        } catch (error) {
            document.getElementById("output").innerHTML = `Sorry messed up: ${error.message}`;
            console.error(error.message);
        }
    }
    getData();
</script>

## How to get a JSON file with a list of Facebook friends

- Go to the friend list page: [https://www.facebook.com/friends/list](https://www.facebook.com/friends/list)
- Scroll all the way to the bottom of the page, loading all of your friends (I know, this is so tedious, you are so popular)
- Right click anywhere on the page and click `Inspect`, opening the developer tools
- Click on `Console` (it should be one of the tabs next to `Elements` or `Inspector` in the popup that has just come up)
- You're going to see it say things like *STOP*, etc. Unfortunately Facebook doesn't make this easy for us, so we have to, sorry
- Copy and paste the following code into the text box at the very bottom of the page, past all of the messages. Press enter. You should see a file called `friendsList.json` downloaded

```
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
Source: [https://stackoverflow.com/questions/50095522/how-to-get-whole-facebook-friends-list-from-api](https://stackoverflow.com/questions/50095522/how-to-get-whole-facebook-friends-list-from-api)

- Use the file upload above! It may take a few moments because you have so many friends. The file is never uploaded to a server or anything, it is all handled by your computer so it is safe. Of course, use at your own risk

