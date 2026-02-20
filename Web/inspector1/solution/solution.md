# Inspector1 walkthrough:

### Step1 (What the web site do?):
> ##### After examining the site, here what interest us:
> * `/` a simple web page with a static posts and some static comments where you can increase reaction count

### Step2 (Inspecting the Code):
> ###### We go to inspect and we see the reaction's increment functionality is handled by simple javascript
> ###### we find the **1st** part of the flag in the html as a comment, and we find also find the **3rd** pard of the flag jus there in the id attribute of the span of the 1st comment of the 1st post. 
> ```
> <div class="comment-header">
>   <span class="comment-author" id="_S0urc3_C0d3}">Houddini <span class="static-badge">Admin</span></span>                          <!--CSCC{R3m3mb3r_T0-->
>   <span class="comment-date">2025-12-28 11:00:00</span>
> </div>
> ```

### Step3 (Finding the 2nd part of the flag):
> ###### Now we need to find the 2nd part of the flag, so we go to the js file and we find nothing there, so we check the css file
> ###### And we find the **2nd** part there!
> ```
> .reaction-btn:hover {
>   border-color: #667eea;                    /*_4lw4y5_ch3ck*/
>   box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
>}
> ```
> ###### We concatenate the 3 parts and get our flag **CSCC{R3m3mb3r_T0_4lw4y5_ch3ck_S0urc3_C0d3}**
