/* deck-nav.js — navegação dos decks comerciais AAPSON.
   Toque (botões ◀▶ fixos), swipe horizontal, teclado (← → Home End), dots.
   Não depende de reveal/scroll-spy — é carrossel puro. Respeita prefers-reduced-motion no swipe. */
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  if(!slides.length) return;
  var dotsBox=document.getElementById('dots');
  var counter=document.getElementById('counter');
  var i=0;

  if(dotsBox){
    slides.forEach(function(_,n){
      var d=document.createElement('span');
      d.className='dot'+(n===0?' on':'');
      d.addEventListener('click',function(){go(n);});
      dotsBox.appendChild(d);
    });
  }
  function paint(){
    slides.forEach(function(s,k){s.classList.toggle('active',k===i);});
    if(dotsBox){[].slice.call(dotsBox.children).forEach(function(d,k){d.classList.toggle('on',k===i);});}
    if(counter){counter.textContent=String(i+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0');}
  }
  function go(n){i=(n+slides.length)%slides.length;paint();}

  // teclado
  window.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();go(i+1);}
    if(e.key==='ArrowLeft'){go(i-1);}
    if(e.key==='Home'){go(0);}
    if(e.key==='End'){go(slides.length-1);}
  });

  // botões de toque
  function bind(id,dir){
    var el=document.getElementById(id);
    if(!el) return;
    el.addEventListener('click',function(e){e.preventDefault();go(i+Number(dir));});
  }
  bind('deck-prev','-1');
  bind('deck-next','1');

  // swipe horizontal (só se não for reduced-motion e houver toque)
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  if(!reduce && ('ontouchstart' in window || navigator.maxTouchPoints>0)){
    var x0=null,y0=null;
    var deck=document.getElementById('deck')||document.body;
    deck.addEventListener('touchstart',function(e){
      if(e.touches&&e.touches.length){x0=e.touches[0].clientX;y0=e.touches[0].clientY;}
    },{passive:true});
    deck.addEventListener('touchend',function(e){
      if(x0===null) return;
      var t=e.changedTouches&&e.changedTouches[0]; if(!t){return;}
      var dx=t.clientX-x0, dy=t.clientY-y0;
      if(Math.abs(dx)>50 && Math.abs(dx)>Math.abs(dy)){
        go(i + (dx<0 ? 1 : -1));   // swipe esq -> prox, swipe dir -> ant
      }
      x0=y0=null;
    },{passive:true});
  }

  paint();
})();
