const showcaseImg = ['url("https://github.com/nemetht91/Automation-X/blob/main/static/img/robot2.png?raw=true")',
                        'url("https://github.com/nemetht91/Automation-X/blob/main/static/img/robot1.jpg?raw=true")'];

var imgCnt = 0;

window.setInterval(changeShowcaseImage, 10000)

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