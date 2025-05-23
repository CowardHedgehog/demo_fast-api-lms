window.MathJax = {
  chtml: {
    matchFontHeight: false
  },
  tex: {
    inlineMath: [['$','$'],['\\(','\\)']],
    displayMath: [['$$','$$'],['\\[','\\]']],
    //processEscapes: true
  },
  svg: {
    fontCache: 'global'
  },
  startup: {
    typeset: false
  }
};

(function () {
  const script = document.createElement('script');
  if (navigator.userAgent.includes("Chrome") || navigator.userAgent.includes("Firefox"))
    script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js";
    //@/components/mathjax/tex-svg.js
  else
    script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
  script.async = true;
  document.head.appendChild(script);
})();