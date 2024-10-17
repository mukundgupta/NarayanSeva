window.onpointermove = event => { 
  const { clientX, clientY } = event;
  
  blob.animate({
    left: `${clientX}px`,
    top: `${clientY}px`
  }, { duration: 3000, fill:"forwards" });

}



window.onload = function () {
  const trailer = document.getElementById("trailer"); 
};

var sec = document.getElementById("about-1");
var sec2 = document.getElementById("about-2");
var sec3 = document.getElementById("about-3");


function alertScroll() {
  var scrollVar = window.scrollY;
  sec.style.scale = scrollVar/10 + '%'; 
  sec2.style.scale = scrollVar/14 + '%'; 
  sec3.style.scale = scrollVar/20 + '%';  
}


window.addEventListener('scroll', function() {
  requestAnimationFrame(alertScroll);
})


window.onscroll = function() {
  const maxScroll = 3000; // Set maximum scroll height 

  if (window.scrollY > maxScroll) {
    window.scrollTo(0, maxScroll); // force scroll to stay at maxScroll
  }
};




const animateTrailer = (e, interacting) => {
  const x = e.clientX - trailer.offsetWidth / 2,
        y = e.clientY - trailer.offsetHeight / 2;
  
  const keyframes = {
    transform: `translate(${x}px, ${y}px) scale(${interacting ? 4 : 1})`
  }
  
  trailer.animate(keyframes, { 
    duration: 800, 
    fill: "forwards" 
  });
}

const getTrailerClass = type => {
  switch(type) {
    case "video":
      return "fa-solid fa-play";
    case "down":
      return "fa-solid fa-arrow-down fa-beat";  
    case "lead-to-page":
      return "fa-solid fa-arrow-right-from-bracket fa-beat";    
    case "home":
      return "fa-solid fa-house fa-beat"  
    case "plus":
      return "fa-solid fa-square-plus fa-beat" 
    case "submit":
      return "fa-regular fa-square-check"    
    default:
      return "fa-solid fa-arrow-up-right"; 
  }
}

window.onmousemove = e => {
  const interactable = e.target.closest(".interactable"),
        interacting = interactable !== null;
  
  const icon = document.getElementById("trailer-icon");
  
  animateTrailer(e, interacting);
  
  trailer.dataset.type = interacting ? interactable.dataset.type : "";
  
  if(interacting) {
    icon.className = getTrailerClass(interactable.dataset.type);
    trailer.style.backgroundColor = "#bfbeba";
  }
  else{
    trailer.style.backgroundColor = "white";
  }
}










