const showcaseImg = ['url("https://github.com/nemetht91/Automation-X/blob/main/static/img/robot2.png?raw=true")',
                        'url("https://github.com/nemetht91/Automation-X/blob/main/static/img/robot1.jpg?raw=true")'];

var imgCnt = 0;

window.setInterval(changeShowcaseImage, 10000)

/* Landing page image changing timer */
function changeShowcaseImage(){
    if (imgCnt == showcaseImg.length - 1){
        imgCnt = 0;
    }
    else{
        imgCnt++;
    }
    var newImage = showcaseImg[imgCnt];
    var r = document.querySelector(':root');
    r.style.setProperty('--showcase-background', newImage)
}


/* Mobile navigation */
const toggle = document.querySelector('.toggle');
const navigation = document.querySelector('.navbar .mobile')


toggle.addEventListener("click", () => {
    toggle.classList.toggle("active")
    navigation.classList.toggle("active")
});

window.addEventListener("resize", () => {
    if(window.innerWidth > 950 ){
        toggle.classList.remove("active")
        navigation.classList.remove("active")
    }
});

/* Portfolio navigatio */
const portfolio_menu = document.querySelectorAll(".services-navigation button")
const portfolio_menu_content = document.querySelectorAll(".services-portfolio .content")


for (var i = 0; i < portfolio_menu.length; i++){
    portfolio_menu[i].addEventListener("click", event => {
        removeAllMenuSelection();
        hideAllPortfolioContent();
        event.currentTarget.classList.add("selected");
        showPortfolioContent(event.currentTarget.getAttribute("id"));
    })
}

function showPortfolioContent(contentName){
    content = document.querySelector(".services-portfolio ."+contentName);
    content.classList.remove("hidden");
}

function removeAllMenuSelection(){
    for (var i = 0; i < portfolio_menu.length; i++){
        portfolio_menu[i].classList.remove("selected");
    }
}

function hideAllPortfolioContent(){
    for (var i = 0; i < portfolio_menu_content.length; i++){
        portfolio_menu_content[i].classList.add("hidden");
    }
}

