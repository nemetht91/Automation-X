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