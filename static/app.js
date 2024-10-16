const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting){
        entry.target.classList.add('show');
      }
      else{
        entry.target.classList.remove('show');
      }
    })
  })
  
const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));

const rightSideHidden = document.querySelectorAll('.hidden-r');
rightSideHidden.forEach((el) => observer.observe(el));

const fadeIn = document.querySelectorAll('.fade-in');
fadeIn.forEach((el) => observer.observe(el));



  
  