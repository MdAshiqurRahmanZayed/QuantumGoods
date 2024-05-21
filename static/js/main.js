function fadeOut(element, duration) {
     var opacity = 1;
     var interval = 50;
     var gap = interval / duration;

     function fade() {
          opacity -= gap;
          if (opacity <= 0) {
               opacity = 0;
               element.style.display = 'none';
          } else {
               element.style.opacity = opacity;
               requestAnimationFrame(fade);
          }
     }

     fade();
}

document.addEventListener("DOMContentLoaded", function () {
     setTimeout(function () {
          var message = document.getElementById('message');
          if (message) {
               fadeOut(message, 2000);
          } 
     }, 4000);
});