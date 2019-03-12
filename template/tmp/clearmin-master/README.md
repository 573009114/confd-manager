#Clearmin Web Template

![Clearmin template](preview.png)


Bootstrap 3 dashboard / webapp / admin template

**Check the demo : http://cm.paomedia.com/**

**More doc inside the repo**

Browser support : ie9+, (Chrome, firefox, opera, safari), mobile browsers


## Quick start

To start using Clearmin template in a new project you can use this minimal template :
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">
    <link rel="stylesheet" type="text/css" href="assets/css/bootstrap-clearmin.min.css">
    <link rel="stylesheet" type="text/css" href="assets/css/roboto.css">
    <link rel="stylesheet" type="text/css" href="assets/css/material-design.css">
    <link rel="stylesheet" type="text/css" href="assets/css/small-n-flat.css">
    <link rel="stylesheet" type="text/css" href="assets/css/font-awesome.min.css">
    <title>Clearmin Page</title>
  </head>
  <body class="cm-no-transition cm-1-navbar">
    <div id="cm-menu">
      <nav class="cm-navbar cm-navbar-primary">
        <div class="cm-flex"><div class="cm-logo"></div></div>
        <div class="btn btn-primary md-menu-white" data-toggle="cm-menu"></div>
      </nav>
      <div id="cm-menu-content">
        <div id="cm-menu-items-wrapper">
          <div id="cm-menu-scroller">
            <ul class="cm-menu-items">
              <li class="active"><a href="#" class="sf-house">This page is active</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <header id="cm-header">
      <nav class="cm-navbar cm-navbar-primary">
        <div class="btn btn-primary md-menu-white hidden-md hidden-lg" data-toggle="cm-menu"></div>
        <div class="cm-flex"><h1>Put your title here</h1></div>
      </nav>
    </header>
    <div id="global">
      <div class="container-fluid">
        <div class="panel panel-default">
          <div class="panel-body">
            <h2 style="margin:0">Hello World !</h2>
          </div>
        </div>
      </div>
      <footer class="cm-footer"><span class="pull-right">&copy; ACME Inc.</span></footer>
    </div>
    <script src="assets/js/lib/jquery-2.1.3.min.js"></script>
    <script src="assets/js/jquery.mousewheel.min.js"></script>
    <script src="assets/js/jquery.cookie.min.js"></script>
    <script src="assets/js/fastclick.min.js"></script>
    <script src="assets/js/bootstrap.min.js"></script>
    <script src="assets/js/clearmin.min.js"></script>
  </body>
</html>
```

## General structure

### CSS and JS files

**CSS files (`<head>`) :**

*   assets/css/roboto.css (main font)
*   assets/css/bootstrap-clearmin.css (bootstrap theme)
*   assets/css/material-design.css (material design svg icons classes)
*   assets/css/small-n-flat.css (small-n-flat svg icons classes)
*   assets/css/font-awesome.min.css (iconic font classes)

**Javascript files (just before `</body>`) :**

*   assets/js/lib/jquery-2.1.3.min.js (required by bootstrap)
*   assets/js/lib/jquery.mousewheel.min.js (catch some scrolling events)
*   assets/js/lib/jquery.cookie.min.js (cookie manipulation plugin)
*   assets/js/lib/fastclick.min.js (enhance mobile device click events)
*   assets/js/bootstrap.min.js (bootstrap js widgets)
*   assets/js/clearmin.js (required by clearmin)


### Body classes

*   cm-no-transition : **must** be present to prevent certain browser to start transition on page load
*   cm-1-navbar : when one navbar is present on your page
*   cm-2-navbar : when two navbars are present on your page
*   cm-3-navbar : when three navbars are present on your page
*   cm-menu-toggled : if you want the menu to be toggled on page load (see next section)


### Preserving left menu state between pages

When the user choose to use the condensed version of the side menu, we want it to stay in this state when the user click on another page. To achieve this, a cookie is automatically set to reflect the menu state.

You got two different way to restore this state :

*   **Server-side** (recommended) : when your server receive a cookie named "cm-menu-toggled" with value "true", just add `.cm-menu-toggled` class to the body tag.
*   **Client-side** : Nothing to do, `.cm-menu-toggled` is automaticaly added to the body when needed but it can cause a blinking reflow on certain browsers (e.g. Google Chrome)

## Credits

*   [Bootstrap](http://getbootstrap.com/) css front-end framework.
*   [jQuery](http://jquery.com/) fast, small, and feature-rich JavaScript library.
*   [Summernote](http://hackerwins.github.io/summernote/) Super Simple WYSIWYG Editor on Bootstrap
*   [Font Awesome](http://fortawesome.github.io/Font-Awesome/) The iconic font and CSS toolkit
*   [Roboto](https://www.google.com/fonts/specimen/Roboto) Google font
*   [Small-n-flat icons](https://github.com/paomedia/small-n-flat) SVG icons on a 24px grid
*   [Material Design Icons](https://github.com/google/material-design-icons) Google SVG icons
*   [D3.js](http://d3js.org/) Data-Driven Documents
*   [C3.js](http://c3js.org/) D3-based reusable chart library
*   [Highlight.js](https://highlightjs.org/) Syntax highlighting for the Web
*   [Fastclick](https://github.com/ftlabs/fastclick) Polyfill to remove click delays on browsers with touch UIs
*   [Jquery-cookie](https://github.com/carhartl/jquery-cookie) A simple, lightweight jQuery plugin for reading, writing and deleting cookies
*   [Jquery-mousewheel](https://github.com/jquery/jquery-mousewheel) A jQuery plugin that adds cross-browser mouse wheel support


